"""SSO token helpers shared across bariLMS and EtapaProductiva."""

import os

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

# DEFAULT SECRET USED TO SIGN TOKENS — OVERRIDE WITH THE SECRET_KEY ENV VAR IN PRODUCTION
_DEFAULT_SECRET = "bari-lms-dev-key"


def _secret() -> str:
    # READS THE SIGNING SECRET FROM THE ENVIRONMENT AT CALL TIME
    # SO CHANGES TO SECRET_KEY TAKE EFFECT WITHOUT RESTARTING
    return os.getenv("SECRET_KEY", _DEFAULT_SECRET)


def make_token(email: str) -> str:
    # GENERATES A SIGNED, TIME-STAMPED TOKEN CONTAINING THE USER'S EMAIL
    # USED BY ETAPAPRODUCTIVA TO BUILD SSO LINKS POINTING TO BARILMS
    return URLSafeTimedSerializer(_secret()).dumps({"email": email})


def read_token(token: str, max_age: int = 300) -> str | None:
    # VALIDATES A TOKEN AND RETURNS THE EMAIL INSIDE IT
    # RETURNS NONE IF THE TOKEN IS TAMPERED WITH OR OLDER THAN max_age SECONDS (DEFAULT 5 MIN)
    # USED BY BARILMS /sso ROUTE TO AUTHENTICATE INCOMING REQUESTS FROM ETAPAPRODUCTIVA
    try:
        return URLSafeTimedSerializer(_secret()).loads(token, max_age=max_age)["email"]
    except (BadSignature, SignatureExpired):
        return None
