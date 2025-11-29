from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    cors.init_app(app)

    from app.routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    from app.routes.users import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
