from flask.app import Flask


def init_app(app: Flask):
    # TODO from .your_view import bp as bp_something
    # TODO app.register_blueprint(bp_something)
    from .pet_view import bp as bp_pet

    app.register_blueprint(bp_pet)

    from .client_view import bp as bp_client

    app.register_blueprint(bp_client)

    from .petshop_view import bp as bp_petshop

    app.register_blueprint(bp_petshop)

    from .order_view import bp as bp_order

    app.register_blueprint(bp_order)

    from .services_view import bp as bp_service

    app.register_blueprint(bp_service)

    from .order_services_view import bp as bp_order_service

    app.register_blueprint(bp_order_service)
