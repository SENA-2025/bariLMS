"""Single source of truth for demo users shared across bariLMS and EtapaProductiva."""

# SINGLE LIST OF DEMO USERS USED BY BOTH APPS — ADD OR REMOVE USERS HERE ONLY
DEMO_USERS = [
    {
        "email": "admin@senalearn.edu.co",
        "password": "Admin123*",
        "role": "Administrador",
        "name": "Laura Moreno",
        "dashboard_slug": "administrador",  # SLUG USED TO RESOLVE THE ROLE DASHBOARD
        "active": 1,
    },
    {
        "email": "administrativo@senalearn.edu.co",
        "password": "Adminvo123*",
        "role": "Administrativo",
        "name": "Carlos Ruiz",
        "dashboard_slug": "administrativo",
        "active": 1,
    },
    {
        "email": "instructor@senalearn.edu.co",
        "password": "Instructor123*",
        "role": "Instructor",
        "name": "Diana Beltran",
        "dashboard_slug": "instructor",
        "active": 1,
    },
    {
        "email": "aprendiz@senalearn.edu.co",
        "password": "Aprendiz123*",
        "role": "Aprendiz",
        "name": "Miguel Torres",
        "dashboard_slug": "aprendiz",
        "active": 1,
    },
]

# KEY USED TO STORE THE LOGGED-IN USER'S EMAIL IN THE FLASK SESSION
# BOTH APPS MUST READ AND WRITE THIS SAME KEY
SESSION_KEY = "user_email"


def get_by_email(email: str) -> dict | None:
    # LOOKS UP A USER BY EMAIL (CASE-INSENSITIVE) — RETURNS THE USER DICT OR NONE
    if not email:
        return None
    email = email.strip().lower()
    return next((u for u in DEMO_USERS if u["email"].lower() == email), None)


def validate(email: str, password: str, role: str) -> dict | None:
    # VALIDATES LOGIN CREDENTIALS AGAINST THE DEMO USER LIST
    # RETURNS THE MATCHING USER DICT IF ALL THREE FIELDS MATCH, OTHERWISE NONE
    user = get_by_email(email)
    if user and user["password"] == password and user["role"] == role:
        return user
    return None
