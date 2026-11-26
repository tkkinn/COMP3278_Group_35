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

    Feature(
        title="Registrations per event",
        description="How many registrations each event has.",
        sql="""
            SELECT e.event_id, e.name, COUNT(r.registration_id) AS registrations
            FROM events AS e
            LEFT JOIN registrations AS r ON r.event_id = e.event_id
            GROUP BY e.event_id, e.name
            ORDER BY registrations DESC, e.name
        """,
    ),

    Feature(
        title="Ticket revenue by type",
        description="Total confirmed ticket revenue for each ticket type.",
        sql="""
            SELECT ticket_type, COUNT(*) AS tickets, SUM(price) AS revenue
            FROM registrations
            WHERE status = 'confirmed'
            GROUP BY ticket_type
            ORDER BY revenue DESC
        """,
    ),

    Feature(
        title="Attendees who never registered",
        description="People in the attendee list with no registration.",
        sql="""
            SELECT attendee_id, first_name || ' ' || last_name AS name, email, organization
            FROM attendees
            WHERE attendee_id NOT IN (SELECT attendee_id FROM registrations)
            ORDER BY last_name, first_name
        """,
    ),

    Feature(
        title="Speakers by affiliation",
        description="How many speakers each organization has.",
        sql="""
            SELECT affiliation, COUNT(*) AS speakers
            FROM speakers
            GROUP BY affiliation
            ORDER BY speakers DESC, affiliation
        """,
    ),

    Feature(
        title="Events with many registrations",
        description="Events with more than a given number of registrations.",
        fields=[
            Field("minimum", "More than (registrations)", type="number"),
        ],
        button="Show events",
        sql="""
            SELECT e.event_id, e.name, COUNT(r.registration_id) AS registrations
            FROM events AS e
            JOIN registrations AS r ON r.event_id = e.event_id
            GROUP BY e.event_id, e.name
            HAVING COUNT(r.registration_id) > :minimum
            ORDER BY registrations DESC
        """,
    ),

    Feature(
        title="Full sessions",
        description="Sessions currently marked full.",
        sql="""
            SELECT s.session_id, s.title, e.name AS event, s.room, s.capacity, s.status
            FROM sessions AS s
            JOIN events AS e ON e.event_id = s.event_id
            WHERE s.status = 'full'
            ORDER BY e.start_date, s.session_id
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
