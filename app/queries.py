# =======================================================================
#  queries.py — conference ticketing features (starter set)
# =======================================================================
#  These 9 features are a working starter set for the conference schema in
#  database/schema.sql. Emma, Ruairi and Jacob can rename, refine or replace
#  them with their final feature list.
#
#  Each Feature(...) is one page of the app and exactly ONE SELECT query.
#  User-typed values are passed as :name parameters, never concatenated.
# =======================================================================
from kit import Feature, Field

APP_NAME = "Conference Ticketing (demo)"

FEATURES = [

    Feature(
        title="All events",
        description="Every event with its dates and venue.",
        sql="""
            SELECT e.event_id, e.name, e.start_date, e.end_date, v.name AS venue
            FROM events AS e
            JOIN venues AS v ON v.venue_id = e.venue_id
            ORDER BY e.start_date
        """,
    ),

    Feature(
        title="Sessions for an event",
        description="All sessions in one event, with the speaker.",
        fields=[
            Field("event_id", "Event",
                  options_sql="SELECT event_id, name FROM events ORDER BY name"),
        ],
        button="Show sessions",
        sql="""
            SELECT s.session_id, s.title, s.room, s.capacity, s.status,
                   sp.first_name || ' ' || sp.last_name AS speaker
            FROM sessions AS s
            JOIN speakers AS sp ON sp.speaker_id = s.speaker_id
            WHERE s.event_id = :event_id
            ORDER BY s.session_id
        """,
    ),

    # Student 3036716552: Refined feature - Registrations per event
    Feature(
        title="Registrations per event",
        description="Confirmed registration count for every event, with venue and dates.",
        sql="""
            SELECT e.event_id, e.name, v.name AS venue, e.start_date, e.end_date,
                   COUNT(r.registration_id) AS confirmed_registrations
            FROM events AS e
            JOIN venues AS v ON v.venue_id = e.venue_id
            LEFT JOIN registrations AS r
              ON r.event_id = e.event_id AND r.status = 'confirmed'
            GROUP BY e.event_id, e.name, v.name, e.start_date, e.end_date
            ORDER BY confirmed_registrations DESC, e.start_date, e.name
        """,
    ),

    # Student 3036716552: Refined feature - Ticket revenue by type
    Feature(
        title="Ticket revenue by type",
        description="Ticket count and total confirmed revenue for each ticket type.",
        sql="""
            SELECT ticket_type,
                   COUNT(*) AS tickets,
                   ROUND(SUM(price), 2) AS revenue,
                   ROUND(AVG(price), 2) AS average_ticket_price
            FROM registrations
            WHERE status = 'confirmed'
            GROUP BY ticket_type
            ORDER BY revenue DESC
        """,
    ),

    # Student 3036062779: Refined feature - Attendees who never registered
    Feature(
        title="Attendees who never registered",
        description="Attendees with no registration record for any event.",
        sql="""
            SELECT a.attendee_id, a.first_name, a.last_name, a.email, a.organization
            FROM attendees AS a
            WHERE NOT EXISTS (
                SELECT 1
                FROM registrations AS r
                WHERE r.attendee_id = a.attendee_id
            )
            ORDER BY a.last_name, a.first_name, a.attendee_id
        """,
    ),

    # Student 3036062779: Refined feature - Speakers by affiliation
    Feature(
        title="Speakers by affiliation",
        description="Number of speakers at each affiliation.",
        sql="""
            SELECT affiliation, COUNT(*) AS speakers
            FROM speakers
            GROUP BY affiliation
            ORDER BY speakers DESC, affiliation
        """,
    ),

    # Student 3036716552: Refined feature - Events with many registrations
    Feature(
        title="Events with many registrations",
        description="Events whose confirmed registration count exceeds a user-entered minimum.",
        fields=[
            Field("minimum", "Minimum confirmed registrations", type="number"),
        ],
        button="Show events",
        sql="""
            SELECT e.event_id, e.name, v.name AS venue, e.start_date,
                   COUNT(r.registration_id) AS confirmed_registrations
            FROM events AS e
            JOIN venues AS v ON v.venue_id = e.venue_id
            JOIN registrations AS r
              ON r.event_id = e.event_id AND r.status = 'confirmed'
            GROUP BY e.event_id, e.name, v.name, e.start_date
            HAVING COUNT(r.registration_id) > :minimum
            ORDER BY confirmed_registrations DESC, e.start_date, e.name
        """,
    ),

    # Student 3036062779: Refined feature - Full sessions
    Feature(
        title="Full sessions",
        description="Sessions marked full, with their schedule, venue, room, and speaker.",
        sql="""
            SELECT s.session_id, s.title, e.name AS event, e.start_date,
                   s.start_time, s.end_time, v.name AS venue, s.room, s.capacity,
                   sp.first_name AS speaker_first_name,
                   sp.last_name AS speaker_last_name, s.status
            FROM sessions AS s
            JOIN events AS e ON e.event_id = s.event_id
            JOIN venues AS v ON v.venue_id = e.venue_id
            JOIN speakers AS sp ON sp.speaker_id = s.speaker_id
            WHERE s.status = 'full'
            ORDER BY e.start_date, s.start_time, s.session_id
        """,
    ),

    Feature(
        title="Sessions by speaker",
        description="All sessions given by one speaker.",
        fields=[
            Field("speaker_id", "Speaker",
                  options_sql="SELECT speaker_id, first_name || ' ' || last_name FROM speakers ORDER BY last_name, first_name"),
        ],
        button="Show sessions",
        sql="""
            SELECT s.session_id, s.title, e.name AS event, s.room, s.capacity, s.status
            FROM sessions AS s
            JOIN events AS e ON e.event_id = s.event_id
            WHERE s.speaker_id = :speaker_id
            ORDER BY e.start_date, s.session_id
        """,
    ),
]
