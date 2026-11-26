from flask import Flask
from pkg import config
from flask_migrate import Migrate
from flask_mail import Mail

mail = Mail()
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    from pkg.models import db

    app = Flask(__name__)

    app.config.from_object(config.DevelopmentConfig)

    db.init_app(app)
    from flask_wtf.csrf import CSRFProtect
    mail.init_app(app)

    csrf = CSRFProtect(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    return app


app = create_app()

from pkg import routes
