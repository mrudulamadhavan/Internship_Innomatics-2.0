## Username Converter Application using Flask

from flask import Flask, request
from datetime import datetime
import re
import random

app = Flask(__name__)

# =========================================================

VOWELS = set("aeiouAEIOU")

COMPLIMENTS = [
    "You're amazing! 🌟",
    "You have great potential! 🚀",
    "Keep shining ✨",
    "You're unstoppable 💪",
    "Great job! 🔥",
    "You're doing fantastic! ⭐",
    "Amazing work! 🎉",
    "You're a star! ⭐"
]


# =========================================================
# Helper Functions 

def get_greeting():
    """Return greeting based on time of day"""
    hour = datetime.now().hour
    if hour < 12:
        return "Good Morning ☀️"
    elif hour < 18:
        return "Good Afternoon 🌤️"
    return "Good Evening 🌙"


def get_compliment():
    """Return a random compliment"""
    return random.choice(COMPLIMENTS)


def count_vowels_consonants(text: str):
    """Count vowels and consonants (only alphabets)"""
    vowels = 0
    consonants = 0
    for ch in text:
        if ch.isalpha():
            if ch in VOWELS:
                vowels += 1
            else:
                consonants += 1
    return vowels, consonants


def alternate_case(text: str):
    """Convert string to alternate case (aBcDeF)"""
    return "".join(
        char.upper() if i % 2 == 0 else char.lower()
        for i, char in enumerate(text)
    )


def contains_numbers(text: str):
    """Check if text contains digits"""
    return bool(re.search(r"\d", text))


def letter_count(text: str):
    """Count only letters (A-Z)"""
    return len(re.findall(r"[a-zA-Z]", text))


def build_report(username: str):
    """Build transformation + stats report"""
    vowels, consonants = count_vowels_consonants(username)

    transformations = {
        "Original Name": username,
        "Name in Uppercase": username.upper(),
        "Name in Lowercase": username.lower(),
        "Name in Reversed Order": username[::-1],
        "Alternate Case": alternate_case(username),
    }

    stats = {
        "Name Length (All Characters)": len(username),
        "Letter Count (Only A-Z)": letter_count(username),
        "Word Count": len(username.split()),
        "Vowels Count": vowels,
        "Consonants Count": consonants,
        "Name with Numbers?": "Yes ✅" if contains_numbers(username) else "No ❌"
        
    }

    return transformations, stats


# =========================================================
def render_home():
    """Home page (input form)"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Username Converter Application</title>
        <style>
            body{
                font-family: Arial, sans-serif;
                background: #eef2f7;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
                margin:0;
            }
            .card{
                width:420px;
                background:white;
                padding:25px;
                border-radius:15px;
                box-shadow:0px 6px 18px rgba(0,0,0,0.15);
                text-align:center;
            }
            input{
                width:90%;
                padding:12px;
                border-radius:10px;
                border:2px solid #ddd;
                font-size:16px;
            }
            button{
                margin-top:12px;
                padding:12px 18px;
                border:none;
                border-radius:10px;
                background:#2563eb;
                color:white;
                font-size:16px;
                font-weight:bold;
                cursor:pointer;
            }
            button:hover{opacity:0.9;}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>🚀 Username Converter Application </h2>
            
            <form action="/" method="GET">
                <input type="text" name="name" placeholder="Enter your name" required>
                <br>
                <button type="submit">Generate Report 📋</button>
            </form>
        </div>
    </body>
    </html>
    """


def make_table(title, data):
    """Reusable HTML table maker"""
    rows = ""
    for k, v in data.items():
        rows += f"""
        <tr>
            <td style="font-weight:bold; color:#374151; padding:10px; width:45%;">{k}</td>
            <td style="color:#111827; padding:10px;">{v}</td>
        </tr>
        """
    return f"""
    <div style="background:white; padding:18px; border-radius:14px;
                box-shadow:0px 6px 18px rgba(0,0,0,0.15); margin-top:15px;">
        <h3 style="text-align:center; margin-top:0;">{title}</h3>
        <table style="width:100%; border-collapse:collapse;">
            {rows}
        </table>
    </div>
    """


def render_result(username, transformations, stats):
    """Result page (tables + try another at END)"""
    greeting = get_greeting()
    compliment = get_compliment()

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Report</title>
        <style>
            body{{
                font-family: Arial, sans-serif;
                background: linear-gradient(to right,#74ebd5,#acb6e5);
                margin:0;
                padding:25px;
            }}
            .wrap{{
                max-width:900px;
                margin:auto;
            }}
            .top{{
                background:white;
                padding:18px;
                border-radius:14px;
                text-align:center;
                box-shadow:0px 6px 18px rgba(0,0,0,0.15);
            }}
            .btn{{
                display:block;
                width:200px;
                margin:25px auto 0;
                text-align:center;
                padding:12px 16px;
                background:#22c55e;
                color:white;
                text-decoration:none;
                border-radius:10px;
                font-weight:bold;
            }}
            .btn:hover{{
                opacity:0.9;
            }}
        </style>
    </head>
    <body>
        <div class="wrap">
            <div class="top">
                <h2>{greeting} , {username}..... 👋</h2>
            </div>

            {make_table(" ✨ Transformations ✨", transformations)}
            {make_table("📊 Statistics", stats)}

            <p style="font-weight:bold; color:#ef4444;">{compliment}</p>

            <a class="btn" href="/"> Try Another Username 🔁</a>
        </div>
    </body>
    </html>
    """

# Route
@app.route("/", methods=["GET"])
def home():
    username = request.args.get("name", "").strip()

    if not username:
        return render_home()

    transformations, stats = build_report(username)
    return render_result(username, transformations, stats)


# =========================================================

if __name__ == "__main__":
    print("\n🚀 Username Converter Application \n")
    print("Open the browser 🌐 : http://127.0.0.1:5000/")
    app.run(debug=True, host="0.0.0.0", port=5000)
