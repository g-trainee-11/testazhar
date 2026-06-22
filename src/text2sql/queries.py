SQL_QUERIES = {
    "q1": {
        # How many students have signed up for Chess Club?
        "sql": (
            "SELECT COUNT(s.id) "
            "FROM signups s "
            "JOIN activities a ON s.activity_id = a.id "
            "WHERE a.name = %s"
        ),
        "params": ("Chess Club",),
    },
    "q2": {
        # List all activities that still have spots available.
        "sql": (
            "SELECT a.id, a.name, a.description, a.max_participants, a.schedule "
            "FROM activities a "
            "LEFT JOIN signups s ON s.activity_id = a.id "
            "GROUP BY a.id, a.name, a.description, a.max_participants, a.schedule "
            "HAVING COUNT(s.id) < a.max_participants"
        ),
        "params": (),
    },
    "q3": {
        # Which activities is student Alice Johnson signed up for?
        "sql": (
            "SELECT a.id, a.name, a.description, a.max_participants, a.schedule "
            "FROM activities a "
            "JOIN signups s ON s.activity_id = a.id "
            "WHERE s.student_name = %s"
        ),
        "params": ("Alice Johnson",),
    },
    "q4": {
        # Show activities with more than 10 max participants.
        "sql": (
            "SELECT id, name, description, max_participants, schedule "
            "FROM activities "
            "WHERE max_participants > %s"
        ),
        "params": (10,),
    },
    "q5": {
        # Remove Alice Johnson from Basketball Team.
        "sql": (
            "DELETE FROM signups "
            "WHERE student_name = %s "
            "AND activity_id = (SELECT id FROM activities WHERE name = %s)"
        ),
        "params": ("Alice Johnson", "Basketball Team"),
    },
}
