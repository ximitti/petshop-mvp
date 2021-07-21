from app.exc.status_unauthorized import Unauthorized


def is_admin(payload):
    if not payload.get("is_admin"):
        raise Unauthorized
    return True