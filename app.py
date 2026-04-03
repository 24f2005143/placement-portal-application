from flask import Flask, render_template, redirect, url_for
from models import db, User
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.company_routes import company_bp
from routes.student_routes import student_bp

from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash


def create_app():  
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(company_bp, url_prefix='/company')
    app.register_blueprint(student_bp, url_prefix='/student')

    @app.route('/')
    def home():
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'company':
                return redirect(url_for('company.dashboard'))
            elif current_user.role == 'student':
                return redirect(url_for('student.dashboard'))

        return render_template('home.html')

    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(role='admin').first()

        if not admin:
            admin_user = User(
                email='admin@portal.com',
                password=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)