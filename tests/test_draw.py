"""Test the index/event page"""

import os

from secret_santa.db import get_db
from secret_santa.draw import perform_draw

with open(
    os.path.join(os.path.dirname(__file__), "test_data/event_attendance.sql"), "rb"
) as f:
    _event_data_sql = f.read().decode("utf8")


def test_draw(app):
    """Test that the event page displays the current event for a logged in user"""

    # First log in
    # auth.login()

    # Add all the event, user and event_attendance indo
    with app.app_context():
        get_db().executescript(_event_data_sql)

        # perform draw for event id
        perform_draw(1)

        # check in the database that everyone has a sensible giftee
        res = get_db().execute(
            "SELECT event_id, user_id, giftee FROM event_attendance WHERE event_id = ?",
            (1,),
        )
        event_attendance_list = res.fetchall()
        for event_attendance in event_attendance_list:
            print(event_attendance.keys())
            assert event_attendance["giftee"] is not None
            assert event_attendance["giftee"] != event_attendance["user_id"]
