from flask_wtf import FlaskForm
from wtforms import SubmitField

class RefreshForm(FlaskForm):
	index=SubmitField("Refresh Index Stats")
	medium=SubmitField("Refresh Medium Stats")
	publication=SubmitField("Refresh Publication Stats")
	count=SubmitField("Refresh RELATION counts")