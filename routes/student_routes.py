from flask import Blueprint
from flask_login import login_required, current_user

student_bp = Blueprint('student', __name__)


@student_bp.route('/')
@login_required
def dashboard():
    if current_user.role != 'student':
        return "Access Denied"

    return "Student Dashboard"