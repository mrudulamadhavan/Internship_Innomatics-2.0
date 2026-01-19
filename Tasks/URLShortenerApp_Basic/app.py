from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pyshorteners
import os
import re

app = Flask(__name__)

# ---------------- DATABASE CONFIG ----------------
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- MODEL ----------------
class Url(db.Model):
    __tablename__ = "urlshortener"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    shorter_url = db.Column(db.String(200), nullable=False)

    def __init__(self, url, shorter_url):
        self.url = url
        self.shorter_url = shorter_url

with app.app_context():
    db.create_all()

# ---------------- URL VALIDATION ----------------
url_regex = re.compile(
    r"^(?:http|ftp)s?://"
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+"
    r"(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
    r"localhost|"
    r"\d{1,3}(?:\.\d{1,3}){3})"
    r"(?::\d+)?"
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE
)

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if not url or re.match(url_regex, url) is None:
            return render_template("home.html", error=1, message="Please Enter a Valid URL!")

        existing = Url.query.filter_by(url=url).first()
        if existing:
            return render_template(
                "home.html",
                original_url=url,
                short_url=existing.shorter_url,
                error=0
            )

        try:
            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(url)
        except Exception:
            return render_template("home.html", error=1, message="URL Shortening Failed!")

        new_entry = Url(url, short_url)
        db.session.add(new_entry)
        db.session.commit()

        return render_template(
            "home.html",
            original_url=url,
            short_url=short_url,
            error=0
        )

    return render_template("home.html")


@app.route("/History")
def history_page():
    allurls = Url.query.order_by(Url.id.desc()).all()
    return render_template("history.html", allurls=allurls)


@app.route("/delete/<int:id>")
def delete(id):
    item = Url.query.get_or_404(id)
    db.session.delete(item).toggle
    db.session.commit()
    return redirect(url_for("history_page"))


if __name__ == "__main__":
    app.run(debug=True)
