import os
from foobar.service.core import create_app
from foobar.config import get_config

app_config = get_config()
foobar_app = create_app(app_config)

# erpro_app.debug = True

if __name__ == '__main__':

    if str(os.environ.get('FLASK_ENV')) != 'prod':
        app_debug = True
    else:
        app_debug = False

    app_config = configure_app()
    foobar_app = create_app(app_config)

    foobar_app.debug = app_debug

    # Werkzeug, WSGI utility library for Python, enable module reloader
    foobar_app.run(use_reloader=True,
                   host="0.0.0.0",
                   reloader_interval=0,
                   use_debugger=app_debug,
                   reloader_type='watchdog')
