from flask import Flask, render_template, redirect
from models import db, User, Student, Company

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "Placement Portal Running "


if __name__ == '__main__':
    app.run(debug=True)