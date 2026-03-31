from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models import db, Company, Drive, Application, Student

company_bp = Blueprint('company', __name__)



def company_required():
    if not current_user.is_authenticated or current_user.role != 'company':
        return False
    if current_user.company.approval_status != "Approved":
        return False
    return True



@company_bp.route('/')
@login_required
def dashboard():
    if not company_required():
        return "Access Denied / Not Approved"

    company = current_user.company

    drives = Drive.query.filter_by(company_id=company.id).all()
    applications = Application.query.join(Drive).filter(
        Drive.company_id == company.id
    ).all()

    return render_template(
        'company_dashboard.html',
        drives=drives,
        applications=applications
    )


@company_bp.route('/create_drive', methods=['GET', 'POST'])
@login_required
def create_drive():
    if not company_required():
        return "Access Denied"

    if request.method == 'POST':
        drive = Drive(
            company_id=current_user.company.id,
            job_title=request.form.get('job_title'),
            salary=request.form.get('salary'),
            status="Pending"   # Admin will approve
        )
        db.session.add(drive)
        db.session.commit()

        return redirect(url_for('company.dashboard'))

    return render_template('company_create_drive.html')


@company_bp.route('/update_drive/<int:id>/<status>')
@login_required
def update_drive(id, status):
    if not company_required():
        return "Access Denied"

    drive = Drive.query.get(id)

    if not drive or drive.company_id != current_user.company.id:
        return "Invalid Drive"

    drive.status = status  
    db.session.commit()

    return redirect(url_for('company.dashboard'))


@company_bp.route('/applications/<int:drive_id>')
@login_required
def view_applications(drive_id):
    if not company_required():
        return "Access Denied"

    drive = Drive.query.get(drive_id)

    if not drive or drive.company_id != current_user.company.id:
        return "Invalid Access"

    applications = Application.query.filter_by(drive_id=drive_id).all()

    return render_template(
        'company_applications.html',
        applications=applications,
        drive=drive
    )



@company_bp.route('/application/<int:id>/<status>')
@login_required
def update_application_status(id, status):
    if not company_required():
        return "Access Denied"

    app = Application.query.get(id)

    if not app:
        return "Application not found"

    
    if app.drive.company_id != current_user.company.id:
        return "Unauthorized"

    app.status = status  
    db.session.commit()

    return redirect(url_for('company.view_applications', drive_id=app.drive_id))



@company_bp.route('/student/<int:id>')
@login_required
def view_student(id):
    if not company_required():
        return "Access Denied"

    student = Student.query.get(id)

    if not student:
        return "Student not found"

    return render_template('student_profile.html', student=student)