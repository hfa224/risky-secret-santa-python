"""Test the index/event page"""

import os

from secret_santa.db import get_db
from secret_santa.draw import perform_draw

with open(
    os.path.join(os.path.dirname(__file__), "test_data/event_attendance.sql"), "rb"
) as f:
    _user_data_sql = f.read().decode("utf8")


def test_draw(app):
    """Test that the draw function correctly assigns giftees to users"""

    # First log in
    # auth.login()

    # Add all the event, user and event_attendance indo
    with app.app_context():
        get_db().executescript(_user_data_sql)

        # perform draw for event id
        perform_draw()

        # check in the database that everyone has a sensible giftee
        res = get_db().execute(
            "SELECT user_id, username, giftee FROM user WHERE has_joined_event = ?",
            (True,),
        )
        user_list = res.fetchall()
        assert len(user_list) != 0
        for user in user_list:
            print(user.keys())
            assert user["giftee"] is not None
            assert user["giftee"] != user["user_id"]
