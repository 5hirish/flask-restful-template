import logging
import os

from flask import Flask, jsonify
from datetime import datetime
from flask_restplus import Resource

from foobar.config import ProdConfig
from foobar.service.extensions import api, migrate, sql_db

app_name = 'foobar'
contact_address = 'mail@5hirish.com'
description = 'A flask API server template with Unit Tests, Swagger documentation, ' \
              'ORMs, ORM Migrations, Docker and Kubernetes.'


def create_app(config_object=ProdConfig, enable_blueprints=True):

    app = Flask(app_name)

    app.config.from_object(config_object)
    register_extensions(app)

    if enable_blueprints:
        register_blueprints(app)

    register_error_handlers(app)
    register_route(app)

    if enable_blueprints:
        register_logger(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""

    api.init_app(app, title="Flask Template APIs", description=description, contact_email=contact_address)
    sql_db.init_app(app)
    migrate.init_app(app, sql_db)

    return None


def register_blueprints(app):

    # defer the import until it is really needed
    from foobar.service.products.views import product_blueprint

    """Register Flask blueprints."""
    app.register_blueprint(product_blueprint)

    return None


def register_error_handlers(app):
    """Register error handlers."""
    def return_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        if error_code == 404:
            return jsonify({"status": "failure", "text": "API request not found :("}), error_code
        elif error_code == 405:
            return jsonify({"status": "failure", "text": "API request method is not allowed :/"}), error_code
        elif error_code == 500:
            return jsonify({"status": "failure", "text": "Something went wrong with this API request X("}), error_code
    for errcode in [404, 405, 500]:
        app.errorhandler(errcode)(return_error)
    return None


def register_route(app):

    # done by using alembic migrations
    @app.before_first_request
    def create_tables():
        # will not attempt to recreate tables already present in the target database.
        sql_db.create_all()

    @api.route('/about')
    class InitApp(Resource):
        def get(self):
            """Root API"""
            return {
                "name": "FooBar",
                "time": datetime.utcnow(),
                "developer": "5hirish",
                "website": "www.5hirish.com",
                "blog": "www.shirishkadam.com"
            }


def register_logger(app):

    gunicorn_logger = logging.getLogger('gunicorn.error')

    log_dir = "logs/"
    # create file handler which logs even debug messages
    os.makedirs(os.path.dirname(log_dir), exist_ok=True)

    fh = logging.FileHandler(os.path.join(log_dir, 'foobar.log'))

    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    app.logger.addHandler(ch)
    app.logger.addHandler(fh)
    app.logger.addHandler(gunicorn_logger)