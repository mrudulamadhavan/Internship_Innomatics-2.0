# 🔗 URL Shortener Web Application

- *A simple **URL Shortener Web Application** built using **Flask & SQLAlchemy**.*

A URL Shortener is a web application that converts a long URL (Uniform Resource Locator) into a shorter and more manageable link. This helps users share links easily without copying long web addresses.

URL shorteners work by creating a redirect from the short URL to the original long URL. When the short URL is opened in a browser, the user is redirected automatically to the original website.

Users can:
- Enter a long URL
- Generate a shortened URL (using TinyURL API via `pyshorteners`)
- Copy the shortened URL with one click
- View all previously shortened URLs in the **History Page**
- Delete any saved URL from history

---

## 📌 Features

✅ Shorten any valid URL  
✅ URL validation (reject invalid links)  
✅ Copy shortened URL button  
✅ Save URL history in SQLite database  
✅ History page with:
- Serial number (S.No)
- Original URL
- Short URL
- Delete option  

---

## 🗂 Project Structure

```
url_shortener/
│
├── app.py
├── data.sqlite     # Auto created after running
│
├── templates/
│ ├── home.html
│ └── history.html
│
└── requirements.txt
```

---
```
requirements.txt
* Flask
* Flask-SQLAlchemy
* pyshorteners
```
