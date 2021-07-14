from flask.app import Flask


def init_app(app: Flask):
    from .petshop_view import bp as bp_petshop

    app.register_blueprint(bp_petshop)
