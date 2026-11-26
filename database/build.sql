-- =====================================================================
--  build.sql  —  builds database/app.db from your two SQL files
-- =====================================================================
--  You do NOT need to change this file. Run it from the starter-kit
--  folder with this command (see README.md, section 3):
--
--      sqlite3 -bail :memory: ".read database/build.sql"
--
--  The new database is first built in memory. Only if every statement
--  works is it saved as database/app.db; if anything fails, your old
--  database/app.db stays exactly as it was.
-- =====================================================================

-- 1. Make SQLite check FOREIGN KEYs (it does not, unless asked to).
PRAGMA foreign_keys = ON;

-- 2. Create your tables.
.read database/schema.sql

-- 3. Insert your sample data.
.read database/seed.sql

-- 4. Everything worked: save the new database as database/app.db.
.save database/app.db

.print "Done: database/app.db was built from schema.sql and seed.sql."
