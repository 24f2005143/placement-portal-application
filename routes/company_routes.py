from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Company, PlacementDrive, Application
from datetime import datetime

company_bp = Blueprint('company', __name__)

@company_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'company':
        return redirect(url_for('auth.login'))

    company = current_user.company_profile

    if not company:
        flash("Company profile missing.", "danger")
        return redirect(url_for('auth.login'))

    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    drive_data = []
    for d in drives:
        count = Application.query.filter_by(drive_id=d.id).count()
        drive_data.append({
            "drive": d,
            "count": count
        })

    return render_template(
        'company_dashboard.html',
        company=company,
        drive_data=drive_data
    )


@company_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_drive():
    if current_user.role != 'company':
        return redirect(url_for('auth.login'))

    company = current_user.company_profile

    if not company:
        flash("Company profile missing.", "danger")
        return redirect(url_for('auth.login'))

    if company.approval_status != 'approved':
        flash("You are not approved yet.", "danger")
        return redirect(url_for('company.dashboard'))

    if request.method == 'POST':
        deadline_str = request.form.get('deadline')
        deadline = None

        if deadline_str:
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()

        drive = PlacementDrive(
            company_id=company.id,
            title=request.form.get('title'),
            description=request.form.get('description'),
            eligibility=request.form.get('eligibility'),
            min_cgpa=request.form.get('min_cgpa'),
            deadline=deadline,
            status='pending'  
        )

        db.session.add(drive)
        db.session.commit()

        flash("Drive created. Waiting for admin approval.", "success")
        return redirect(url_for('company.dashboard'))

    return render_template('company_create_drive.html')


@company_bp.route('/applications/<int:drive_id>')
@login_required
def view_applications(drive_id):
    if current_user.role != 'company':
        return redirect(url_for('auth.login'))

    company = current_user.company_profile
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.company_id != company.id:
        flash("Access denied.", "danger")
        return redirect(url_for('company.dashboard'))

    applications = Application.query.filter_by(drive_id=drive.id).all()

    return render_template(
        'company_applications.html',
        drive=drive,
        applications=applications
    )


@company_bp.route('/applications/<int:app_id>/update', methods=['POST'])
@login_required
def update_status(app_id):
    if current_user.role != 'company':
        return redirect(url_for('auth.login'))

    application = Application.query.get_or_404(app_id)

    if application.drive.company_id != current_user.company_profile.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('company.dashboard'))

    new_status = request.form.get('status')

    if new_status not in ['shortlisted', 'selected', 'rejected']:
        flash("Invalid status.", "danger")
        return redirect(url_for('company.dashboard'))

    application.status = new_status
    db.session.commit()

    flash("Application status updated.", "success")
    return redirect(url_for('company.view_applications', drive_id=application.drive_id))


@company_bp.route('/edit/<int:drive_id>', methods=['GET', 'POST'])
@login_required
def edit_drive(drive_id):
    if current_user.role != 'company':
        return redirect(url_for('auth.login'))

    company = current_user.company_profile
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.company_id != company.id:
        flash("Access denied.", "danger")
        return redirect(url_for('company.dashboard'))

    if request.method == 'POST':
        drive.title = request.form.get('title')
        drive.description = request.form.get('description')
        drive.eligibility = request.form.get('eligibility')
        drive.min_cgpa = request.form.get('min_cgpa')

        deadline_str = request.form.get('deadline')
        if deadline_str:
            drive.deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()

        db.session.commit()
        flash("Drive updated.", "success")
        return redirect(url_for('company.dashboard'))

    return render_template('company_edit_drive.html', drive=drive)


@company_bp.route('/delete/<int:drive_id>', methods=['POST'])
@login_required
def delete_drive(drive_id):
    if current_user.role != 'company':
        return redirect(url_for('auth.login'))

    company = current_user.company_profile
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.company_id != company.id:
        flash("Access denied.", "danger")
        return redirect(url_for('company.dashboard'))

    db.session.delete(drive)
    db.session.commit()

    flash("Drive deleted.", "success")
    return redirect(url_for('company.dashboard'))