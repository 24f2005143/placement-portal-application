from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Student, PlacementDrive, Application
from datetime import date

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))

    student = current_user.student_profile

    if not student:
        flash("Student profile not found.", "danger")
        return redirect(url_for('auth.login'))

    applications = Application.query.filter_by(student_id=student.id).all()

    return render_template(
        'student_dashboard.html',
        student=student,
        applications=applications
    )


@student_bp.route('/drives')
@login_required
def drives():
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))

    student = current_user.student_profile

    if not student:
        flash("Student profile missing.", "danger")
        return redirect(url_for('auth.login'))

    drives = PlacementDrive.query.filter_by(status='approved').all()
    applications = Application.query.filter_by(student_id=student.id).all()

    return render_template(
        'student_drives.html',
        drives=drives,
        applications=applications
    )


@student_bp.route('/apply/<int:drive_id>', methods=['POST'])
@login_required
def apply_drive(drive_id):
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))

    student = current_user.student_profile

    if not student:
        flash("Student profile missing.", "danger")
        return redirect(url_for('auth.login'))

    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.status != 'approved':
        flash("Drive not available.", "danger")
        return redirect(url_for('student.drives'))

    if drive.deadline and drive.deadline < date.today():
        flash("Application deadline has passed.", "danger")
        return redirect(url_for('student.drives'))

    existing = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive.id
    ).first()

    if existing:
        flash("You already applied!", "warning")
        return redirect(url_for('student.drives'))

    if drive.min_cgpa and student.cgpa:
        if student.cgpa < drive.min_cgpa:
            flash(f"Minimum CGPA required: {drive.min_cgpa}", "danger")
            return redirect(url_for('student.drives'))

    application = Application(
        student_id=student.id,
        drive_id=drive.id,
        status='applied'
    )

    db.session.add(application)
    db.session.commit()

    flash(f"Applied for {drive.title} at {drive.company.name}", "success")
    return redirect(url_for('student.drives'))


@student_bp.route('/history')
@login_required
def history():
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))

    student = current_user.student_profile

    if not student:
        flash("Student profile missing.", "danger")
        return redirect(url_for('auth.login'))

    applications = Application.query.filter_by(student_id=student.id).all()

    return render_template(
        'student_applications.html',
        applications=applications
    )