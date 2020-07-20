from flask import render_template, redirect, url_for, flash, request, jsonify, send_file
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
import pandas as pd
pd.options.mode.chained_assignment=None
from datetime import datetime
import io

from app import db
from app.upload import bp
from app.general import getUser, userIsAdmin, userConfirmed, navigation, getStrains, getMedia
from app.upload.forms import SubmitDataForm
from app.model._data_columns import DownloadDict
from app.stats.routes import ForMediumPlot

@bp.route('/submit', methods=["GET","POST"])
def submit():
	#deal with users who arent registered/logged in
	if not current_user.is_authenticated:
		return render_template("upload/submit.html", admin=userIsAdmin(), navigation=navigation, category="submit", title="Submit Data", user=False)
	else:
		#create choices for submission form
		choices={}
		choices["StrainSelected"]=["add strain"]+sorted(getStrains())
		choices["MediumSelected"]=["add medium"]+sorted(getMedia())
		choices["Medium_CompoundSelected"]=["add component"]+sorted(ForMediumPlot["outmatrix_wide"].columns)
		choices["DataTypes"]=DownloadDict["choices"]

		#create defaults for submission form
		defaults={}
		user=getUser()
		defaults["DataSetContact"]=user.email
		defaults["StrainSelected"]="add strain"
		defaults["MediumSelected"]="add medium"
		defaults["Medium_CompoundSelected"]="add component"
		defaults["DataTypes"]=choices["DataTypes"][0][0]		

		defDtype=DownloadDict["identifier"][defaults["DataTypes"]]

		form=SubmitDataForm(choices, defaults)
		form.process()
		submittedAs=False

		if request.method=="POST":
			user.last_submit=datetime.utcnow()
			db.session.commit()
			flash("Your data were successfully submitted.", "info")
			submittedAs=request.form['DataSetName']
		
		return render_template("upload/submit.html", defDtype=defDtype, submittedAs=submittedAs, user=True, form=form, admin=userIsAdmin(), navigation=navigation, category="submit", title="Submit Data", confirmed=userConfirmed())

@bp.route("/submit/process", methods=["POST"])
def processSubmission():
	if request.is_json:
		ajax = request.get_json(force=True)
		formData = {elem["name"]:elem["value"] for elem in ajax["formData"]}
		formData["user"]=getUser().id
		#drop form data that are not necessary
		for key in ["csrf_token", "Medium_provided", "Medium_CompoundSelected", "Medium_CompoundName", "Medium_CompoundPubChemID", "Medium_Value", "Medium_Unit", "pretty-input", "Data_provided", "check_time", "pretty-input-2", "submit"]:
			formData.pop(key, None)
		formData=pd.DataFrame.from_dict(formData, orient="index")
		mediumComposition = pd.read_json(ajax["mediumComposition"], orient="records")
		Data = pd.read_json(ajax["Data"], orient="records")
		#tables: appr. data; RELATION strain, pub, medium; META medium comp
		name=f"{formData.loc['DataSetName',0]}_{datetime.utcnow().strftime('%d-%m-%Y_%H:%M:%S')}"
		directory=config["BASEDIR"]+"/DataUpload/"+name
		os.mkdir(directory)
		#save data to files
		with open(config["BASEDIR"]+"/DataUpload/UploadsOverview.csv", "a+") as file:
			file.write(f"{formData.loc['DataSetName',0]},{formData.loc['DataSetContact',0]},{datetime.utcnow()},{formData.loc['DataTypes',0]},{len(Data.index)},,,,\n")
		formData.to_csv(directory+f"/FormData_{name}.csv", header=False)
		mediumComposition.to_csv(directory+f"/Medium_{name}.csv")
		Data.to_csv(directory+f"/Data_{name}.csv")
		pickle.dump({"formData": formData, "mediumComposition": mediumComposition, "Data": Data}, open(directory+f"/DataSet_{name}.pkl", "wb+"))
		return "true"
	else:
		return "false"

@bp.route("/submit/checkTime")
@login_required
def checkTime():	
	user=getUser()
	lastSubmit=user.last_submit
	if lastSubmit:
		timeDifference=(datetime.utcnow()-lastSubmit).total_seconds()/60
		valid = timeDifference>=config["TIME_BETWEEN_SUBMITS"]
	else:
		valid = False
	return str(valid).lower()

@bp.route("/submit/downloadCurrent/<data>")
def downloadCurrent(data):
	formData=data.split("&&")[0]
	dataName=[arg for arg in formData.split("&") if "DataSetName" in arg][0].split("=")[-1]
	fileName=f"DataSet_{dataName}_{datetime.utcnow().strftime('%d-%m-%Y_%H:%M:%S')}.txt"

	file = io.BytesIO()
	file.write(data.encode('utf-8'))
	file.seek(0)
	
	return send_file(file, mimetype='text/txt', as_attachment=True, attachment_filename=fileName)

@bp.route("/submit/autoFill", methods=["POST"])
def fillSubmit():
	#deal with ajax requests to populate fields	
	if request.is_json:
		ajax = request.get_json(force=True)
		if ajax["request"]=="strain":
			if ajax["strain"]!="add strain":
				strainDict=getStrainInfo(ajax["strain"])
			else:
				strainDict={"strainId":"new"}
			return jsonify(strainDict)
		if ajax["request"]=="medium":
			if ajax["medium"]!="add medium":
				mediumDict=pd.read_sql_query(f"select Medium_ID, pH, uniqueID from RELATION_Medium where Medium_ID='{ajax['medium']}'", db.get_engine(bind="data")).to_dict("records")[0]
				mediumDict["composition"]=pd.read_sql_query(f"select Component, PubChem, Value, Unit from META_MediumComposition where Medium_uniqueID='{mediumDict['uniqueID']}'", db.get_engine(bind="data")).fillna("").to_json(orient="values")
			else:
				mediumDict={"Medium_ID":"new"}
			return jsonify(mediumDict)
		if ajax["request"]=="component":
			if ajax["component"]!="add component":
				componentDict=pd.read_sql_query(f"select Component, PubChem from META_MediumComposition where Component='{ajax['component']}'", db.get_engine(bind="data")).to_dict("records")[0]
			else:
				componentDict={"PubChem": "new"}
			return jsonify(componentDict)
		if ajax["request"]=="dtype":
			return jsonify({"identifier": DownloadDict["identifier"][ajax["dtype"]]})

@bp.route("/getTemplate")
@login_required
def downloadTemplate():
	path=config["BASEDIR"]+"/UploadTemplates/"+request.args.get("file")
	return send_file(path, mimetype='text/csv', as_attachment=True, attachment_filename="DataTemplate.csv")

@bp.route("/uploadTemplate", methods=["POST"])
@login_required
def uploadTemplate():
	uploadedFile=request.files.get('file')
	data=pd.read_csv(uploadedFile, skiprows=1).fillna(" ").iloc[:,1:]
	colsDef=json.dumps([{"data":col, "title":col} for col in data.columns])
	return jsonify({"columns":colsDef, "data":data.to_json(orient="records")})