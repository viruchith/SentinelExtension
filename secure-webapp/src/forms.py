from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SelectField, TextAreaField, HiddenField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Regexp


class UserSignupForm(FlaskForm):
    email = EmailField(validators=[DataRequired('Email is required !')])
    password = PasswordField(validators=[DataRequired('Password is required !'),EqualTo('confirm_password','Passwords donot match !')])
    confirm_password = PasswordField(label='Confirm Password',validators=[DataRequired('Confirm Password is required !'),EqualTo('password','Passwords donot match !')])
    first_name = StringField('First Name',id='fname',validators=[DataRequired('First Name is required !')])
    last_name = StringField('Last Name',id='lname',validators=[DataRequired('Last Name is required !')])
    gender = SelectField(choices=['Male','Female','Other'],validators=[DataRequired('Gender is required !')])
    address = TextAreaField('Address', validators=[DataRequired('Address is required !')])
    mobile = StringField(validators=[DataRequired('First Name is required !'), Regexp(regex="[0-9]{10}", message="Enter a valid mobile number")])
    credit_card_number = StringField(validators=[DataRequired('Credit Card Number is required !'), Regexp(
        regex="[0-9]{5}-[0-9]{5}-[0-9]{5}", message="Enter a valid Credit Card number")])
    aadhaar_number = StringField(validators=[DataRequired('Aadhaar Number is required !'), Regexp(
        regex="[0-9]{4}-[0-9]{4}-[0-9]{4}", message="Enter a valid Aadhar Number !")])
    pancard_number = StringField(validators=[DataRequired('Pancard Number is required !'), Regexp(
        regex="[0-9]{10}", message="Enter a valid PAN number")])


class UserLoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired('Email is required !')])
    password = PasswordField(
        validators=[DataRequired('Password is required !')])
