import datetime
import os
from flask import Flask,render_template,request,flash,session,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt


from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SelectField, TextAreaField, HiddenField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Regexp

import pyotp

from forms import UserLoginForm,UserSignupForm
from helper import calc_integrity
from aes_encryptor import encryptor,key_encode_to_base64

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)

bcrypt = Bcrypt(app)

#CORS
CORS(app)

app.secret_key = 'SECRET123'

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
# initialize the app with the extension
db.init_app(app)


def password_hash(password: str):
    return bcrypt.generate_password_hash(password).decode("utf-8")


def password_verify(hash: str, password: str):
    return bcrypt.check_password_hash(hash, password)


def is_user_loggedin():
    return 'loggedin' in session


def verify_totp(secret_key, totp_code):
    totp = pyotp.TOTP(secret_key)
    return totp.verify(totp_code)




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    first_name = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable=False)
    mobile = db.Column(db.String, nullable=False)
    credit_card_number = db.Column(db.String, nullable=False)
    aadhaar_number = db.Column(db.String,nullable=False)
    pancard_number = db.Column(db.String,nullable=False)    
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


with app.app_context():
    db.create_all()
    




@app.route("/")
def index():
    return render_template('index.html')


@app.route('/logout')
def user_logout():
    session.clear()
    return redirect(url_for('user_login'))

@app.route('/login',methods=['GET','POST'])
def user_login():
    form = UserLoginForm()
    if is_user_loggedin():
        return redirect(url_for('user_dashboard'))
    elif request.method == 'POST' and form.validate():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if password_verify(user.password, form.password.data):
                key = os.urandom(16)
                session['key'] = key
                session['base64_key'] = key_encode_to_base64(key)
                session['loggedin'] = True
                session['user_id'] = user.id
                return redirect(url_for('user_dashboard'))
            else:
                flash('Incorrect Password !', 'danger')
        except Exception as e:
            print(e)
            flash('Email does not exist !','danger')
    #calc_integrity(render_template('user.login.html', form=form))
    return render_template('user.login.html',form=form)


@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    form = UserSignupForm()
    if request.method=='POST' and form.validate():
        user = User(
            email=form.email.data,
            password=password_hash(form.password.data),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            address=form.address.data,
            mobile=form.mobile.data,
            credit_card_number=form.credit_card_number.data,
            aadhaar_number=form.aadhaar_number.data,
            pancard_number=form.pancard_number.data
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful !','success')
        except Exception as e:
            print(e)
            flash('Email ID already exists !','danger')
          
    return render_template('user.signup.html',form=form)


@app.route('/dashboard')
def user_dashboard():
    if is_user_loggedin():
        user = db.session.get(User, session['user_id'])
        user_enc_data = {
            'aadhaar':encryptor(user.aadhaar_number,session['key']),
            'credit':encryptor(user.credit_card_number,session['key']),
            'pan':encryptor(user.pancard_number,session['key'])
        }
        return render_template('user.dashboard.html',data=user_enc_data)
    else:
        return redirect(url_for('user_login'))


@app.route('/key')
def user_encryption_key():
    if is_user_loggedin():
        return jsonify({'key':session['base64_key']})
    else:
        redirect(url_for('user_login'))
        
if __name__ == "__main__":
    app.run(debug=True)