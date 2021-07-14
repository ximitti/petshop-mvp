from flask.app import Flask


def init_app(app: Flask):
    # TODO from .your_view import bp as bp_something
    # TODO app.register_blueprint(bp_something)
    from .client_view import bp as bp_client
    app.register_blueprint(bp_client)


    from .petshop_view import bp as bp_petshop
    app.register_blueprint(bp_petshop)
