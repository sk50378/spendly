import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_login_valid_credentials_redirects_to_landing(client):
    response = client.post(
        "/login",
        data={"email": "demo@spendly.com", "password": "demo123"},
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
    with client.session_transaction() as sess:
        assert sess.get("user_id") is not None
        assert sess.get("user_name") == "Demo User"


def test_login_wrong_password_shows_generic_error(client):
    response = client.post(
        "/login",
        data={"email": "demo@spendly.com", "password": "wrong-password"},
    )
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_login_unknown_email_shows_same_generic_error(client):
    response = client.post(
        "/login",
        data={"email": "nobody@nowhere.com", "password": "whatever123"},
    )
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_login_blank_fields_shows_validation_error(client):
    response = client.post("/login", data={"email": "", "password": ""})
    assert response.status_code == 200
    assert b"required" in response.data.lower()


def test_logout_clears_session_and_redirects_to_login(client):
    client.post(
        "/login",
        data={"email": "demo@spendly.com", "password": "demo123"},
    )
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_logout_while_logged_out_does_not_crash(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_nav_shows_login_links_when_logged_out(client):
    response = client.get("/")
    assert b"Sign in" in response.data
    assert b"Log out" not in response.data


def test_nav_shows_username_and_logout_link_when_logged_in(client):
    client.post(
        "/login",
        data={"email": "demo@spendly.com", "password": "demo123"},
    )
    response = client.get("/")
    assert b"Demo User" in response.data
    assert b"Log out" in response.data
    assert b"Sign in" not in response.data
