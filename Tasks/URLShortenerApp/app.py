from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
import pyshorteners
import os
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = "super_secret_key_advanced"

# ---------------- DATABASE CONFIG ----------------
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- LOGIN MANAGER ----------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ---------------- MODELS ----------------
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


class Url(db.Model):
    __tablename__ = "urlshortener"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    shorter_url = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# Flask 3.x compatible create
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- URL VALIDATION ----------------
def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ["http", "https"] and parsed.netloc != ""
    except:
        return False


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Username length check (5 to 9)
        if len(username) < 5 or len(username) > 9:
            flash("Username must be between 5 to 9 characters long", "danger")
            return redirect(url_for("signup"))

        # Unique username check
        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("This username already exists…", "danger")
            return redirect(url_for("signup"))

        if not password:
            flash("Password cannot be empty!", "danger")
            return redirect(url_for("signup"))

        new_user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Signup successful! Please login now.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid username or password!", "danger")
            return redirect(url_for("login"))

        login_user(user)
        flash("Login successful!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    shorter = ""

    # POST = shorten URL
    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if not url:
            flash("Please enter a URL!", "danger")
            return redirect(url_for("dashboard"))

        if not is_valid_url(url):
            flash("Please enter a valid URL with http:// or https://", "danger")
            return redirect(url_for("dashboard"))

        existing = Url.query.filter_by(url=url, user_id=current_user.id).first()
        if existing:
            shorter = existing.shorter_url
            flash("URL already shortened! Showing saved result.", "info")
        else:
            try:
                s = pyshorteners.Shortener()
                shorter = s.tinyurl.short(url)

                new_entry = Url(url=url, shorter_url=shorter, user_id=current_user.id)
                db.session.add(new_entry)
                db.session.commit()

                flash("URL shortened successfully!", "success")
            except Exception:
                flash("TinyURL service error! Try again later.", "danger")

    # GET = history pagination (5 per page)
    page = request.args.get("page", 1, type=int)

    history = Url.query.filter_by(user_id=current_user.id) \
        .order_by(Url.id.desc()) \
        .paginate(page=page, per_page=5)

    return render_template(
        "dashboard.html",
        shorter=shorter,
        history=history,
        username=current_user.username
    )


@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_url(id):
    row = Url.query.get_or_404(id)

    if row.user_id != current_user.id:
        flash("Unauthorized action!", "danger")
        return redirect(url_for("dashboard"))

    db.session.delete(row)
    db.session.commit()
    flash("URL deleted successfully!", "warning")
    return redirect(url_for("dashboard"))


@app.route("/clear_all", methods=["POST"])
@login_required
def clear_all():
    Url.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    flash("All history cleared!", "danger")
    return redirect(url_for("dashboard"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
