from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from database import db
from models import Product, User

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

        if user and check_password_hash(user.password, password):

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

        hashed_password = generate_password_hash(password)

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
@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)