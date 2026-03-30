from flask import Flask, render_template, redirect, request, url_for
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models import db, User, Student, Company
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



with app.app_context():
    db.create_all()

    
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@gmail.com",
            password="admin123",
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        



@app.route('/')
def home():
    return "Placement Portal Running "



@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    
    if request.method == 'POST':
        user = User(
            username=request.form.get('username'),
            password = generate_password_hash(request.form.get('password')),
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

        return redirect(url_for('login'))

    return render_template('register_student.html')



@app.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        user = User(
            username=request.form.get('username'),
            password = generate_password_hash(request.form.get('password')),
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



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(
            username=request.form.get('username'),
            password = generate_password_hash(request.form.get('password'))
        ).first()

        if user:
            
            if user.role == 'company':
                if not user.company or user.company.approval_status != "Approved":
                    return "Wait for admin approval"

            login_user(user)

            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'company':
                return redirect(url_for('company_dashboard'))

        return "Invalid credentials"

    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return "Access Denied"
    return "Admin Dashboard"


@app.route('/student')
@login_required
def student_dashboard():
    if current_user.role != 'student':
        return "Access Denied"
    return "Student Dashboard"


@app.route('/company')
@login_required
def company_dashboard():
    if current_user.role != 'company':
        return "Access Denied"
    return "Company Dashboard"



@app.route('/admin/approve_company/<int:id>')
@login_required
def approve_company(id):
    if current_user.role != 'admin':
        return "Access Denied"

    company = Company.query.get(id)
    company.approval_status = "Approved"
    db.session.commit()

    return "Company Approved"


@app.route('/admin/pending_companies')
@login_required
def pending_companies():
    if current_user.role != 'admin':
        return "Access Denied"

    companies = Company.query.filter_by(approval_status="Pending").all()
    return render_template('pending_companies.html', companies=companies)



if __name__ == '__main__':
    app.run(debug=True)