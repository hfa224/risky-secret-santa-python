""" Test the index/home page """


def test_index(client, auth):
    """Test that the index page displays correct actions for
    logged in and logged out users"""
    response = client.get("/")
    assert b"Log in" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/")
    print(response.data)
    assert b"Log Out" in response.data
