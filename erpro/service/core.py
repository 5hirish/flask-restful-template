import logging
import os

from flask import Flask, jsonify
from datetime import datetime

from erpro.config import ProdConfig
from erpro.service.extensions import migrate, db

app_name = 'erpro'


def create_app(config_object=ProdConfig, enable_blueprints=True):

    app = Flask(__name__)

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

    db.init_app(app)
    migrate.init_app(app, db)

    return None


def register_blueprints(app):

    # defer the import until it is really needed
    from erpro.service.product.views import product_blueprint

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
            return jsonify({"status": "failure", "text": "API request not found :("}), 200
        elif error_code == 405:
            return jsonify({"status": "failure", "text": "API request method is not allowed :/"}), 200
        elif error_code == 500:
            return jsonify({"status": "failure", "text": "Something went wrong with this API request X("}), 200
    for errcode in [404, 405, 500]:
        app.errorhandler(errcode)(return_error)
    return None


def register_route(app):

    # done by using alembic migrations
    # @app.before_first_request
    # def create_tables():
    #     # will not attempt to recreate tables already present in the target database.
    #     db.create_all()

    @app.before_first_request
    def first_request_tasks():
        pass

    @app.route('/', methods=['GET'])
    def init_api():
        return jsonify(
            {
                "name": "ERPRO",
                "time": datetime.utcnow(),
                "developer": "5hirish",
                "website": "www.5hirish.com",
                "blog": "www.shirishkadam.com"
            }
        )


def register_logger(app):

    gunicorn_logger = logging.getLogger('gunicorn.error')

    log_dir = "logs/"
    # create file handler which logs even debug messages
    os.makedirs(os.path.dirname(log_dir), exist_ok=True)

    fh = logging.FileHandler(os.path.join(log_dir, 'erpro.log'))

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