# 🔗 URL Shortener Web Application (Flask)

A simple **URL Shortener Web Application** built using **Flask & SQLAlchemy**.

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
