-- =====================================================================
--  schema.sql  —  creates every table in your database
-- =====================================================================
--  This is the DEMO schema for a tiny library: 3 tables.
--  Replace it with the tables from YOUR ER diagram.
--
--  After you change this file, build the database again:
--      sqlite3 -bail :memory: ".read database/build.sql"
--  (see README.md, section 3).
--
--  SQLite is not MySQL: write a numbered key column as exactly
--      id INTEGER PRIMARY KEY
--  (no INT, no AUTO_INCREMENT). See the table in README.md, section 4.
--
--  Order matters: create a table BEFORE any table that refers to it
--  with a FOREIGN KEY.
-- =====================================================================

-- Entity set: Member
CREATE TABLE members (
    member_id   INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    email       TEXT    NOT NULL UNIQUE,
    joined_on   DATE    NOT NULL
);

-- Entity set: Book
CREATE TABLE books (
    book_id     INTEGER PRIMARY KEY,
    title       TEXT    NOT NULL,
    author      TEXT    NOT NULL,
    year        INTEGER
);

-- Relationship set: a Member borrows a Book (many-to-many),
-- with its own attributes loan_date and return_date.
CREATE TABLE loans (
    loan_id     INTEGER PRIMARY KEY,
    member_id   INTEGER NOT NULL,
    book_id     INTEGER NOT NULL,
    loan_date   DATE    NOT NULL,
    return_date DATE,                       -- NULL means "not returned yet"
    FOREIGN KEY (member_id) REFERENCES members (member_id),
    FOREIGN KEY (book_id)   REFERENCES books (book_id)
);
