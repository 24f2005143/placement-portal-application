from flask import Flask
from flask_login import LoginManager
from models import db, User
import os


from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)

   
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    
    db.init_app(app)

    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

   
    @app.route('/')
    def home():
        return "Placement Portal Running 🚀"

    
    with app.app_context():
        db.create_all()

        from werkzeug.security import generate_password_hash

        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@gmail.com",
                password=generate_password_hash("admin123"),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)