from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    student_profile = db.relationship('Student', backref='user', uselist=False)
    company_profile = db.relationship('Company', backref='user', uselist=False)

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float)
    resume = db.Column(db.String(200))
    is_blacklisted = db.Column(db.Boolean, default=False)

    applications = db.relationship('Application', backref='student', lazy=True)

    def __repr__(self):
        return f"<Student {self.full_name}>"


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(200))
    approval_status = db.Column(db.String(20), default='pending')
    is_blacklisted = db.Column(db.Boolean, default=False)

    drives = db.relationship('PlacementDrive', backref='company', lazy=True)

    def __repr__(self):
        return f"<Company {self.name}>"


class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    eligibility = db.Column(db.Text)
    min_cgpa = db.Column(db.Float)
    deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')

    applications = db.relationship('Application', backref='drive', lazy=True)

    def __repr__(self):
        return f"<Drive {self.title}>"


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    status = db.Column(db.String(20), default='applied')
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),)

    def __repr__(self):
        return f"<Application Student:{self.student_id} Drive:{self.drive_id}>"