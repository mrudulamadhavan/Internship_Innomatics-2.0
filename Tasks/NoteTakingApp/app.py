from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from uuid import uuid4

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def home():
    session.setdefault("notes", [])

    # Add Note
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("note", "").strip()

        if title and content:
            session["notes"].append({
                "id": str(uuid4()),
                "title": title,
                "content": content
            })
            session.modified = True

        return redirect(url_for("home"))

    # Sorting
    sort_by = request.args.get("sort", "latest")
    notes = session["notes"].copy()

    if sort_by == "oldest":
        pass
    elif sort_by == "title":
        notes.sort(key=lambda x: x["title"].lower())
    else:
        notes.reverse()  # latest first

    return render_template("home.html", notes=notes, sort_by=sort_by)


@app.route("/view/<note_id>")
def view_note(note_id):
    session.setdefault("notes", [])

    note = next((n for n in session["notes"] if n["id"] == note_id), None)
    if note is None:
        return redirect(url_for("home"))

    return render_template("view.html", note=note)


@app.route("/edit/<note_id>", methods=["GET", "POST"])
def edit_note(note_id):
    session.setdefault("notes", [])

    note = next((n for n in session["notes"] if n["id"] == note_id), None)
    if note is None:
        return redirect(url_for("home"))

    if request.method == "POST":
        new_title = request.form.get("title", "").strip()
        new_content = request.form.get("note", "").strip()

        if new_title and new_content:
            note["title"] = new_title
            note["content"] = new_content
            session.modified = True

        return redirect(url_for("view_note", note_id=note_id))

    return render_template("edit.html", note=note)


@app.route("/delete/<note_id>", methods=["POST"])
def delete_note(note_id):
    session.setdefault("notes", [])

    session["notes"] = [n for n in session["notes"] if n["id"] != note_id]
    session.modified = True

    return redirect(url_for("home"))


@app.route("/clear", methods=["POST"])
def clear_notes():
    session["notes"] = []
    session.modified = True
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
