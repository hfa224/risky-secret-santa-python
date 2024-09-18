""" Test the index/event page """


def test_index(client, auth):
    """Test that the event page displays the current event for a logged in user """
    response = client.get("/")
    assert b"Log in" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    print(response.data)
    assert b"Log out" in response.data

def test_join(client, auth):
    """Test that a uer that hasn't joined sees the join button """
    response = client.get("/")
    assert b"Log in" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    print(response.data)
    assert b"Log out" in response.data
