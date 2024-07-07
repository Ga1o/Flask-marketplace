from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'user_bp.login'
mail = Mail()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    from .blueprints.main_bp import main_bp as main_blueprint
    app.register_blueprint(main_blueprint)

    from .blueprints.user_bp import user_bp as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/user')

    from .blueprints.product_bp import product_bp as product_blueprint
    app.register_blueprint(product_blueprint, url_prefix='/product')

    with app.app_context():
        db.create_all()

    return app
