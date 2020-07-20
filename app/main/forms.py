from flask_wtf import FlaskForm
from wtforms import widgets, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    option_widget = widgets.CheckboxInput()
    widget = widgets.TableWidget()

class SelectCompoundForm(FlaskForm):
	def __init__(self, choices, default="glucose"):
		super(SelectCompoundForm, self).__init__()
		self.compound.choices=choices
		self.compound.default=default
	compound=SelectField("")

class FilterResultsForm(FlaskForm):
	def __init__(self, choices, default):
		super(FilterResultsForm, self).__init__()
		self.select.choices=choices
		self.select.default=default	
	select = MultiCheckboxField("", validators=[DataRequired()])
	submit = SubmitField("Apply")