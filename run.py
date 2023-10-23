from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import UserMixin
import stripe
from dotenv import load_dotenv
import os

load_dotenv()

stripe_public_key = os.getenv("STRIPE_PUBLIC_KEY")
stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'CMfgkELMQ4e7FG8nS+GVC7Lr9174et8jR0bJcBeuKVtm7JseaG1QWy0NIsofOo/v'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


@app.route("/")
@app.route("/home")
def home():
    return render_template('Home.html')


@app.route("/platform")
def platform():
    return render_template('Platform.html')


@app.route("/ingest")
def ingest():
    return render_template('Ingest.html')


@app.route("/preprocessing")
def preprocessing():
    return render_template('PreProcessing.html')


@app.route("/classify")
def classify():
    return render_template('Classify.html')


@app.route("/extract")
def extract():
    return render_template('Extract.html')


@app.route("/products")
def products():
    return render_template('Products.html')


@app.route("/privacypolicy")
def privacypolicy():
    return render_template('PrivacyPolicy.html')


@app.route("/aboutus")
def aboutus():
    return render_template('AboutUs.html')


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('That username is taken. Please choose a different one.')
            return redirect(url_for('signup'))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login Successful. Welcome, { form.username.data }')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You have successfuly logged out!")
    return redirect(url_for('home'))


@app.route("/donate")
def donate():
    return render_template('donate.html')


@app.route('/charge', methods=['POST'])
def charge():
    try:
       	flash("Payment Successful, Thanks For The Support!")
        return redirect(url_for('home'))
    except stripe.error.CardError as e:
        # The card has been declined
        flash("Payment Unsuccessful, Card Was Declined!")
        return render_template('home.html')


@app.route("/contactus")
def contactus():
    return render_template('ContactUs.html')


@app.route('/resumemaker')
def resumemaker():
    return render_template('ResumeMaker.html')


@app.route('/generateresume', methods=['POST'])
def generate_resume():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    summary = request.form['summary']

    titles = request.form.getlist('titles[]')
    companies = request.form.getlist('companies[]')
    start_dates = request.form.getlist('start_dates[]')
    end_dates = request.form.getlist('end_dates[]')
    descriptions = request.form.getlist('descriptions[]')

    experiences = []
    for i in range(len(titles)):
        experiences.append({
            'title': titles[i],
            'company': companies[i],
            'start_date': start_dates[i],
            'end_date': end_dates[i],
            'description': descriptions[i],
        })

    return render_template('GenerateResume.html', name=name, email=email, phone=phone, summary=summary, experiences=experiences)


if __name__ == '__main__':
    app.run(debug=True)
