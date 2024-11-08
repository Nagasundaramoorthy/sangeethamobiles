from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://naga:BMG8joHgRfqCQjSaHMQmMbycnvNlqc3U@dpg-csk5680gph6c73a6pqb0-a.virginia-postgres.render.com/sangeethamobiles?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    online = db.Column(db.Boolean, default=False)

# Create tables
with app.app_context():
    db.create_all()
