# 📝 NOTEVAULT 
 - A simple NoteTakingApp 

A simple **Flask-based Note Taking Application - NOTEVAULT** where users can:

✅ Add Notes with **Title + Content**  
✅ View saved notes (Title list view)  
✅ Open a note by clicking the title  
✅ Edit notes  
✅ Delete notes  
✅ Clear all notes  
✅ Sort notes (Latest / Oldest / Title A–Z)

Notes are stored using **Flask Session** (temporary storage).

---

## 📌 Features

- Add a new note using Title + Note text
- Notes list page shows:
  - **Title**
  - **Edit** and **Delete** buttons in the same line
- Click the **title** to open the full note view
- Edit and Delete options available in the view page
- Clear all notes option
- Sort notes:
  - Latest First
  - Oldest First
  - Title (A-Z)

---

## 🗂 Project Structure

```
NOTETAKINGAPP/
│
├── app.py
├── requirements.txt
├── flask_session/ 
│ └── (session files...)
│
└── templates/
├── home.html   # add + list notes
├── view.html   # view full note content
└── edit.html   # edit note

```

---

## ⚙️ Requirements

- Python 3.x
- Flask
- Flask-Session

---
