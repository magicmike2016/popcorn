from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate  # <-- 📌 Agrega esta línea
from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
jwt = JWTManager()

def create_app():
    app = Flask(__name__, template_folder='/Users/miguelleon/code/programacion-avanzada/popcorn/templates')

    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    
    # 📌 Agrega esto para habilitar Flask-Migrate
    migrate = Migrate(app, db)

    login_manager.login_view = 'auth.login_page'
    login_manager.login_message_category = 'info'

    from .models import User  # 📌 Importamos User aquí para evitar importaciones circulares

    @login_manager.user_loader
    def load_user(user_id):  # 📌 Flask-Login usa esta función para cargar el usuario
        return User.query.get(int(user_id))

    from .routes import main_bp
    from .auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
