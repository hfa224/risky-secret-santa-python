import pytest
from flask import g, session
from secret_santa.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a', 'email': 'email@email.com', 'address': "", 'dietary_info': ""}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'email', 'message'), (
    ('', '', 'email@gmail.com', b'Username is required.'),
    ('a', '', 'email@gmail.com',b'Password is required.'),
    ('test', 'test', 'email@gmail.com',b'already registered'),
    ('new_user', 'test', 'test@gmail.com',b'already registered')
))
def test_register_validate_input(client, username, password, email, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password, 'email': email, 'address': "", 'dietary_info': ""}
    )
    assert message in response.data
    
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data
    
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session