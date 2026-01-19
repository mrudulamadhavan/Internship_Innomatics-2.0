# 🔗 URL Shortener Web Application

## 📌 Project Overview
This is an **advanced version of URL Shortener Web Application** built using:
- **Frontend:** HTML, CSS, Bootstrap 5
- **Backend:** Flask (Python)
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Authentication:** Flask-Login + Werkzeug password hashing
- **Shortener Service:** TinyURL (via `pyshorteners`)

Users can **Signup → Login → Shorten URLs → Copy shortened URL → View history** (with pagination + search).

---

## 🎯 Objectives
✔ Shorten long URLs  
✔ Save URLs per user account  
✔ Copy shortened URL with one click  
✔ View saved URL history  
✔ Delete specific URL history items  
✔ Clear all history for a user  

---

## 🧩 Features
### ✅ Authentication
- Signup with:
  - Unique username
  - Username length must be **5 to 9**
- Login with password verification
- Logout

### ✅ URL Shortening
- Enter long URL
- URL validation (must start with **http:// or https://**)
- Generates short URL using TinyURL
- Saves original + short URL in database

### ✅ History Management
- History opens **only when clicked** (Show/Hide toggle)
- Search box to filter URLs (current page)
- Pagination: **5 URLs per page**
- Delete URL entry
- Clear all history

---

## 📂 Project Structure
```
url_shortener_app/
│── app.py
│── requirements.txt
│
└── templates/
│── home.html
│── signup.html
│── login.html
│── dashboard.html

```
