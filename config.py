import os, sys
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get ("SECRET_KEY")
	if SECRET_KEY==None or len(SECRET_KEY)<10:
		sys.exit("SECURITY WARNING: PLEASE PROVIDE A VALID SECRET KEY")
	user_bind = "sqlite+pysqlite:///" + basedir + os.environ.get("USERS_DB")
	SQLALCHEMY_BINDS = {'users': user_bind, 'data': os.environ.get("DATA_DB")}
	SQLALCHEMY_TRACK_MODFICATIONS = False

	MAIL_SERVER = os.environ.get("MAIL_SERVER")
	MAIL_PORT = int(os.environ.get("MAIL_PORT"))
	MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
	MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

	DB_NAME=os.environ.get("DB_NAME")
	DB_HOST=os.environ.get("DB_HOST")
	DB_USER=os.environ.get("DB_USER")
	DB_PASSWORD=os.environ.get("DB_PASSWORD")

	ADMINS = os.environ.get("ADMINS")
	BASEDIR=basedir
	RSCRIPT=os.environ.get("RSCRIPT")

	TIME_BETWEEN_SUBMITS=os.environ.get("TIME_BETWEEN_SUBMITS")
