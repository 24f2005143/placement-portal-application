from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    student = db.relationship('Student', backref='user', uselist=False, cascade="all, delete")
    company = db.relationship('Company', backref='user', uselist=False, cascade="all, delete")


class Student(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    department = db.Column(db.String(100))
    skills = db.Column(db.String(200))
    resume = db.Column(db.String(200))
    is_blacklisted = db.Column(db.Boolean, default=False)
    applications = db.relationship('Application', backref='student', cascade="all, delete", lazy=True)



class Company(db.Model):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(200))
    approval_status = db.Column(db.String(50), default="Pending")
    drives = db.relationship('Drive', backref='company', cascade="all, delete", lazy=True)



class Drive(db.Model):
    __tablename__ = "drive"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text)
    eligibility = db.Column(db.String(200))
    location = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(50), default="Pending")
    applications = db.relationship('Application', backref='drive', cascade="all, delete", lazy=True)



class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)
    status = db.Column(db.String(50), default="Applied")
    application_date = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),)