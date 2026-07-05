import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200


def test_login_page(client):
    response = client.get("/login")

    assert response.status_code == 200


def test_register_page(client):
    response = client.get("/register")

    assert response.status_code == 200


def test_products_page(client):
    response = client.get("/products")

    assert response.status_code == 200


def test_upload_page(client):
    response = client.get("/upload")

    assert response.status_code == 200


def test_admin_page(client):
    response = client.get("/admin")

    assert response.status_code == 200


def test_dashboard_requires_login(client):
    response = client.get("/dashboard")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_logout_redirects_home(client):
    response = client.get("/logout")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")