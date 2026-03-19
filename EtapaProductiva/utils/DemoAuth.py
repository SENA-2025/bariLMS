from flask import session


class DemoAuth:
    """Demo authentication class for EtapaProductiva prototyping.
    Provides mock users and session-based auth utilities without a real DB.
    """

    DEMO_USERS = [
        {
            "email": "admin@etapa.sena.edu.co",
            "password": "admin123",
            "name": "Admin Demo",
            "role": "Administrador",
            "dashboard_slug": "administrador",
        },
        {
            "email": "instructor@etapa.sena.edu.co",
            "password": "instructor123",
            "name": "Instructor Demo",
            "role": "Instructor",
            "dashboard_slug": "instructor",
        },
        {
            "email": "aprendiz@etapa.sena.edu.co",
            "password": "aprendiz123",
            "name": "Aprendiz Demo",
            "role": "Aprendiz",
            "dashboard_slug": "aprendiz",
        },
    ]

    ROLE_SLUGS = {
        "Administrador": "administrador",
        "Instructor": "instructor",
        "Aprendiz": "aprendiz",
    }

    @classmethod
    def validate_login(cls, email: str, password: str, role: str) -> dict | None:
        """Return the matching demo user dict or None if credentials are invalid."""
        email = email.strip().lower()
        for user in cls.DEMO_USERS:
            if (
                user["email"] == email
                and user["password"] == password
                and user["role"] == role
            ):
                return user
        return None

    @classmethod
    def get_user_by_email(cls, email: str) -> dict | None:
        """Look up a demo user by email (case-insensitive)."""
        email = email.strip().lower()
        for user in cls.DEMO_USERS:
            if user["email"] == email:
                return user
        return None

    @classmethod
    def current_user(cls) -> dict | None:
        """Return the user dict stored in the session, or None if not logged in."""
        email = session.get("pf_user_email")
        if not email:
            return None
        return cls.get_user_by_email(email)

    @classmethod
    def login_user(cls, user: dict) -> None:
        """Persist the authenticated user to the session."""
        session.clear()
        session["pf_user_email"] = user["email"]

    @classmethod
    def logout_user(cls) -> None:
        """Remove the user from the session."""
        session.clear()
