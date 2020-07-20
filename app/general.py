import pandas as pd
from lxml import etree
import io, re
from flask_login import current_user
from flask import current_app
from flask_mail import Message
from threading import Thread
from app import mail, db
from app.model.models import User

navigation=["metabolic", "proteomic", "biophysical", "strains", "media", "publications", "about"]

def figureToSvg(fig):
	#convert fig to svg
	storage=io.StringIO()
	fig.savefig(storage, format="svg")
	storage.seek(0)
	
	#remove encoding specification to enable lxml parse
	figSvg=re.sub(r"encoding=['\"](.*?)['\"] ", "", storage.read())
	#set svg width
	figSvg=setSvgWidth(figSvg, width="100%")

	return figSvg

def getMedia():
	return pd.read_sql_query("select Medium_ID from RELATION_Medium", db.get_engine(bind="data")).fillna("").to_dict("list")["Medium_ID"]

def getStrains():
	return pd.read_sql_query("select Strain_ID from RELATION_Strain", db.get_engine(bind="data")).fillna("").to_dict("list")["Strain_ID"]

def getStrainInfo(strainId):
	strain=pd.read_sql_query(f"select * from RELATION_Strain where Strain_ID='{strainId}'", db.get_engine(bind="data")).fillna("")
	strain=strain.to_dict("records")[0]
	strainDict={}
	strainDict["strainId"]=strain["Strain_ID"]
	strainDict["ploidity"]=strain["Ploidity"]
	strainDict["matingType"]=strain["Mating_Type"]
	mutations=""
	for key in strain.keys():
		if "Mutation" in key:
			if strain[key]:
				if mutations:
					mutations+=", "+strain[key]
				else:
					mutations=strain[key]
	strainDict["mutations"]=mutations
	strainDict["link"]=strain["Link"]
	strainDict["comment"]=strain["Comment"]
	strainDict["closestAncestor"]=pd.read_sql_query(f"select Closest_Ancestor from RELATION_Strain where Strain_ID='{strainId}'", db.get_engine(bind="data")).fillna("").iloc[0,0]
	return strainDict

def getUser():
	if current_user.is_authenticated:
		return User.query.filter_by(id=current_user.id).first()
	else:
		return None

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
	msg = Message(subject, sender=sender, recipients=recipients)
	msg.body = text_body
	msg.html = html_body
	Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def setSvgWidth(svg, width="100%"):
	root=etree.fromstring(svg)
	root.attrib["width"]=width
	root.attrib.pop("height")
	return etree.tostring(root)

def userConfirmed():
	if current_user.is_authenticated:
		return getUser().confirmed
	else:
		return False

def userIsAdmin():
	user=getUser()
	if user:
		return user.email in current_app.config["ADMINS"] and userConfirmed()
	else:
		return False