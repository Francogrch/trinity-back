from flask_marshmallow import Marshmallow

ma = Marshmallow()


def init_ma(app):
    ma.init_app(app)
