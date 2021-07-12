from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)
    app.db = db

    # TODO import your model here!!!  from app.models import YourModel
