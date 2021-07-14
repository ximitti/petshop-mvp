from flask.app import Flask


def init_app(app: Flask):
    # TODO from .your_view import bp as bp_something
    # TODO app.register_blueprint(bp_something)
    from .pet_view import bp as bp_pet
    app.register_blueprint(bp_pet)