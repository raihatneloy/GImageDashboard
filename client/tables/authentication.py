from wtforms import Form, TextField, PasswordField, validators

class Login(Form):
	identity = TextField('Username', validators=[validators.required()])
	password = PasswordField('Password', validators=[validators.required()])

class Register(Form):
	username = TextField('Username', validators=[validators.required()])
	email = TextField('Email Address', validators=[validators.Email(message='Input a valid email id')])
	name = TextField('Full name', validators=[validators.required()])
	password = PasswordField('Password', validators=[validators.required(), validators.EqualTo('confirm', message='Password didn\'t match')])
	confirm = PasswordField('Confirm Password', validators=[validators.required()])
