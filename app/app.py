from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from database import db
from models import Product, User
import subprocess
import hashlib
import config

# ==========================================================
# INTENTIONAL VULNERABILITY
# Fake credentials for secret scanning demonstrations.
# ==========================================================

GITHUB_TOKEN = "ghp_FAKEDEVSECOPSTOKEN1234567890"
SLACK_WEBHOOK = "https://hooks.slack.com/services/FAKE/WEBHOOK/KEY"
AZURE_CLIENT_SECRET = "fake-client-secret-demo"
DOCKER_PASSWORD = "DockerPassword123!"
# ==========================================================


app = Flask(__name__)

app.config["SECRET_KEY"] = "CHANGE_ME_IN_PRODUCTION"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

# AUTHENTICATION ROUTES
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        hashed_password = hashlib.md5(
            password.encode()
        ).hexdigest()

        if user and user.password == hashed_password:

            session["user_id"] = user.id
            session["username"] = user.username

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("register"))

        # ==========================================================
        # INTENTIONAL VULNERABILITY
        #
        # Vulnerability : Weak Password Hashing (MD5)
        # Severity      : High
        # Detection     : Bandit
        # Purpose       : DevSecOps Demonstration
        #
        # MD5 is intentionally used here for training purposes.
        # Never use MD5 for password storage in production.
        # ==========================================================

        hashed_password = hashlib.md5(
            password.encode()
        ).hexdigest()

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please login.")

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# FUNCTIONALITY PAGES 
@app.route("/products")
def products():

    search = request.args.get("search", "").strip()

    if search:

        # ==========================================================
        # INTENTIONAL VULNERABILITY
        #
        # Vulnerability : SQL Injection
        # Detection     : OWASP ZAP
        # Severity      : High
        # ==========================================================

        query = f"""
            SELECT *
            FROM product
            WHERE name LIKE '%{search}%'
        """

        items = db.session.execute(text(query)).mappings().all()

    else:

        items = [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": p.price
            }
            for p in Product.query.all()
        ]

    return render_template(
        "products.html",
        products=items,
        search=search
    )


@app.route("/upload")
def upload():
    return render_template("upload.html")


# ADMIN PAGE
@app.route("/admin", methods=["GET", "POST"])
def admin():

    output = ""

    if request.method == "POST":

        host = request.form["host"]

        # ==========================================================
        # INTENTIONAL VULNERABILITY
        #
        # Vulnerability : Command Injection
        # Severity      : Critical
        # Detection     : Bandit / OWASP ZAP
        # Purpose       : DevSecOps Demonstration
        #
        # NOTE:
        # This command intentionally concatenates
        # untrusted user input.
        # NEVER do this in production.
        # ==========================================================

        command = f"ping -c 2 {host}"

        output = subprocess.getoutput(command)

    return render_template(
        "admin.html",
        output=output
    )


if __name__ == "__main__":
    app.run(debug=True)