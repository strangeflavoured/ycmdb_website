from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.model.models import User

class ChangePasswordForm(FlaskForm):
	oldPassword = PasswordField('Old Password', validators=[DataRequired()])
	newPassword = PasswordField('New Password', validators=[DataRequired()])
	newPassword2 = PasswordField('Repeat New Password', validators=[DataRequired(), EqualTo('newPassword')])
	submit = SubmitField('Change Password')

class DeleteAccountForm(FlaskForm):
	password=PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Delete Account')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Email is already in use.')

class ResendConfirmationForm(FlaskForm):
	submit = SubmitField('Resend Confirmation E-Mail')
		
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')

class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')