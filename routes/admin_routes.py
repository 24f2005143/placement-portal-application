from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Student, Company, PlacementDrive, Application

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    return render_template(
        'admin_dashboard.html',
        total_students=Student.query.count(),
        total_companies=Company.query.count(),
        total_drives=PlacementDrive.query.count(),
        total_applications=Application.query.count()
    )


@admin_bp.route('/students')
@login_required
def manage_students():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    query = request.args.get('q')

    if query:
        students = Student.query.filter(
            Student.full_name.ilike(f"%{query}%")
        ).all()
    else:
        students = Student.query.all()

    return render_template('admin_students.html', students=students)


@admin_bp.route('/students/<int:sid>/toggle', methods=['POST'])
@login_required
def toggle_student(sid):
    student = Student.query.get_or_404(sid)
    student.is_blacklisted = not student.is_blacklisted
    db.session.commit()
    return redirect(url_for('admin.manage_students'))


@admin_bp.route('/companies')
@login_required
def manage_companies():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    query = request.args.get('q')

    if query:
        companies = Company.query.filter(
            Company.name.ilike(f"%{query}%")
        ).all()
    else:
        companies = Company.query.all()

    return render_template('admin_companies.html', companies=companies)


@admin_bp.route('/companies/<int:cid>/update', methods=['POST'])
@login_required
def update_company(cid):
    company = Company.query.get_or_404(cid)
    action = request.form.get('action')

    if action == 'approve':
        company.approval_status = 'approved'
    elif action == 'reject':
        company.approval_status = 'rejected'

    db.session.commit()
    return redirect(url_for('admin.manage_companies'))


@admin_bp.route('/companies/<int:cid>/toggle', methods=['POST'])
@login_required
def toggle_company(cid):
    company = Company.query.get_or_404(cid)
    company.is_blacklisted = not company.is_blacklisted
    db.session.commit()
    return redirect(url_for('admin.manage_companies'))


@admin_bp.route('/drives')
@login_required
def manage_drives():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    drives = PlacementDrive.query.all()
    return render_template('admin_drives.html', drives=drives)


@admin_bp.route('/drives/<int:did>/update', methods=['POST'])
@login_required
def update_drive(did):
    drive = PlacementDrive.query.get_or_404(did)
    action = request.form.get('action')

    if action == 'approve':
        drive.status = 'approved'
    elif action == 'reject':
        drive.status = 'rejected'
    elif action == 'close':
        drive.status = 'closed'

    db.session.commit()
    return redirect(url_for('admin.manage_drives'))


@admin_bp.route('/applications')
@login_required
def view_applications():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    applications = Application.query.all()
    return render_template('admin_applications.html', applications=applications)