"""
The building blocks you use in queries.py: Feature and Field.

You normally do NOT need to edit this file.
"""
import ast
import importlib.util
import re
import textwrap
import traceback
from dataclasses import dataclass, field as _field
from pathlib import Path

from db import without_strings

APP_DIR = Path(__file__).resolve().parent
QUERIES_PATH = APP_DIR / "queries.py"
FIELD_TYPES = ("text", "number", "date", "textarea")


@dataclass
class Field:
    """One input box on a feature's page.

    name         the :name used in your SQL, e.g. "member_id" for :member_id
    label        the text shown next to the box (defaults to the name)
    type         "text", "number", "date" or "textarea"
    options_sql  optional SELECT that turns the box into a drop-down list.
                 Its 1st column is the value put into your SQL,
                 its 2nd column is what the user sees.
    required     False lets the user leave it empty (your SQL then gets NULL)
    """
    name: str
    label: str = ""
    type: str = "text"
    options_sql: str = ""
    required: bool = True

    def __post_init__(self):
        if not self.label:
            self.label = self.name.replace("_", " ").capitalize()


@dataclass
class Feature:
    """One thing a user wants to find out = one page = one SQL query.

    title        the name shown in the menu, e.g. "A member's loans"
    sql          exactly one query (SELECT ...); use :name for values typed by the user
    description  one sentence shown under the title
    fields       a list of Field(...) the user fills in before the SQL runs
    button       the text on the button, e.g. "Show loans"
    """
    title: str
    sql: str
    description: str = ""
    fields: list = _field(default_factory=list)
    button: str = "Run"

    @property
    def clean_sql(self):
        return textwrap.dedent(self.sql).strip().rstrip(";").strip()


# ---------------------------------------------------------------- SQL helpers

_COMMENTS = re.compile(r"--[^\n]*|/\*.*?\*/", re.S)


def strip_comments(sql):
    return _COMMENTS.sub(" ", sql)


def param_names(sql):
    return sorted(set(re.findall(r"(?<![:\w]):(\w+)", without_strings(strip_comments(sql)))))


def uses_question_marks(sql):
    return "?" in without_strings(strip_comments(sql))


# ---------------------------------------------------------------- loading queries.py

@dataclass
class Loaded:
    features: list
    app_name: str
    error: dict = None


def _python_hint(message):
    """Plain-language advice for the Python mistakes beginners make in queries.py."""
    m = message.lower()
    if "invalid character" in m and any(q in message for q in "“”‘’"):
        return ("This line contains curly quotes (“ ” ‘ ’). Python only accepts straight quotes \" and '. "
                "They usually come from Word, TextEdit, Notes or a PDF: edit queries.py in VS Code and retype the quotes.")
    if "perhaps you forgot a comma" in m:
        return ("A comma is missing. Python points to the START of the part that is missing it, so look at the end of "
                "the Feature(...) or Field(...) that starts on this line: a comma is needed after its closing ) and "
                "after every line like title=\"...\" inside it. (Comments in queries.py start with #, not --.)")
    if "triple-quoted" in m or "unterminated string" in m or "eol while scanning" in m:
        return ("A text in quotes is not closed. Check every sql=\"\"\" ... \"\"\" above this line: each needs exactly three "
                "quotes at the start AND at the end. Python sometimes reports a later line than the real mistake.")
    if "indent" in m:
        return ("Spaces at the start of a line matter in Python. APP_NAME = ... and FEATURES = [ must start at the very "
                "beginning of the line; lines inside FEATURES = [ ... ] should be indented.")
    if "name 'false'" in m or "name 'true'" in m or "name 'none'" in m or "name 'null'" in m:
        return "Python writes True, False and None with a capital first letter, e.g. required=False."
    if "name 'feature'" in m or "name 'field'" in m:
        return "Keep the line  from kit import Feature, Field  at the top of queries.py."
    if "nameerror" in m:
        return ("Python thinks this word is a variable. Text must be inside quotes, e.g. title=\"My page\", "
                "and SQL inside sql=\"\"\" ... \"\"\".")
    if "unexpected keyword argument" in m:
        return ("A setting name is misspelled. Feature(...) accepts title, sql, description, fields, button; "
                "Field(...) accepts name, label, type, options_sql, required.")
    if "invalid syntax" in m:
        return ("Python could not read this line. Check this line and the end of the line just before it for a "
                "missing comma, a missing or extra bracket ( ) [ ], or SQL that is outside the \"\"\" quotes. "
                "Comments in queries.py start with #, not --.")
    return ""


def _stray_features(source):
    """Line numbers of Feature(...) blocks that are outside FEATURES = [ ... ] and so would be ignored."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    inside = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "FEATURES" for t in node.targets):
            inside |= {id(n) for n in ast.walk(node.value)}
    return [n.lineno for n in ast.walk(tree)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "Feature"
            and id(n) not in inside]


def load_queries():
    """Read app/queries.py fresh every time, so your edits show up after a page refresh."""
    default_name = "My COMP3278 App"

    def failed(line, code, message, hint=None):
        return Loaded([], default_name, {"line": line, "code": (code or "").rstrip(), "message": message,
                                         "hint": _python_hint(message) if hint is None else hint})

    try:
        source = QUERIES_PATH.read_text(encoding="utf-8")
        spec = importlib.util.spec_from_file_location("queries", QUERIES_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except FileNotFoundError:
        return failed(None, "", "app/queries.py is missing.", "")
    except UnicodeDecodeError:
        return failed(None, "", "app/queries.py is not saved as UTF-8 text, so Python cannot read it.",
                      "In VS Code, click the encoding name at the bottom right of the window (for example “Big5”), "
                      "choose “Save with Encoding” and then “UTF-8”.")
    except SyntaxError as e:
        if "unexpected indent" in e.msg and (e.text or "").strip().startswith("Feature("):
            return failed(e.lineno, e.text,
                          f"The Feature(...) on line {e.lineno} is outside FEATURES = [ ... ], so Python cannot read it.",
                          "Move it above the closing ] of FEATURES (and put a comma after the Feature before it).")
        return failed(e.lineno, e.text, f"{type(e).__name__}: {e.msg}")
    except Exception as e:
        frames = [f for f in traceback.extract_tb(e.__traceback__) if Path(f.filename) == QUERIES_PATH]
        frame = frames[-1] if frames else None
        return failed(frame.lineno if frame else None, frame.line if frame else "", f"{type(e).__name__}: {e}")

    stray = _stray_features(source)
    if stray:
        line = stray[0]
        return failed(line, source.splitlines()[line - 1],
                      f"The Feature(...) on line {line} is outside FEATURES = [ ... ], so the app would ignore it.",
                      "Move it above the closing ] of FEATURES (and put a comma after the Feature before it).")

    app_name = getattr(module, "APP_NAME", default_name)
    features = getattr(module, "FEATURES", None)
    problem = _check_features(features)
    if problem:
        return Loaded([], app_name, {"line": None, "code": "", "message": problem, "hint": ""})
    return Loaded(list(features), app_name)


def _check_features(features):
    if features is None:
        return "app/queries.py must define a list called FEATURES."
    if not isinstance(features, (list, tuple)):
        return "FEATURES in app/queries.py must be a list: FEATURES = [ Feature(...), Feature(...) ]"
    for i, f in enumerate(features, start=1):
        if not isinstance(f, Feature):
            return f"Item {i} in FEATURES is not a Feature(...)."
        name = f'Feature {i} ("{f.title}")'
        for attr in ("title", "description", "button"):
            if not isinstance(getattr(f, attr), str):
                return f'{name}: {attr}= must be text in quotes, e.g. {attr}="..."'
        if not isinstance(f.sql, str) or not f.sql.strip():
            return f"{name} has no SQL. Write it as sql=\"\"\" ... \"\"\"."
        if not isinstance(f.fields, (list, tuple)):
            return f"{name}: fields= must be a list in square brackets: fields=[ Field(...), Field(...) ]"
        for fld in f.fields:
            if not isinstance(fld, Field):
                return f"{name}: every item in fields=[...] must be a Field(...)."
            if not isinstance(fld.name, str) or not fld.name.isidentifier():
                return (f'{name}: the field name {fld.name!r} must be one word made of letters, digits and _, '
                        "matching the :name in your SQL.")
            if fld.type not in FIELD_TYPES:
                return (f'{name}: field "{fld.name}" has type "{fld.type}". '
                        f"Use one of: {', '.join(FIELD_TYPES)}.")
            if not isinstance(fld.required, bool):
                return (f'{name}: field "{fld.name}" has required={fld.required!r}. '
                        "Write required=False or required=True (capital letter, no quotes).")
            if not isinstance(fld.options_sql, str):
                return f'{name}: field "{fld.name}": options_sql= must be SQL text in quotes.'
    return None
