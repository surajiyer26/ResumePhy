from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'CMfgkELMQ4e7FG8nS+GVC7Lr9174et8jR0bJcBeuKVtm7JseaG1QWy0NIsofOo/v'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
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
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.password == form.password.data:
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html', form=form)


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
