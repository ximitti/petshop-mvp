from flask.app import Flask


def init_app(app: Flask):
    from .client_view import bp as bp_client
    app.register_blueprint(bp_client)
    # TODO from .your_view import bp as bp_something
    # TODO app.register_blueprint(bp_something)
    pass
