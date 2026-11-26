# =======================================================================
#  queries.py  —  ALL the SQL of your app lives in this file
# =======================================================================
#
#  Each Feature(...) below becomes one page of your app. A feature answers
#  one question a user has, with one SQL query (SELECT ...):
#
#      Feature(
#          title="A member's loans",               # name in the menu
#          description="Books one member borrowed",# one sentence (optional)
#          fields=[                                # boxes the user fills in (optional)
#              Field("member_id", "Member",
#                    options_sql="SELECT member_id, name FROM members"),
#          ],
#          button="Show loans",                    # text on the button (optional)
#          sql="""
#              SELECT b.title, l.loan_date
#              FROM loans AS l
#              JOIN books AS b ON b.book_id = l.book_id
#              WHERE l.member_id = :member_id
#          """,
#      ),
#
#  Rules
#    * One Feature = exactly ONE query. The app only reads data: it never
#      adds, changes or deletes rows (all data comes from seed.sql).
#    * Write :name in the SQL wherever a value typed by the user goes,
#      and add a Field("name", ...) with the same name.
#    * Field types: "text" (default), "number", "date", "textarea".
#      options_sql="SELECT value, label FROM ..." turns a box into a drop-down.
#      required=False lets the user leave a box empty (the SQL gets NULL).
#    * Save this file and refresh the browser: no restart needed.
#
#  The features below are a DEMO for the tiny library in
#  database/schema.sql. Replace them with features for YOUR project.
# =======================================================================
from kit import Feature, Field

APP_NAME = "Mini Library (demo)"   # the name shown at the top of every page

# Every Feature(...) goes inside the square brackets below, each followed by a comma.
FEATURES = [

    Feature(
        title="All books",
        description="Every book in the library.",
        sql="""
            SELECT book_id, title, author, year
            FROM books
            ORDER BY title
        """,
    ),

    Feature(
        title="Search books by title",
        description="Books whose title contains a word.",
        fields=[
            Field("keyword", "Title contains"),
        ],
        button="Search",
        sql="""
            SELECT book_id, title, author, year
            FROM books
            WHERE title LIKE '%' || :keyword || '%'
            ORDER BY title
        """,
    ),

    Feature(
        title="A member's loans",
        description="All books one member has borrowed.",
        fields=[
            Field("member_id", "Member",
                  options_sql="SELECT member_id, name FROM members ORDER BY name"),
        ],
        button="Show loans",
        sql="""
            SELECT m.name, b.title, l.loan_date, l.return_date
            FROM loans AS l
            JOIN members AS m ON m.member_id = l.member_id
            JOIN books   AS b ON b.book_id   = l.book_id
            WHERE l.member_id = :member_id
            ORDER BY l.loan_date DESC
        """,
    ),

    Feature(
        title="Books on loan now",
        description="Books that are borrowed and not returned yet, and who has them.",
        sql="""
            SELECT b.title, m.name AS borrowed_by, l.loan_date
            FROM loans AS l
            JOIN books   AS b ON b.book_id   = l.book_id
            JOIN members AS m ON m.member_id = l.member_id
            WHERE l.return_date IS NULL
            ORDER BY l.loan_date
        """,
    ),

    Feature(
        title="Books on the shelf",
        description="Books that can be borrowed right now.",
        sql="""
            SELECT title, author
            FROM books
            WHERE book_id NOT IN (SELECT book_id FROM loans WHERE return_date IS NULL)
            ORDER BY title
        """,
    ),

    Feature(
        title="Most borrowed books",
        description="How many times each book has been borrowed.",
        sql="""
            SELECT b.title, COUNT(l.loan_id) AS times_borrowed
            FROM books AS b
            LEFT JOIN loans AS l ON l.book_id = b.book_id
            GROUP BY b.book_id, b.title
            ORDER BY times_borrowed DESC, b.title
        """,
    ),

    Feature(
        title="Long loans",
        description="Books kept longer than a number of days and not returned yet.",
        fields=[
            Field("days", "Longer than (days)", type="number"),
        ],
        button="Show",
        sql="""
            SELECT b.title, m.name, l.loan_date,
                   CAST(JULIANDAY('now', 'localtime') - JULIANDAY(l.loan_date) AS INTEGER) AS days_out
            FROM loans AS l
            JOIN books   AS b ON b.book_id   = l.book_id
            JOIN members AS m ON m.member_id = l.member_id
            WHERE l.return_date IS NULL
              AND JULIANDAY('now', 'localtime') - JULIANDAY(l.loan_date) > :days
            ORDER BY days_out DESC
        """,
    ),

    Feature(
        title="New members",
        description="Members who joined on or after a date.",
        fields=[
            Field("since", "Joined on or after", type="date"),
        ],
        button="Show",
        sql="""
            SELECT name, email, joined_on
            FROM members
            WHERE joined_on >= :since
            ORDER BY joined_on
        """,
    ),
]
