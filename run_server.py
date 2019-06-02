import os
from erpro.service.core import create_app
from erpro.config import DevConfig, TestConfig, ProdConfig


def configure_app():
    flask_env = str(os.environ.get('FLASK_ENV'))
    if flask_env == 'dev':
        return DevConfig
    elif flask_env == 'test':
        return TestConfig
    else:
        return ProdConfig


app_config = configure_app()
erpro_app = create_app(app_config)

# erpro_app.debug = True

if __name__ == '__main__':

    if str(os.environ.get('FLASK_ENV')) != 'prod':
        app_debug = True
    else:
        app_debug = False

    app_config = configure_app()
    erpro_app = create_app(app_config)

    erpro_app.debug = app_debug

    # Werkzeug, WSGI utility library for Python, enable module reloader
    erpro_app.run(use_reloader=True,
                  host=os.environ.get("HOST_IP"),
                  reloader_interval=0,
                  use_debugger=app_debug,
                  reloader_type='watchdog')