# Admission Intelligence — AI-Based Student Admission Prediction System

A multi-page, enterprise-styled web application that predicts a student's
admission probability using a trained machine learning model, and logs
every prediction to a real SQL database.

---

## What's Different From a Basic Demo

- **Three separate pages**, not one form dumped on a page: a landing
  page (with your name and an animated hero), a prediction dashboard,
  and a history page.
- **Real trained ML model** (Random Forest, scikit-learn) — every
  prediction is computed live by the model, not hardcoded.
- **Real SQL database** (SQLite) — every prediction is written to a
  `predictions` table and can be reviewed on the History page. This is
  genuine persistent backend behaviour, not a stateless demo.
- **Enterprise dark theme** — custom design system (colors, typography,
  animated SVG gauge, animated network canvas on the landing page),
  not a default template.
- **All code comments in English.**

---

## How to Run

```bash
pip install -r requirements.txt
python generate_dataset.py
python train_model.py
python app.py
```

Open your browser at:
```
http://127.0.0.1:5000
```

You'll land on the branded homepage first — click **"Launch Predictor"**
to reach the dashboard.

---

## Project Structure

```
admission-predictor-v2/
├── generate_dataset.py   # creates a synthetic training dataset
├── train_model.py        # trains and saves the Random Forest model
├── database.py           # SQLite setup + prediction logging
├── app.py                # Flask app: pages + API routes
├── templates/
│   ├── landing.html       # branded homepage with animated hero
│   ├── dashboard.html      # prediction form + result panel
│   └── history.html        # prediction log table
├── static/
│   ├── css/style.css        # full design system
│   └── js/
│       ├── landing.js        # network animation
│       ├── dashboard.js       # form logic + gauge animation
│       └── history.js          # history table rendering
├── requirements.txt
├── Procfile               # for deployment (Render, etc.)
└── .gitignore
```

---

## How It Works (for your presentation)

**1. Landing page (`landing.html` + `landing.js`)**
A branded entry point with an animated canvas background (a network of
connected nodes, representing data points feeding into a model) and your
name displayed as the developer credit.

**2. Dashboard (`dashboard.html` + `dashboard.js`)**
The student profile form posts to `/api/predict`. The backend runs the
trained Random Forest model, computes a probability, and returns it.
The frontend animates an SVG arc gauge to show the result, along with a
breakdown of which factors influenced the prediction most (the model's
feature importances).

**3. Persistence (`database.py`)**
Every prediction — inputs and result — is inserted into a SQLite table
called `predictions`. This is what makes the system stateful: it
remembers every prediction it has ever made.

**4. History (`history.html` + `history.js`)**
Reads the `predictions` table via `/api/history` and displays it as a
table, newest first — a genuine audit trail of the system's usage.

**5. Backend (`app.py`)**
Flask serves the three pages and exposes three JSON API endpoints:
`/api/predict`, `/api/history`, `/api/stats`.

---

## Deploying (to get a live link)

1. Push this project to GitHub.
2. Create a free account on [render.com](https://render.com).
3. New → Web Service → connect your GitHub repo.
4. Build command: `pip install -r requirements.txt`
5. Start command:
   ```
   python generate_dataset.py && python train_model.py && python database.py && gunicorn app:app --bind 0.0.0.0:$PORT
   ```
6. Deploy — you'll get a public `https://your-app.onrender.com` link.

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML Model | Python, scikit-learn (Random Forest) |
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript (custom design system, no template kit) |
| Deployment | Render (via Procfile + gunicorn) |
