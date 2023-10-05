from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from constants import IMAGE_DB_PATH

# Login manager
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Database and security
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    # Get base dir
    basedir = path.abspath(path.dirname(__file__))

    # Setup app
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + path.join(
        basedir, "database", "cvis.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = IMAGE_DB_PATH

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    import routes

    app.register_blueprint(routes.blue_print)

    return app
