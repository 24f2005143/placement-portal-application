from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import db, User, Student, Company, Drive, Application

admin_bp = Blueprint('admin', __name__)



def admin_required():
    return current_user.is_authenticated and current_user.role == 'admin'



@admin_bp.route('/')
@login_required
def dashboard():
    if not admin_required():
        return "Access Denied"

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = Drive.query.count()
    total_applications = Application.query.count()

    return render_template(
        'admin/dashboard.html',
        students=total_students,
        companies=total_companies,
        drives=total_drives,
        applications=total_applications
    )



@admin_bp.route('/companies')
@login_required
def view_companies():
    if not admin_required():
        return "Access Denied"

    companies = Company.query.all()
    return render_template('admin/companies.html', companies=companies)



@admin_bp.route('/company/approve/<int:id>')
@login_required
def approve_company(id):
    if not admin_required():
        return "Access Denied"

    company = Company.query.get(id)
    if not company:
        return "Company not found"

    company.approval_status = "Approved"
    db.session.commit()

    return "Company Approved"



@admin_bp.route('/company/reject/<int:id>')
@login_required
def reject_company(id):
    if not admin_required():
        return "Access Denied"

    company = Company.query.get(id)
    if not company:
        return "Company not found"

    company.approval_status = "Rejected"
    db.session.commit()

    return "Company Rejected"


@admin_bp.route('/companies/pending')
@login_required
def pending_companies():
    if not admin_required():
        return "Access Denied"

    companies = Company.query.filter_by(approval_status="Pending").all()
    return render_template('admin/pending_companies.html', companies=companies)


@admin_bp.route('/students')
@login_required
def view_students():
    if not admin_required():
        return "Access Denied"

    students = Student.query.all()
    return render_template('admin/students.html', students=students)



@admin_bp.route('/students/search')
@login_required
def search_students():
    if not admin_required():
        return "Access Denied"

    query = request.args.get('q')

    students = Student.query.filter(
        Student.name.contains(query)
    ).all()

    return render_template('admin/students.html', students=students)



@admin_bp.route('/companies/search')
@login_required
def search_companies():
    if not admin_required():
        return "Access Denied"

    query = request.args.get('q')

    companies = Company.query.filter(
        Company.company_name.contains(query)
    ).all()

    return render_template('admin/companies.html', companies=companies)



@admin_bp.route('/student/blacklist/<int:id>')
@login_required
def blacklist_student(id):
    if not admin_required():
        return "Access Denied"

    student = Student.query.get(id)
    if not student:
        return "Student not found"

    student.is_blacklisted = True
    db.session.commit()

    return "Student Blacklisted"



@admin_bp.route('/company/blacklist/<int:id>')
@login_required
def blacklist_company(id):
    if not admin_required():
        return "Access Denied"

    company = Company.query.get(id)
    if not company:
        return "Company not found"

    company.approval_status = "Blacklisted"
    db.session.commit()

    return "Company Blacklisted"


@admin_bp.route('/drives')
@login_required
def view_drives():
    if not admin_required():
        return "Access Denied"

    drives = Drive.query.all()
    return render_template('admin/drives.html', drives=drives)



@admin_bp.route('/drive/approve/<int:id>')
@login_required
def approve_drive(id):
    if not admin_required():
        return "Access Denied"

    drive = Drive.query.get(id)
    if not drive:
        return "Drive not found"

    drive.status = "Approved"
    db.session.commit()

    return "Drive Approved"



@admin_bp.route('/drive/reject/<int:id>')
@login_required
def reject_drive(id):
    if not admin_required():
        return "Access Denied"

    drive = Drive.query.get(id)
    if not drive:
        return "Drive not found"

    drive.status = "Rejected"
    db.session.commit()

    return "Drive Rejected"



@admin_bp.route('/applications')
@login_required
def view_applications():
    if not admin_required():
        return "Access Denied"

    applications = Application.query.all()
    return render_template('admin/applications.html', applications=applications)