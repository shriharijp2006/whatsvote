# WhatsVote (Mini Project)

A minimal WhatsApp-style poll/voting system built with Django.

## Features
- Create polls with multiple options.
- Single-choice voting per user/session (prevents duplicate votes).
- Live-style results refresh on vote (page reload).
- Simple, clean templates.

## Quick Start
```bash
# 1) Create & activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Create Django project files
# (already included in this zip)

# 4) Apply migrations
python manage.py migrate

# 5) Create a superuser (optional, for admin)
python manage.py createsuperuser

# 6) Run the server
python manage.py runserver

# Visit http://127.0.0.1:8000/ to view polls
```

## Notes
- Default DB is SQLite (file-based). No extra setup needed.
- Time zone set to Asia/Kolkata.
- For production, turn DEBUG=False and configure ALLOWED_HOSTS.
