

# --- IMPORTS ---
import random
import string
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

# --- APP CONFIG ---
app = Flask(__name__)
app.secret_key = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sendercode0000@gmail.com'
app.config['MAIL_PASSWORD'] = 'mswkimotafgjbdek'

db = SQLAlchemy(app)
mail = Mail(app)

# --- MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)  # username
    password = db.Column(db.String(150), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=False)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('election.id'))
    votes = db.Column(db.Integer, default=0)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    election_id = db.Column(db.Integer)

# --- HELPERS ---
def get_current_user():
    user_id = session.get('user')
    if user_id:
        return User.query.get(user_id)
    return None

# --- EMAIL CODE ---
def generate_code():
    return ''.join(random.choices(string.digits, k=6))

# --- ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash("Passwords do not match", "danger")
            return redirect('/register')

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return redirect('/register')

        code = generate_code()
        session['temp_user'] = {
            'email': email,
            'password': password,
            'code': code
        }
        msg = Message(
            subject="Online Voting System – Email Verification",
            sender=("Online Voting System", app.config['MAIL_USERNAME']),
            recipients=[email],
            body=f"Your verification code is: {code}"
        )
        mail.send(msg)
        return redirect('/verify')
    return render_template('register.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        user_code = request.form['code']
        temp_user = session.get('temp_user')
        if not temp_user:
            flash("Session expired. Register again.", "danger")
            return redirect('/register')
        if user_code == temp_user['code']:
            new_user = User(
                email=temp_user['email'],
                password=temp_user['password'],
                verified=True
            )
            db.session.add(new_user)
            db.session.commit()
            session.pop('temp_user')
            flash("Email verified successfully! Please login.", "success")
            return redirect('/login')
        else:
            flash("Invalid verification code", "danger")
    return render_template('verify.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password, verified=True).first()
        if user:
            session['user'] = user.id
            return redirect('/dashboard')
        else:
            flash("Invalid credentials or email not verified", "danger")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    elections = Election.query.filter_by(is_active=True).all()
    return render_template('dashboard.html', elections=elections)

@app.route('/vote/<int:id>', methods=['GET','POST'])
def vote(id):
    if request.method == 'POST':
        if not Vote.query.filter_by(user_id=session['user'], election_id=id).first():
            v = Vote(user_id=session['user'], election_id=id)
            c = Candidate.query.get(request.form['candidate'])
            c.votes += 1
            db.session.add(v)
            db.session.commit()
        return redirect('/dashboard')
    candidates = Candidate.query.filter_by(election_id=id).all()
    return render_template('vote.html', candidates=candidates)

@app.route('/results/<int:id>')
def results(id):
    candidates = Candidate.query.filter_by(election_id=id).all()
    return render_template('results.html', candidates=candidates)

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        e = Election(name=request.form['name'], active=True)
        db.session.add(e)
        db.session.commit()
    return render_template('admin.html', elections=Election.query.all())

@app.route('/admin/create-election', methods=['GET', 'POST'])
def create_election():
    user = get_current_user()
    if not user or not user.is_admin:
        return redirect('/dashboard')
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        election = Election(title=title, description=desc, is_active=True)
        db.session.add(election)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('create_election.html')

@app.route('/make-admin')
def make_admin():
    user = User.query.filter_by(email="youradminemail@gmail.com").first()
    if user:
        user.is_admin = True
        db.session.commit()
        return "Admin created"
    return "User not found"

# --- DB INIT ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
