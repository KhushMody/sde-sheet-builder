from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    question = db.Column(db.Text, nullable=False)
    acceptance = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    question_link = db.Column(db.Text, nullable=False)