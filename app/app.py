"""
=======================================================================
 app.py  —  the BACKEND of your app
=======================================================================
 You normally do NOT need to edit this file.

   Your SQL ............ app/queries.py
   Your database ....... database/app.db, which you build yourself from
                         database/schema.sql and database/seed.sql
                         (see README.md, section 3)
   The page layouts .... app/templates/*.html  (changing them is optional)

 Start the app:  in a terminal in the kit folder, type  bash start_mac.command  (macOS)
                or  start_windows.bat  (Windows)
=======================================================================
"""
import argparse
import re
import socket
import sqlite3
import sys
import threading
import webbrowser
from contextlib import closing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from flask import Flask, abort, g, render_template, request

import db
import kit

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

MAX_RESULT_ROWS = 500    # rows shown as the result of a feature

MYSQL_FUNCTIONS = ("SQLite names some functions differently from MySQL: use DATE('now', 'localtime') instead of "
                   "CURDATE(), DATETIME('now', 'localtime') instead of NOW(), STRFTIME('%Y', d) instead of YEAR(d), "
                   "JULIANDAY(a) - JULIANDAY(b) instead of DATEDIFF(a, b), and a || b instead of CONCAT(a, b).")
REBUILD = "build the database again (README.md, section 3)"

# (text in the error message, hint) - the first match wins.
HINTS = [
    ("readonly database",
     "This app only runs queries (SELECT). It cannot add, change or delete data: put INSERT statements "
     f"in seed.sql and {REBUILD}."),
    ("interrupted",
     f"The query took longer than {db.QUERY_SECONDS} seconds and was stopped. Check your JOIN conditions: "
     "a JOIN without a correct ON condition combines every row with every other row."),
    ("no such table",
     f"That table is not in database/app.db. Check the spelling. If you changed schema.sql, {REBUILD}."),
    ("no such column",
     f"That column is not in database/app.db. Check the spelling. If you changed schema.sql, {REBUILD}. "
     "If the word is meant to be text, put it in 'single quotes'."),
    ("no such function", MYSQL_FUNCTIONS),
    ('unrecognized token: "#"', "In SQL, comments start with -- (two dashes), not #."),
    ("unrecognized token",
     "SQLite found a character it does not understand. Check for curly quotes (“ ” ‘ ’) pasted from Word "
     "or a PDF, and for an unclosed 'quote'."),
    ("syntax error",
     "SQLite could not read the query. Look just before the word mentioned: usually a missing or extra "
     "comma, a missing bracket, text without 'single quotes', or a misspelled keyword."),
    ("did not supply a value for binding parameter",
     "The SQL uses a :name that has no matching Field(...) in queries.py. Add the Field or fix the spelling."),
    ("one statement at a time", "Each Feature may contain only ONE query. Remove the extra statement."),
    ("database is locked",
     "Another program is changing database/app.db right now (the build command, or DB Browser for SQLite "
     "with unsaved changes). Wait for it to finish, or click “Write Changes” in DB Browser, then try again."),
    ("file is not a database",
     f"database/app.db is not an SQLite database. Delete it and {REBUILD}."),
]


CURLY_QUOTES = ("SQLite found a curly quote (“ ” ‘ ’), usually pasted from Word or a PDF. "
                "Retype the quotes in VS Code as straight quotes: 'text' for text values.")


def hint_for(message):
    if any(q in message for q in "“”‘’"):
        return CURLY_QUOTES
    for needle, hint in HINTS:
        if needle.lower() in message.lower():
            return hint
    return ""


def loaded():
    """app/queries.py, read fresh once per page view."""
    if "loaded" not in g:
        g.loaded = kit.load_queries()
    return g.loaded


@app.template_filter("show")
def show_value(value):
    """How a value from the database appears on the page."""
    if isinstance(value, float) and not value.is_integer():
        return f"{value:.6f}".rstrip("0")
    return value


@app.context_processor
def common():
    return {"app_name": loaded().app_name}


@app.before_request
def need_database():
    if request.endpoint in ("index", "feature_page") and not db.exists():
        return render_template("no_database.html", command=db.BUILD_COMMAND), 503
    return None


def queries_error():
    return render_template("queries_error.html", error=loaded().error), 500


# ------------------------------------------------------------------ pages

@app.route("/")
def index():
    if loaded().error:
        return queries_error()
    return render_template("index.html", features=list(enumerate(loaded().features, start=1)))


@app.route("/feature/<int:number>")
def feature_page(number):
    if loaded().error:
        return queries_error()
    features = loaded().features
    if not 1 <= number <= len(features):
        abort(404)
    feature = features[number - 1]
    values = request.args

    with closing(db.connect()) as conn:
        options, option_errors = load_options(conn, feature)
        # A feature without input boxes runs straight away; otherwise it runs when the form is sent.
        should_run = not feature.fields or any(fld.name in values for fld in feature.fields)
        run = run_feature(conn, feature, values, options) if should_run else None

    return render_template("feature.html", feature=feature, number=number, options=options,
                           option_errors=option_errors, values=values, run=run, max_rows=MAX_RESULT_ROWS)


def load_options(conn, feature):
    """Run each Field's options_sql to fill its drop-down list."""
    options, errors = {}, {}
    for fld in feature.fields:
        if fld.options_sql:
            try:
                db.limit_time(conn)
                rows = conn.execute(fld.options_sql).fetchall()
                options[fld.name] = [(r[0], r[1] if len(r) > 1 else r[0]) for r in rows]
            except (sqlite3.Error, sqlite3.Warning) as e:
                errors[fld.name] = f"{e}. {hint_for(str(e))}"
    return options, errors


class InputError(ValueError):
    pass


def convert(fld, raw, choices):
    """Turn the text typed in the browser into the value given to SQLite."""
    if choices:
        for value, _label in choices:
            if str(value) == raw:
                return value
    if fld.type == "number":
        for kind in (int, float):
            try:
                return kind(raw)
            except ValueError:
                pass
        raise InputError(f"“{fld.label}” must be a number.")
    if fld.type == "date" and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        raise InputError(f"“{fld.label}” must be a date like 2026-12-02.")
    return raw


def run_feature(conn, feature, values, options):
    run = {"error": None, "hint": "", "stage": None}
    params, missing, bad = {}, [], []
    for fld in feature.fields:
        raw = values.get(fld.name, "").strip()
        if raw == "":
            params[fld.name] = None
            if fld.required:
                missing.append(fld.label)
        else:
            try:
                params[fld.name] = convert(fld, raw, options.get(fld.name))
            except InputError as e:
                bad.append(str(e))
    if missing or bad:
        problems = (["Please fill in: " + ", ".join(missing)] if missing else []) + bad
        run.update(error=" ".join(problems), stage="input")
        return run

    if kit.uses_question_marks(feature.sql) and not kit.param_names(feature.sql):
        params = tuple(params[fld.name] for fld in feature.fields)  # ? placeholders, in field order

    try:
        db.limit_time(conn)
        cur = conn.execute(feature.clean_sql, params)
        run["columns"] = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchmany(MAX_RESULT_ROWS + 1)
        run["more"] = len(rows) > MAX_RESULT_ROWS
        run["rows"] = rows[:MAX_RESULT_ROWS]
    except (sqlite3.Error, sqlite3.Warning, ValueError) as e:
        run.update(error=str(e), hint=hint_for(str(e)), stage="database")
    return run


@app.errorhandler(404)
def not_found(_e):
    return render_template("not_found.html"), 404


# ------------------------------------------------------------------ start-up

def free_port(start):
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    sys.exit(f"Ports {start}-{start + 19} are all in use. Close other copies of the app and try again.")


def main():
    parser = argparse.ArgumentParser(description="COMP3278 starter kit")
    parser.add_argument("--port", type=int, default=5050, help="first port to try (default 5050)")
    parser.add_argument("--no-browser", action="store_true", help="do not open a browser window")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)  # show messages immediately

    port = free_port(args.port)
    url = f"http://127.0.0.1:{port}"
    print("=" * 64)
    if port != args.port:
        print(f"  Port {args.port} is busy: another copy of the app is probably still")
        print(f"  running. This copy uses port {port} instead; close the other one")
        print("  (its terminal window) to avoid looking at the wrong copy.")
        print()
    print(f"  Your app is running at   {url}")
    print("  Keep this window open while you use the app.")
    print("  To stop the app: press Ctrl+C here, or close this window.")
    if not db.exists():
        print()
        print("  database/app.db does not exist yet. Build it first: open a")
        print("  terminal in the starter-kit folder and run")
        print(f"      {db.BUILD_COMMAND}")
    print("=" * 64)

    try:  # hide Flask's own start-up text; our message above replaces it
        import flask.cli
        import werkzeug.serving
        flask.cli.show_server_banner = lambda *a, **k: None
        werkzeug.serving.BaseWSGIServer.log_startup = lambda self: None
    except (ImportError, AttributeError):
        pass

    if not args.no_browser:
        threading.Timer(1.2, webbrowser.open, [url]).start()
    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    main()
