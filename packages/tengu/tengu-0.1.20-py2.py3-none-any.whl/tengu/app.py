from .factory import FlaskFactory
from .models import db


def get_app():
    factory = FlaskFactory()
    app = factory.initiallize_flask(db)  # , blueprint_dicts)
    return app
