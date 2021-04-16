import datetime

import jwt
from django.conf import settings

from lightning_plus.contrib.graphql.exceptions import AuthFailed


def decode_jwt(token):
    return jwt.decode(
        token, settings.SECRET_KEY, algorithms=JWT_ALGORITHM, audience=None
    )


def get_authorization_header(request):
    return request.headers.get("Authorization", None)


def get_token_auth_header(request):
    auth = get_authorization_header(request)
    if not auth:
        return None
    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise AuthFailed("Authorization header must start with bearer")
    elif len(parts) == 1:
        raise AuthFailed("Token not found")
    elif len(parts) > 2:
        raise AuthFailed("Authorization header must be" " Bearer token")

    return parts[1]


def gen_jwt_token(payload, expires=None):
    payload = {**payload}
    if expires is not NOT_EXPIRE:
        payload["exp"] = expires or datetime.datetime.utcnow() + datetime.timedelta(
            days=30
        )

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=JWT_ALGORITHM).decode()
    return token


JWT_ALGORITHM = "HS256"
NOT_EXPIRE = object()


def auth_request(request):
    try:
        token = get_token_auth_header(request)
        if not token:
            return None
        payload = decode_jwt(token)
    except jwt.ExpiredSignatureError:
        raise AuthFailed("token is expired")
    except jwt.MissingRequiredClaimError:
        raise AuthFailed("incorrect claims, please check the audience and issuer")
    except jwt.InvalidIssuerError:
        raise AuthFailed("issuer invalid")
    except jwt.InvalidAudience:
        raise AuthFailed("audience invalid")
    except jwt.InvalidTokenError:
        raise AuthFailed("Unable to parse authentication header")
    except jwt.InvalidSignatureError:
        raise AuthFailed("token secret not match")

    if payload.get("type", None) == "ADMIN":
        return 1

    if payload.get("type", None) == "KID":
        from lightning_plus.app_guaiclass.models import KidUser

        user = KidUser.get_or_404(pk=payload["user_id"])
        return user

    if payload.get("type", None) == "FACE":
        from lightning_plus.app_faceplus.models import FaceUser

        user = FaceUser.get_or_404(pk=payload["user_id"])
        return user

    return None
