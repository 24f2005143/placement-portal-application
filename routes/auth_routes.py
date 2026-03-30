from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from models import db, User, Student, Company
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            
            if user.role == 'company':
                if not user.company or user.company.approval_status != "Approved":
                    return "Wait for admin approval"

            login_user(user)

            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))

            return "Login Successful"

        return "Invalid credentials"

    return render_template('login.html')



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth_bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        user = User(
            username=request.form.get('username'),
            password=generate_password_hash(request.form.get('password')),
            role='student'
        )
        db.session.add(user)
        db.session.commit()

        student = Student(
            user_id=user.id,
            name=request.form.get('name'),
            email=request.form.get('email')
        )
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register_student.html')



@auth_bp.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        user = User(
            username=request.form.get('username'),
            password=generate_password_hash(request.form.get('password')),
            role='company'
        )
        db.session.add(user)
        db.session.commit()

        company = Company(
            user_id=user.id,
            company_name=request.form.get('company_name'),
            email=request.form.get('email'),
            approval_status="Pending"
        )
        db.session.add(company)
        db.session.commit()

        return "Registered! Wait for Admin Approval."

    return render_template('register_company.html')