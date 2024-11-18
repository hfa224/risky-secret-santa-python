"""Test the index/event page"""

import os

from secret_santa.db import get_db

with open(
    os.path.join(os.path.dirname(__file__), "test_data/event_data.sql"), "rb"
) as f:
    _event_data_sql = f.read().decode("utf8")


def test_event_index(client, auth, app):
    """Test that the event page displays the current event for a logged in user"""

    # First log in
    auth.login()

    # assert there's no event
    assert client.get("/event/").status_code == 200
    response = client.get("/event/")
    assert b"There's no event running currently." in response.data

    # Then add an event
    with app.app_context():
        get_db().execute(_event_data_sql)

        assert client.get("/event/").status_code == 200
        response = client.get("/event/")
        assert b"2024-01-01" in response.data
        assert b"twenty english pounds" in response.data


def test_join_leave(client, auth, app):
    """Test that a user that hasn't joined sees the join button"""

    # First log in - by default this logs in the user "test" with id 1
    auth.login()

    # Then add an event
    with app.app_context():
        get_db().execute(_event_data_sql)

        response = client.get("/event/")
        assert response.status_code == 200
        assert b"Join" in response.data

        # use follow_redirects=True to test the redirect endpoint
        # the current event has id 2
        response = client.post("/event/join", follow_redirects=True)
        assert response.request.path == "/event/"

        response = client.get("/event/")
        print(response.data)
        assert b"Leave" in response.data

        # in future check the user can't join twice
        # response = client.post("/event/2/join", follow_redirects=True)
        # assert response.request.path == "/event/"

        # use follow_redirects=True to test the redirect endpoint
        # the current event has id 2
        response = client.post("/event/leave", follow_redirects=True)
        assert response.request.path == "/event/"

        response = client.get("/event/")
        print(response.data)
        assert b"Join" in response.data
