from . import db


def create_app():
    from clustering_outliers import app
    return app.app
