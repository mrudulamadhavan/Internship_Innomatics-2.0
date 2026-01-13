from flask import Flask, request, render_template
import re

app = Flask(__name__)

# -------------------------------------------------------
# HELPER FUNCTIONS

def build_flags(form):
    """Only 2 flags: IGNORECASE and MULTILINE"""
    flags = 0
    if form.get("ignorecase"):
        flags |= re.IGNORECASE
    if form.get("multiline"):
        flags |= re.MULTILINE
    return flags


def highlight_matches(text, matches):
    """Highlight matched portions using <mark>"""
    if not matches:
        return text.replace("<", "&lt;").replace(">", "&gt;")

    result = []
    last_index = 0

    for m in matches:
        start, end = m.start(), m.end()

        normal_part = text[last_index:start].replace("<", "&lt;").replace(">", "&gt;")
        match_part = text[start:end].replace("<", "&lt;").replace(">", "&gt;")

        result.append(normal_part)
        result.append(f"<mark>{match_part}</mark>")
        last_index = end

    remaining = text[last_index:].replace("<", "&lt;").replace(">", "&gt;")
    result.append(remaining)

    return "".join(result)

# ------------------------------------------
# Routes

@app.route("/", methods=["GET"])
def home():
    return render_template("query.html")


@app.route("/result", methods=["POST"])
def result():
    regex_pattern = request.form.get("regex", "").strip()
    test_string = request.form.get("string", "")

    ignorecase = bool(request.form.get("ignorecase"))
    multiline = bool(request.form.get("multiline"))

    matches_data = []
    highlighted = ""
    error_msg = None

    if not regex_pattern:
        error_msg = "Please enter a regex pattern!"
        return render_template(
            "result.html",
            error=error_msg,
            regex=regex_pattern,
            string=test_string,
            matches=[],
            count=0,
            highlighted="",
            ignorecase=ignorecase,
            multiline=multiline
        )

    try:
        flags = build_flags(request.form)
        compiled = re.compile(regex_pattern, flags)
        matches = list(compiled.finditer(test_string))

        for idx, m in enumerate(matches, start=1):
            groups = []
            if m.groups():
                for gi, gval in enumerate(m.groups(), start=1):
                    groups.append({"group_no": gi, "value": gval})

            matches_data.append({
                "no": idx,
                "text": m.group(),
                "start": m.start(),
                "end": m.end(),
                "groups": groups
            })

        highlighted = highlight_matches(test_string, matches)

    except re.error as e:
        error_msg = f"Invalid Regex ❌ : {str(e)}"

    return render_template(
        "result.html",
        regex=regex_pattern,
        string=test_string,
        matches=matches_data,
        count=len(matches_data),
        highlighted=highlighted,
        error=error_msg,
        ignorecase=ignorecase,
        multiline=multiline
    )

if __name__ == "__main__":
    print("🚀 Regex Matcher Application Running...")
    print("👉 Open: http://127.0.0.1:5000/")
    app.run(debug=True)

