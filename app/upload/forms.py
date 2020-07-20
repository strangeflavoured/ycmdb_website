from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField

class SubmitDataForm(FlaskForm):
	#init with choices & default values
	def __init__(self, choices, defaults):
		super(SubmitDataForm, self).__init__()
		#set choices		
		self.StrainSelected.choices=choices["StrainSelected"]	
		self.MediumSelected.choices=choices["MediumSelected"]
		self.Medium_CompoundSelected.choices=choices["Medium_CompoundSelected"]
		self.DataTypes.choices=choices["DataTypes"]
		#set defaults
		self.DataSetContact.default=defaults["DataSetContact"]
		self.StrainSelected.default=defaults["StrainSelected"]
		self.MediumSelected.default=defaults["MediumSelected"]
		self.Medium_CompoundSelected.default=defaults["Medium_CompoundSelected"]
		self.DataTypes.default=defaults["DataTypes"]

	#general info
	DataSetName=StringField("Name your data set")  # save datset information
	DataSetContact=StringField("Contact email address")
	DataSetPublication=StringField("Optional: Publication (PubMedID or doi)")
	#strain info
	StrainSelected=SelectField("Select strain")  # save Strain Information #choices = c("add new strain", all_strains))
	StrainName=StringField("Strain name") 
	strain_ploidity=StringField("Ploidity") 
	strain_mating_type=StringField("Mating type") 
	strain_mutations =StringField("Mutations")
	strain_link =StringField("External link to strain")
	strain_comment =StringField("Additional information")
	#medium info
	MediumSelected=SelectField("Select medium") # save Medium Information #choices = c("add new medium", all_media))
	Medium_pH=StringField("Medium pH") 
	Medium_Name =StringField("Medium name")
	#medium composition
	Medium_CompoundSelected=SelectField("Select compound")#choices = c("add new compound", knownMediumCompounds$Component)
	Medium_CompoundName=StringField("Compound")
	Medium_Value=StringField("Concentration")
	Medium_Unit=StringField("Unit")
	Medium_CompoundPubChemID=StringField("PubChem")
	Medium_provided=BooleanField("")
	#cultivation info
	Synchronised=StringField("Synchronisation method") # save Cultivation information
	Temperature =StringField("Temperature [°C]")
	GrowthPhase =StringField("Growth phase")
	GrowthRate=StringField("Growth rate [1/h]")
	Aeration =SelectField("Aeration", choices=["aerobic", "anaerobic"])
	CultureType=SelectField("Culture type", choices=["batch", "chemostat"])
	#measurement info
	MethodName =StringField("Measurement method") # save method information
	Unit =StringField("Unit of measurement")
	ValueType =SelectField("Type of values", choices=[("average", "average - std"),("median", "median - 25% percentile - 75% percentile"), ("range", "value - min - max")])
	IsTimeResolved=SelectField("Is your data time resolved?", choices=[("true", "yes"), ("false", "no")])
	UnitTime=SelectField("Timesteps unit", choices=["n.a.","s","min","h","d"])
	#upload
	DataTypes=SelectField("Select data type to be uploaded")
	submit=SubmitField("Submit Data")