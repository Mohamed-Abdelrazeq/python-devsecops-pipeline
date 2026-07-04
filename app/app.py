from flask import Flask, render_template

app = Flask(__name__)

app.config["SECRET_KEY"] = "CHANGE_ME_IN_PRODUCTION"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/products")
def products():
    return render_template("products.html")


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)