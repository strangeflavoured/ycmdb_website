from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime

from app import db
from app.auth import bp
from app.general import getUser, userIsAdmin, userConfirmed, navigation
from app.auth.forms import ChangePasswordForm, DeleteAccountForm, LoginForm, RegistrationForm, ResendConfirmationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.model.models import User
from app.auth.email import send_confirmation_email, send_password_reset_email

@bp.route("/changePassword", methods=["GET","POST"])
@login_required
def changePassword():
	form=ChangePasswordForm()
	user=getUser()
	if form.validate_on_submit():
		if not user.check_password(form.oldPassword.data):
			flash('Invalid password',"danger")
			return redirect(url_for('changePassword'))
		else:
			user.set_password(form.newPassword.data)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for("index"))
	return render_template("auth/change_password.html", admin=userIsAdmin(), navigation=navigation, confirmed=userConfirmed(), form=form)

@bp.route("/resendConfirmation", methods=["GET","POST"])
@login_required
def resendConfirmation():
	if userConfirmed():
		return redirect(url_for("index"))
	form=ResendConfirmationForm()
	if request.method=="POST":
		user=getUser()
		send_confirmation_email(user)
		flash('Confirmation mail was sent', "info")
		return redirect(url_for("index"))
	return render_template("auth/resend_confirmation.html", admin=userIsAdmin(), navigation=navigation, confirmed=userConfirmed(), form=form)

@bp.route("/deleteAccount", methods=["GET","POST"])
@login_required
def deleteAccount():
	form=DeleteAccountForm()
	if request.method=="POST":
		user = getUser()
		if not user.check_password(form.password.data):
			flash('Invalid password',"danger")
			return redirect(url_for('deleteAccount'))
		else:
			logout_user()
			db.session.delete(user)
			db.session.commit()			
			flash("Your Account was deleted permanently.", "warning")
			return redirect(url_for("index"))
	return render_template("auth/delete_account.html", admin=userIsAdmin(), navigation=navigation, confirmed=userConfirmed(), form=form)

@bp.route('/login', methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password',"danger")
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get("next")
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('auth/login.html', admin=userIsAdmin(), navigation=navigation, category=False, title='Sign In', form=form, confirmed=userConfirmed())

@bp.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))

@bp.route("/register", methods=["GET","POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(name=form.name.data, email=form.email.data, confirmed=False, created=datetime.utcnow())
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		send_confirmation_email(user)
		flash('Please confirm your E-mail adress', "info")
		return redirect(url_for('login'))
	return render_template('auth/register.html', admin=userIsAdmin(), category=False, navigation=navigation, title='Register', confirmed=userConfirmed(), form=form)

@bp.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
	user = User.verify_email_token(token)	
	if not user:
		flash("Confirmation failed", "warning")
		return redirect(url_for('index'))
	else:
		user.confirmed=True
		db.session.commit()
		flash('Your E-mail adress has been confirmed.', "success")
		return redirect(url_for('login'))
	return render_template('auth/reset_password.html', admin=userIsAdmin(), navigation=navigation, category=False, confirmed=userConfirmed(), form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash('Check your email for the instructions to reset your password', "info")
		return redirect(url_for('login'))
	return render_template('auth/reset_password_request.html', admin=userIsAdmin(), title='Reset Password', category=False, navigation=navigation, confirmed=userConfirmed(), form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been reset.',"success")
		return redirect(url_for('login'))
	return render_template('auth/reset_password.html', admin=userIsAdmin(), category=False, navigation=navigation, confirmed=userConfirmed(), form=form)