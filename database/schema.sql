-- =====================================================================
-- schema.sql — conference ticketing database (v2)
-- Converted from Melody's ER diagram, annotated with the group's
-- cardinality / participation spec (26 Nov 2026).
-- =====================================================================
-- Entities: Venue, Event, Speaker, Session, Attendee, Registration.
--
-- Relationships (notation: (min, max) per relationship end):
--   Venue —hosts—> Event        Venue (0,N) partial  ·  Event (1,1) total
--   Event —contains—> Session   Event (1,N) total    ·  Session (1,1) total
--   Speaker —gives—> Session    Speaker (0,N) partial ·  Session (1,1) total
--   Attendee —makes—> Registration  Attendee (0,N) partial · Registration (1,1) total
--   Event —has—> Registration       Event (0,N) partial    · Registration (1,1) total
--
-- Design notes:
--   * Venue "address" composite flattened to city, state, country, postal_code
--     (per the v2 ER spec).
--   * Speaker "contact" flattened to email (+ phone kept for the seed/app).
--   * Event "date" is now start_date/end_date (a date range).
--   * Speaker is split into first_name / last_name; same for Attendee.
--   * attendee.email is UNIQUE (one account per email).
--   * (attendee_id, event_id) is UNIQUE: an attendee registers at most once
--     per event (group business rule, confirmed 26 Nov 2026).
--   * "contains" is (1,N): every event has at least one session — enforced
--     by the seed data (SQLite cannot express min-cardinality on the Event
--     side as a table constraint).
--   * Session.speaker_id is NOT NULL: every session has exactly one primary
--     speaker ("give", Session side (1,1)).
--   * Registration keeps the attributes from the ER (registration_id PK,
--     ticket_type, price, purchase_date, status) plus attendee_id/event_id
--     as foreign keys implementing "makes" and "has".
-- =====================================================================

CREATE TABLE venues (
    venue_id          INTEGER PRIMARY KEY,
    name              TEXT    NOT NULL,
    city              TEXT,
    state             TEXT,
    country           TEXT,
    postal_code       TEXT,
    default_capacity  INTEGER
);

CREATE TABLE events (
    event_id      INTEGER PRIMARY KEY,
    name          TEXT    NOT NULL,
    description   TEXT,
    start_date    DATE    NOT NULL,
    end_date      DATE    NOT NULL,
    website       TEXT,
    timezone      TEXT,
    venue_id      INTEGER NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES venues (venue_id)
);

CREATE TABLE speakers (
    speaker_id    INTEGER PRIMARY KEY,
    first_name    TEXT    NOT NULL,
    last_name     TEXT    NOT NULL,
    email         TEXT,
    phone         TEXT,
    bio           TEXT,
    affiliation   TEXT,
    profile_url   TEXT
);

CREATE TABLE attendees (
    attendee_id   INTEGER PRIMARY KEY,
    first_name    TEXT    NOT NULL,
    last_name     TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    phone         TEXT,
    organization  TEXT
);

CREATE TABLE sessions (
    session_id    INTEGER PRIMARY KEY,
    event_id      INTEGER NOT NULL,
    speaker_id    INTEGER NOT NULL,
    title         TEXT    NOT NULL,
    description   TEXT,
    start_time    TEXT,
    end_time      TEXT,
    room          TEXT,
    capacity      INTEGER,
    status        TEXT    NOT NULL DEFAULT 'scheduled',
    FOREIGN KEY (event_id)   REFERENCES events (event_id),
    FOREIGN KEY (speaker_id) REFERENCES speakers (speaker_id)
);

CREATE TABLE registrations (
    registration_id   INTEGER PRIMARY KEY,
    attendee_id       INTEGER NOT NULL,
    event_id          INTEGER NOT NULL,
    ticket_type       TEXT    NOT NULL,
    price             REAL    NOT NULL,
    purchase_date     DATE    NOT NULL,
    status            TEXT    NOT NULL DEFAULT 'confirmed',
    payment_reference TEXT,
    FOREIGN KEY (attendee_id) REFERENCES attendees (attendee_id),
    FOREIGN KEY (event_id)    REFERENCES events (event_id),
    UNIQUE (attendee_id, event_id)   -- at most one registration per attendee per event
);

CREATE INDEX idx_events_venue            ON events (venue_id);
CREATE INDEX idx_sessions_event          ON sessions (event_id);
CREATE INDEX idx_sessions_speaker        ON sessions (speaker_id);
CREATE INDEX idx_registrations_attendee  ON registrations (attendee_id);
CREATE INDEX idx_registrations_event     ON registrations (event_id);
