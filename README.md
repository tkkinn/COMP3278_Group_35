# COMP3278 Starter Kit: Technical Help

What to do and what to hand in is in the project instructions
(`COMP3278_Group_Project_Instructions.docx`). This file gives the technical details
behind them: how to set up your computer, how to use a terminal, how to build and look
inside your database, how to write your SQL files and `queries.py`, and what to do when
something goes wrong. Use it when you need it; you do not have to read it from start to end.

Tip: open this file in VS Code and press Ctrl+Shift+V (Windows) or Cmd+Shift+V (macOS)
to see it nicely formatted.

| Section | Topic |
|---|---|
| 1 | Setting up your computer |
| 2 | Using a terminal and starting the app |
| 3 | Building and looking inside your database |
| 4 | Writing `schema.sql` and `seed.sql` |
| 5 | Writing your features in `queries.py` (Option A) |
| 6 | When something goes wrong |
| 7 | Words you will see |

---

## 1. Setting up your computer

### 1.1 Install Python

1. Go to <https://www.python.org/downloads/> and download the latest Python 3.
2. Run the installer.
   - Windows: on the first screen, tick "Add python.exe to PATH", then click "Install Now".
   - macOS: click through the installer with the default options.

### 1.2 Install VS Code

Download it from <https://code.visualstudio.com/> and use it to edit the kit's files.
Do not edit them in Word, TextEdit or Notes: those programs turn straight quotes (`"`)
into curly quotes (`“ ”`), which Python and SQL cannot read.

### 1.3 Get sqlite3

`sqlite3` is SQLite's command-line program. You use it to build your database and to
look inside it (section 3).

- macOS: it is already on your Mac. Nothing to install.
- Windows: download it once and put it in the starter-kit folder:
  1. Go to <https://sqlite.org/download.html> and scroll to "Precompiled Binaries for Windows".
  2. Download the file whose name starts with `sqlite-tools-win-x64` (a .zip file).
  3. Open the zip and copy `sqlite3.exe` into your starter-kit folder, next to
     `start_windows.bat`. You do not need the other files in the zip.

To check that it works, open a terminal in the starter-kit folder (section 2.2), type
`sqlite3 --version` and press Enter. You should see a version number such as 3.54.0.

Optional: DB Browser for SQLite (<https://sqlitebrowser.org/dl/>) lets you look at your
tables with the mouse instead of typing commands (section 3.3).

---

## 2. Using a terminal and starting the app

You start the app by typing one command into a terminal, and you use the same kind of
window to build your database (section 3).

### 2.1 Put the starter kit in the right place

Extract the zip first. Do not run anything while it is still inside the zip.

- Windows: right-click the zip → "Extract All..." and extract it to `C:\COMP3278`.
  Your Desktop and Documents folders are often synced by OneDrive, which can lock the
  database file.
- macOS: double-click the zip, then move the folder into your home folder
  (in Finder: "Go" → "Home"). Avoid iCloud Drive folders.

### 2.2 Open a terminal in the starter-kit folder

A terminal is a window where you type commands instead of clicking. Each command starts
a program. A terminal is always "in" one folder, the current folder, and commands look
for files starting from there. So the most important thing is to open the terminal in
the starter-kit folder.

Windows (use Command Prompt, not PowerShell):

1. Open the starter-kit folder in File Explorer (the folder that contains `start_windows.bat`).
2. Click in the address bar at the top, type `cmd` and press Enter.
3. A black window opens. Its last line ends with the folder, for example
   `C:\COMP3278\COMP3278_starter_kit>`.

macOS:

1. In Finder, right-click the starter-kit folder → "Services" → "New Terminal at Folder".
2. If you do not see that menu item: open the Terminal app, type `cd ` (with a space
   after it), drag the starter-kit folder into the Terminal window, and press Return.

Check that you are in the right folder: type `dir` (Windows) or `ls` (macOS) and press
Enter. You should see `app`, `database`, `README.md` and the start files in the list.
If not, close the window and try again.

### 2.3 Start the app

In that terminal, type the command for your computer and press Enter:

| Your computer | Command |
|---|---|
| Windows | `start_windows.bat` |
| macOS | `bash start_mac.command` |

The first start takes a little longer: it sets up Python for this project in a hidden
`.venv` folder. Then your browser opens the app at <http://127.0.0.1:5050>.

You can also double-click `start_windows.bat` or `start_mac.command` in the folder, but
your computer may block a file downloaded from the internet:

- Windows: if a blue box says "Windows protected your PC", click "More info" → "Run anyway".
- macOS: if it says "cannot be opened because it is from an unidentified developer" or
  "Apple could not verify ...", click "OK" or "Done" (never "Move to Trash") and type the
  command above instead.

### 2.4 While the app is running

Keep this terminal open: closing it stops the app. Lines in it such as
`"GET /feature/3 HTTP/1.1" 200` are the requests your browser (the frontend) sends to
the backend.

- Windows: do not click inside that window. Windows pauses the app while text in it is
  selected; if the app seems frozen, click in the window and press Enter.
- To stop the app, press Ctrl+C in the terminal, or close it (on Windows, answer Y to
  "Terminate batch job?").
- To start it again, type the start command again. Tip: press the ↑ key to bring back
  the last command instead of typing it again.

This terminal is busy running the app. To type other commands (section 3), open a second
terminal in the starter-kit folder in the same way (section 2.2).

---

## 3. Building and looking inside your database

### 3.1 What the build command does

You build `database/app.db` from your two SQL files with this command, typed into a
terminal in the starter-kit folder:

```
sqlite3 -bail :memory: ".read database/build.sql"
```

If everything is correct, you see:

```
Done: database/app.db was built from schema.sql and seed.sql.
```

Then refresh the app in your browser; you do not need to restart it. Each run builds a
new database and replaces the old one, so you can run it as often as you like.

The command has four parts:

| Part | Meaning |
|---|---|
| `sqlite3` | Start SQLite's own command-line program. Like the app, it is a program that talks to the database. |
| `-bail` | Stop at the first error, instead of carrying on with a half-built database. |
| `:memory:` | Build the new database in the computer's memory first, not in a file. |
| `".read database/build.sql"` | Run the commands in the file `database/build.sql`. |

`database/build.sql` is provided; do not change it. It does four things:

| Line in `build.sql` | What it does |
|---|---|
| `PRAGMA foreign_keys = ON;` | Makes SQLite check every FOREIGN KEY. Without this line, SQLite would silently accept rows that point to ids that do not exist. |
| `.read database/schema.sql` | Runs your `CREATE TABLE` statements: the tables now exist, empty. |
| `.read database/seed.sql` | Runs your `INSERT` statements: the tables are now filled. |
| `.save database/app.db` | Everything worked: saves the new database as `database/app.db`, replacing the old one. |

If any step fails, `-bail` stops before `.save`, so your old `app.db` stays exactly as
it was. Lines that start with a dot (`.read`, `.save`, `.print`) are commands for the
`sqlite3` program itself, not SQL. In short: your database is exactly what your two SQL
files say, nothing more.

### 3.2 When the build fails

The command stops at the first mistake and shows where it is, for example:

```
Parse error near line 23: no such column: Beaulieu
     (11, 'Learning SQL',                           Beaulieu,
                                      error here ---^
```

- "Line 23" is the line where the statement with the mistake starts, in the file that was
  being read: `schema.sql` if the mistake is in a `CREATE TABLE`, `seed.sql` if it is in an
  `INSERT`. VS Code shows the line number to the left of every line. The mistake itself
  can be further down in that statement: look for the text shown above the arrow (here it
  is on line 34).
- Some messages have no arrow, for example "FOREIGN KEY constraint failed". Then check
  every row of the `INSERT` that starts on that line.
- "foreign key mismatch" is reported while `seed.sql` is being read, but the mistake is
  in `schema.sql` (see section 6).
- The arrow points at the problem. Here, the text Beaulieu has no quotes, so SQLite
  thinks it is a column name. It should be `'Beaulieu'`.
- Nothing was saved, so the app still uses your previous database.
- Fix the file, save it, and run the command again (press ↑, then Enter).

Section 6 explains the common messages.

### 3.3 Look inside your database

You can use `sqlite3` to look at your tables at any time:

| To ... | Type |
|---|---|
| list your tables | `sqlite3 database/app.db ".tables"` |
| show the columns of a table | `sqlite3 database/app.db ".schema loans"` |
| show the rows of a table | `sqlite3 -header -column database/app.db "SELECT * FROM loans;"` |
| try any query | `sqlite3 -header -column database/app.db "SELECT ... ;"` |

This is also how you test a query before you put it into your app, and how you show the
rows behind a result in your video's live demo. Two things to know when you test a query:

- Write the whole query on one line.
- If your query contains `:name` (a value the user enters), replace it with a real value
  while testing, for example `WHERE l.member_id = 1001` instead of
  `WHERE l.member_id = :member_id`. Otherwise `sqlite3` returns no rows and shows no error.

If you prefer the mouse, open DB Browser for SQLite → "Open Database Read Only" → choose
`database/app.db` → tab "Browse Data". Use it only to look. After you build the database
again, close it in DB Browser ("Close Database") and open it again; otherwise it keeps
showing the old data.

---

## 4. Writing `schema.sql` and `seed.sql`

These two files must match, so rewrite both before you build. If you only replace
`schema.sql`, the build fails, because the demo data in `seed.sql` refers to the demo
tables.

`schema.sql` turns your ER diagram into `CREATE TABLE` statements, for example:

```sql
CREATE TABLE members (
    member_id   INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    email       TEXT    NOT NULL UNIQUE
);

CREATE TABLE books (
    book_id     INTEGER PRIMARY KEY,
    title       TEXT    NOT NULL
);

CREATE TABLE loans (
    loan_id     INTEGER PRIMARY KEY,
    member_id   INTEGER NOT NULL,
    book_id     INTEGER NOT NULL,
    loan_date   DATE    NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members (member_id),
    FOREIGN KEY (book_id)   REFERENCES books (book_id)
);
```

- End every statement with `;`.
- Create a table before any table whose FOREIGN KEY refers to it.
- A FOREIGN KEY must point at the primary key of the other table.
- SQL comments start with `--`.

SQLite is not MySQL. If you learned MySQL, watch out for these:

| Instead of (MySQL) | Write (SQLite) |
|---|---|
| `id INT AUTO_INCREMENT PRIMARY KEY` | `id INTEGER PRIMARY KEY` (exactly INTEGER; it numbers new rows by itself) |
| `ENUM('open', 'closed')` | `TEXT CHECK (status IN ('open', 'closed'))` |
| `VARCHAR(50)`, `INT`, `DATETIME` | fine, but `TEXT`, `INTEGER`, `DATE` are simpler |
| `NOW()` / `CURDATE()` | `DATETIME('now', 'localtime')` / `DATE('now', 'localtime')` |
| `YEAR(d)`, `MONTH(d)` | `STRFTIME('%Y', d)`, `STRFTIME('%m', d)` |
| `DATEDIFF(a, b)` | `JULIANDAY(a) - JULIANDAY(b)` |
| `CONCAT(a, b)` | `a \|\| b` |

`seed.sql` adds your sample data, for example:

```sql
INSERT INTO members (member_id, name, email) VALUES
    (1001, 'Jerry', 'jerry@example.com'),
    (1002, 'Kit',   'kit@example.com');
```

- Insert the rows that a foreign key points to first (members and books before loans).
- Text values need single quotes (`'Jerry'`); numbers do not.
- To write an apostrophe inside text, type it twice: `'Dragon''s Back'`.
- Dates are text in the form `'2026-11-20'`.

After you build the database with your own tables, the demo feature pages show red
errors, because `app/queries.py` still contains the demo features, which use tables you
just removed. That is expected: you replace them with your own features (section 5).

---

## 5. Writing your features in `queries.py` (Option A)

This is the shape of the whole file:

```python
from kit import Feature, Field            # keep this line exactly as it is

APP_NAME = "Club Event Booking"            # the name at the top of every page

FEATURES = [
    Feature(
        ...                                # your first feature
    ),
    Feature(
        ...                                # your second feature
    ),
]                                          # every Feature goes ABOVE this bracket
```

Delete the demo features (everything between `FEATURES = [` and the final `]`) and add
your own. Each `Feature(...)` becomes one page.

A feature that needs no input:

```python
    Feature(
        title="All members",
        description="Everyone who has joined the library.",
        sql="""
            SELECT member_id, name, email
            FROM members
            ORDER BY name
        """,
    ),
```

A feature where the user types or picks something:

```python
    Feature(
        title="A member's loans",
        fields=[
            Field("member_id", "Member",
                  options_sql="SELECT member_id, name FROM members ORDER BY name"),
        ],
        button="Show loans",
        sql="""
            SELECT b.title, l.loan_date, l.return_date
            FROM loans AS l
            JOIN books AS b ON b.book_id = l.book_id
            WHERE l.member_id = :member_id
            ORDER BY l.loan_date DESC
        """,
    ),
```

More kinds of input boxes:

```python
            Field("title", "Event title"),                        # text (the default)
            Field("capacity", "Capacity", type="number"),         # numbers only
            Field("event_date", "Date", type="date"),             # a date picker
            Field("notes", "Notes", type="textarea", required=False),  # long text, may be empty
```

How it works:

- `:member_id` in the SQL is filled with what the user entered in
  `Field("member_id", ...)`. The names must match exactly.
- `options_sql` turns a box into a drop-down list. Its first column is the value given
  to your SQL; its second column is what the user sees. Use it for every foreign key, so
  that users pick a name instead of typing an id.
- `required=False` allows an empty box (your SQL then receives NULL).
- The page shows the rows your query returns (at most 500). A query that runs longer
  than 5 seconds is stopped.

Rules:

1. One feature is exactly one query. `INSERT`, `UPDATE` and `DELETE` are refused: the
   app only reads data. Put your data in `seed.sql` instead.
2. Never build SQL by pasting user input into the text. Always use `:name`. This is what
   protects real apps from SQL injection.

All you need to know about Python:

- Every line inside `Feature(...)` ends with a comma, and so does the closing `),` of
  every `Feature` and every `Field`.
- Text goes in straight quotes: `title="All members"`. SQL goes between three quotes at
  both ends: `sql=""" ... """`.
- `True`, `False` and `None` start with a capital letter and have no quotes:
  `required=False`.
- Comments in Python start with `#`. Inside the SQL text, use SQL comments (`--`).
- Spaces at the start of a line matter: `APP_NAME` and `FEATURES` start at the very
  beginning of the line. Copy the indentation of the examples.

Save the file and refresh the browser; you do not need to restart the app. If something
is wrong, the app shows the line and a hint.

---

## 6. When something goes wrong

Starting the app:

| What you see | What to do |
|---|---|
| "You opened this file from inside the zip" | Extract the zip first (section 2.1). |
| "Python is not installed" | Install Python (section 1.1). On Windows, run the installer again and tick "Add python.exe to PATH". |
| Windows: "'start_windows.bat' is not recognized as an internal or external command" | The terminal is not in the starter-kit folder, or it is PowerShell. Open it as in section 2.2. |
| macOS: "No such file or directory" | The terminal is not in the starter-kit folder. Open it as in section 2.2. |
| "Windows protected your PC" (after double-clicking) | Click "More info" → "Run anyway", or type the start command instead (section 2.3). |
| macOS: "cannot be opened", "Apple could not verify" or "you do not have appropriate access privileges" (after double-clicking) | Click "OK" or "Done" (never "Move to Trash") and type `bash start_mac.command` in a terminal instead (section 2.3). |
| "Could not create .venv", or an error that mentions `.venv` | Close the terminal, delete the `.venv` folder in the starter-kit folder (it is hidden on macOS: press Cmd+Shift+. in Finder to see it), and start the app again. |
| The app seems frozen (Windows) | Click in the black window and press Enter. |
| The browser does not open | Open <http://127.0.0.1:5050> yourself. If that port is busy, the terminal shows the address it used instead. |
| The app says "No database yet" | Build the database (section 3.1), then refresh the page. |

Building the database (in the terminal):

| What you see | What to do |
|---|---|
| Windows: "'sqlite3' is not recognized as an internal or external command" | `sqlite3.exe` is not in the starter-kit folder (section 1.3), or the terminal is not in that folder, or it is PowerShell. Open it as in section 2.2, and check that `dir` lists `sqlite3.exe`. |
| macOS: "command not found: sqlite3" | Type `xcode-select --install`, follow the window that opens, then try again. |
| cannot open "database/build.sql" | The terminal is not in the starter-kit folder (section 2.2). |
| "Parse error near line N: ..." | Look at line N of `schema.sql` or `seed.sql` and at the arrow (section 3.2). |
| "no such table: X" | `seed.sql` inserts into a table that `schema.sql` does not create. Check the spelling, or rewrite `seed.sql` for your tables. |
| "no such column: X" while building | Usually text without single quotes, an apostrophe that is not doubled (`'Dragon''s Back'`), or curly quotes (`‘ ’`) instead of straight ones (`'`). |
| "NOT NULL constraint failed: T.c" | A row has no value for column c of table T, which is NOT NULL. Give every row a value there. |
| "CHECK constraint failed" | A value is not one of the values the CHECK allows. Capitals count: `'Sports'` is not `'sports'`. |
| "all VALUES must have the same number of terms" | One row in the `INSERT` has more or fewer values than the others. Count the values in each row. |
| "FOREIGN KEY constraint failed" | A row refers to an id that does not exist (yet). Check the ids, and insert the rows being referred to first. |
| "UNIQUE constraint failed" | Two rows have the same value in a column that must be unique (often the primary key). |
| "foreign key mismatch" | A FOREIGN KEY in `schema.sql` points at a column that is not the primary key of the other table. |
| "table X already exists" | `schema.sql` creates the same table twice. |
| "database is locked" or "unable to open database" | `app.db` is open in DB Browser with unsaved changes, or in another program. Close it there and run the command again. |
| Rows get an empty (NULL) id | Write the key as exactly `id INTEGER PRIMARY KEY` (not INT, no AUTO_INCREMENT), then build again. |

Your features (in the app):

| What you see | What to do |
|---|---|
| "Problem in app/queries.py" | Read the line number and the hint. Most often: a missing comma, curly quotes, or a missing `"""`. |
| "... is outside FEATURES = [ ... ]" | Move that `Feature(...)` above the final `]`. |
| "no such table" or "no such column" | Check the spelling. If you changed `schema.sql`, build the database again (section 3.1). |
| A message about curly quotes (“ ” ‘ ’) | Retype the quotes in VS Code as straight quotes: `"` in Python, `'` around text in SQL. |
| "app/queries.py is not saved as UTF-8 text" | In VS Code, click the encoding name at the bottom right of the window, choose "Save with Encoding" and then "UTF-8". |
| "no such function: NOW" (or CURDATE, YEAR, CONCAT ...) | Use the SQLite version from the table in section 4. |
| "attempt to write a readonly database" | Your feature contains `INSERT`, `UPDATE` or `DELETE`. Features can only query; put data in `seed.sql`. |
| "The query took longer than 5 seconds" | Usually a `JOIN` without a correct `ON` condition, which combines every row with every other row. |
| The app still shows old data | Did the build command end with "Done"? Then refresh the page. If the terminal said "Port 5050 is busy", an older copy of the app is still running: close its terminal, and use the address the new copy shows. |

Still stuck? Ask on Ed (or ask an AI tool to explain the message), and include a
screenshot of the error.

---

## 7. Words you will see

| Word | Meaning |
|---|---|
| Terminal, Command Prompt | A window where you type commands instead of clicking (section 2.2). On Windows it is called Command Prompt or cmd. |
| Command | One line you type into a terminal and run with Enter, such as the build command. |
| Current folder | The folder a terminal is "in". Commands look for files starting from there. |
| sqlite3 | SQLite's own command-line program. You use it to build your database and to look inside it. |
| localhost, 127.0.0.1 | "This computer". The app runs only on your computer; nobody else can see it. |
| Port (:5050) | A numbered "door" on your computer that a program listens on. |
| Request | A message your browser sends to the backend, such as `GET /feature/3`. |
| PATH | The list of places Windows looks for programs. Ticking "Add python.exe to PATH" lets Windows find Python. |
| `.venv` | A hidden folder with this project's own copy of Python and Flask. It is made on the first start; never submit it. |
| Flask | The Python library the backend (`app/app.py`) is built with. You do not need to learn it. |
| Markdown | A plain-text format for documents. This README is written in it. |
