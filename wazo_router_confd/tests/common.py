from tempfile import NamedTemporaryFile

from starlette.testclient import TestClient

from wazo_router_confd.app import get_app
from functools import wraps


def get_app_and_client(f):
    @wraps(f)
    def wrapper(*args, **kw):
        with NamedTemporaryFile(suffix=".db") as tmp:
            config = dict(database_uri='sqlite:///' + tmp.name, database_upgrade=True)
            app = get_app(config)
            client = TestClient(app)
            return f(*args, app=app, client=client, **kw)

    return wrapper
