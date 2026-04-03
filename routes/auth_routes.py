from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, User, Student, Company
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password", "danger")
            return redirect(url_for('auth.login'))

        if user.role == 'student' and user.student_profile:
            if user.student_profile.is_blacklisted:
                flash("Your account is blocked.", "danger")
                return redirect(url_for('auth.login'))

        if user.role == 'company' and user.company_profile:
            if user.company_profile.is_blacklisted:
                flash("Your company is blocked.", "danger")
                return redirect(url_for('auth.login'))

        login_user(user)

        if user.role == 'admin':
            return redirect(url_for('admin.dashboard'))

        elif user.role == 'company':
            if user.company_profile and user.company_profile.approval_status != 'approved':
                flash("Waiting for admin approval.", "warning")
            return redirect(url_for('company.dashboard'))

        elif user.role == 'student':
            return redirect(url_for('student.dashboard'))

    return render_template('login.html')


@auth_bp.route('/register')
def register():
    return render_template('register_choice.html')


@auth_bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':

        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')
        full_name = request.form.get('full_name', '').strip()
        cgpa = request.form.get('cgpa')

        if not email or not password or not full_name:
            flash("All required fields must be filled.", "danger")
            return redirect(url_for('auth.register_student'))

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "warning")
            return redirect(url_for('auth.register_student'))

        try:
            cgpa = float(cgpa) if cgpa else None
        except ValueError:
            flash("Invalid CGPA.", "danger")
            return redirect(url_for('auth.register_student'))

        user = User(
            email=email,
            password=generate_password_hash(password),
            role='student'
        )

        db.session.add(user)
        db.session.flush()

        student = Student(
            user_id=user.id,
            full_name=full_name,
            cgpa=cgpa
        )

        db.session.add(student)
        db.session.commit()

        flash("Student registered successfully!", "success")
        return redirect(url_for('auth.login'))

    return render_template('register_student.html')


@auth_bp.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':

        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')
        company_name = request.form.get('company_name', '').strip()
        hr_contact = request.form.get('hr_contact')
        website = request.form.get('website')

        if not email or not password or not company_name:
            flash("All required fields must be filled.", "danger")
            return redirect(url_for('auth.register_company'))

        if User.query.filter_by(email=email).first():
            flash("Email already exists.", "warning")
            return redirect(url_for('auth.register_company'))

        user = User(
            email=email,
            password=generate_password_hash(password),
            role='company'
        )

        db.session.add(user)
        db.session.flush()

        company = Company(
            user_id=user.id,
            name=company_name,
            hr_contact=hr_contact,
            website=website
        )

        db.session.add(company)
        db.session.commit()

        flash("Company registered! Await admin approval.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register_company.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth.login'))