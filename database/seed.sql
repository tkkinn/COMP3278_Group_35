-- =====================================================================
--  seed.sql  —  fills your tables with sample data
-- =====================================================================
--  Replace this with realistic data for YOUR tables
--  (at least 10 rows in each table; small fixed lists may have fewer).
--
--  Order matters: insert the rows a FOREIGN KEY points to first
--  (members and books before loans).
-- =====================================================================

INSERT INTO members (member_id, name, email, joined_on) VALUES
    (1001, 'Jerry',  'jerry@example.com',      '2026-09-01'),
    (1002, 'Kit',    'kit@example.com',        '2026-09-01'),
    (1003, 'Kevin',  'kevin@example.com',      '2026-09-02'),
    (1004, 'Amy',    'amy@example.com',        '2026-09-03'),
    (1005, 'Ben',    'ben@example.com',        '2026-09-05'),
    (1006, 'Chloe',  'chloe@example.com',      '2026-09-08'),
    (1007, 'Daniel', 'daniel@example.com',     '2026-09-10'),
    (1008, 'Emma',   'emma@example.com',       '2026-09-12'),
    (1009, 'Frank',  'frank@example.com',      '2026-09-15'),
    (1010, 'Grace',  'grace@example.com',      '2026-09-20');

INSERT INTO books (book_id, title, author, year) VALUES
    (1,  'Database System Concepts',               'Silberschatz, Korth, Sudarshan', 2019),
    (2,  'Fundamentals of Database Systems',       'Elmasri, Navathe',               2016),
    (3,  'SQL Cookbook',                           'Molinaro, de Graaf',             2020),
    (4,  'Designing Data-Intensive Applications',  'Kleppmann',                      2017),
    (5,  'Clean Code',                             'Martin',                         2008),
    (6,  'Python Crash Course',                    'Matthes',                        2023),
    (7,  'The Pragmatic Programmer',               'Thomas, Hunt',                   2019),
    (8,  'Introduction to Algorithms',             'Cormen, Leiserson, Rivest, Stein', 2022),
    (9,  'Computer Networking: A Top-Down Approach', 'Kurose, Ross',                 2021),
    (10, 'Operating System Concepts',              'Silberschatz, Galvin, Gagne',    2018),
    (11, 'Learning SQL',                           'Beaulieu',                       2020),
    (12, 'Head First Design Patterns',             'Freeman, Robson',                2020);

INSERT INTO loans (loan_id, member_id, book_id, loan_date, return_date) VALUES
    (1,  1001, 1,  '2026-09-02', '2026-09-16'),
    (2,  1002, 1,  '2026-09-20', '2026-10-04'),
    (3,  1003, 4,  '2026-09-05', '2026-09-19'),
    (4,  1001, 4,  '2026-09-25', '2026-10-09'),
    (5,  1004, 2,  '2026-09-10', '2026-09-24'),
    (6,  1005, 3,  '2026-09-12', NULL),
    (7,  1006, 1,  '2026-10-08', NULL),
    (8,  1002, 5,  '2026-10-01', '2026-10-08'),
    (9,  1007, 6,  '2026-10-03', NULL),
    (10, 1008, 4,  '2026-10-12', NULL),
    (11, 1003, 7,  '2026-10-05', '2026-10-12'),
    (12, 1009, 8,  '2026-10-06', NULL),
    (13, 1010, 9,  '2026-10-07', '2026-10-13'),
    (14, 1001, 10, '2026-10-09', NULL),
    (15, 1004, 5,  '2026-10-11', NULL);
