from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from time import time
from datetime import datetime
import jwt
from app import db, login

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	__bind_key__="users"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	confirmed = db.Column(db.Boolean, unique=False, default=False)	
	last_submit = db.Column(db.DateTime, index=True)
	
	def __repr__(self):
		return f"<{self.name}>"

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_reset_password_token(self, expires_in=1800):
		return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	def get_email_token(self, expires_in=1800):
		return jwt.encode({'confirm_email': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

	@staticmethod
	def verify_email_token(token):
		try:
			id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

from app.model._data_models import *