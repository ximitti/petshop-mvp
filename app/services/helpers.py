from . import db
from app.exc import InvalidKeysError, Unauthorized


def is_admin(payload):
    if not payload.get("is_admin"):
        raise Unauthorized


def add_commit(model: db.Model):

    db.session.add(model)
    db.session.commit()


def delete_commit(model: db.Model):

    db.session.delete(model)
    db.session.commit()


def check_valid_keys(data, valid_keys):

    for key in data.keys():
        if key not in valid_keys:
            return True
