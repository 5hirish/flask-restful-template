import pytest
from foobar.service.core import create_app
from foobar.config import TestConfig


@pytest.fixture(scope="module")
def test_client():

    app_config = TestConfig
    erpro_app = create_app(app_config)

    erpro_app.debug = True

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = erpro_app.test_client()

    # Establish an application context before running the tests.
    ctx = erpro_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()
