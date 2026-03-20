from flask import session

from shared_auth.users import DEMO_USERS, SESSION_KEY, get_by_email, validate


class DemoAuth:
    DEMO_USERS = DEMO_USERS

    @classmethod
    def validate_login(cls, email: str, password: str, role: str) -> dict | None:
        return validate(email, password, role)

    @classmethod
    def current_user(cls) -> dict | None:
        return get_by_email(session.get(SESSION_KEY))

    @classmethod
    def login_user(cls, user: dict) -> None:
        session.clear()
        session[SESSION_KEY] = user["email"]

    @classmethod
    def logout_user(cls) -> None:
        session.clear()
