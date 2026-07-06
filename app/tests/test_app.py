import hashlib
import io
import sys
from pathlib import Path

import pytest


APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))

import app as app_module
from database import db
from models import Product, User


@pytest.fixture
def client(tmp_path):
    flask_app = app_module.app
    flask_app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{tmp_path / 'test.db'}",
        UPLOAD_FOLDER=str(tmp_path / "uploads"),
        WTF_CSRF_ENABLED=False,
    )

    Path(flask_app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    with flask_app.app_context():
        db.create_all()
        yield flask_app.test_client()
        db.session.remove()
        db.drop_all()


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"DevSecOps" in response.data


def test_login_page(client):
    response = client.get("/login")

    assert response.status_code == 200
    assert b"Login" in response.data


def test_register_page(client):
    response = client.get("/register")

    assert response.status_code == 200
    assert b"Register" in response.data


def test_register_creates_user_with_hashed_password(client):
    response = client.post(
        "/register",
        data={
            "username": "alice",
            "email": "alice@example.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")

    user = User.query.filter_by(username="alice").one()
    assert user.email == "alice@example.com"
    assert user.password == hashlib.md5(b"Password123").hexdigest()


def test_register_rejects_duplicate_username(client):
    user = User(
        username="alice",
        email="alice@example.com",
        password=hashlib.md5(b"Password123").hexdigest(),
    )
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/register",
        data={
            "username": "alice",
            "email": "other@example.com",
            "password": "Different123",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/register")
    assert User.query.filter_by(username="alice").count() == 1


def test_login_with_valid_credentials_starts_session(client):
    user = User(
        username="alice",
        email="alice@example.com",
        password=hashlib.md5(b"Password123").hexdigest(),
    )
    db.session.add(user)
    db.session.commit()

    response = client.post(
        "/login",
        data={"username": "alice", "password": "Password123"},
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/dashboard")

    with client.session_transaction() as session:
        assert session["username"] == "alice"
        assert session["user_id"] == user.id


def test_login_with_invalid_credentials_shows_error(client):
    response = client.post(
        "/login",
        data={"username": "missing", "password": "wrong"},
    )

    assert response.status_code == 200
    assert b"Invalid username or password." in response.data


def test_dashboard_requires_login(client):
    response = client.get("/dashboard")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_dashboard_shows_logged_in_username(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "alice"

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert b"Welcome alice" in response.data


def test_logout_redirects_home_and_clears_session(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "alice"

    response = client.get("/logout")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    with client.session_transaction() as session:
        assert "user_id" not in session
        assert "username" not in session


def test_products_page_lists_products(client):
    product = Product(
        name="Laptop",
        description="Developer workstation",
        price=1299.5,
    )
    db.session.add(product)
    db.session.commit()

    response = client.get("/products")

    assert response.status_code == 200
    assert b"Laptop" in response.data
    assert b"Developer workstation" in response.data
    assert b"$1299.50" in response.data


def test_products_search_filters_results(client):
    db.session.add_all(
        [
            Product(name="Laptop", description="Developer workstation", price=1299.5),
            Product(name="Keyboard", description="Mechanical keyboard", price=99.99),
        ]
    )
    db.session.commit()

    response = client.get("/products?search=Lap")

    assert response.status_code == 200
    assert b"Laptop" in response.data
    assert b"Keyboard" not in response.data


def test_upload_page(client):
    response = client.get("/upload")

    assert response.status_code == 200
    assert b"File Upload" in response.data


def test_upload_saves_file_to_configured_upload_folder(client):
    response = client.post(
        "/upload",
        data={"file": (io.BytesIO(b"hello"), "note.txt")},
        content_type="multipart/form-data",
    )

    uploaded_file = Path(app_module.app.config["UPLOAD_FOLDER"]) / "note.txt"
    assert response.status_code == 200
    assert b"note.txt uploaded successfully." in response.data
    assert uploaded_file.read_bytes() == b"hello"


def test_uploaded_file_can_be_downloaded(client):
    upload_dir = Path(app_module.app.config["UPLOAD_FOLDER"])
    (upload_dir / "note.txt").write_text("hello", encoding="utf-8")

    response = client.get("/uploads/note.txt")

    assert response.status_code == 200
    assert response.data == b"hello"


def test_admin_page(client):
    response = client.get("/admin")

    assert response.status_code == 200
    assert b"Admin Diagnostics" in response.data


def test_admin_runs_diagnostic_command(client, monkeypatch):
    calls = []

    def fake_getoutput(command):
        calls.append(command)
        return "diagnostic output"

    monkeypatch.setattr(app_module.subprocess, "getoutput", fake_getoutput)

    response = client.post("/admin", data={"host": "example.com"})

    assert response.status_code == 200
    assert calls == ["ping -c 2 example.com"]
    assert b"diagnostic output" in response.data
