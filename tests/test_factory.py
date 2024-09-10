""" Test factory create_app method """

from secret_santa import create_app


def test_config():
    """test create app with test config"""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client):
    """test hello endpoint is avilable"""
    response = client.get("/hello")
    assert response.data == b"Hello, World!"
