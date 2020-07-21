from flask import render_template, redirect, url_for, flash, request, jsonify, current_app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
import pandas as pd
pd.options.mode.chained_assignment=None
import re, os, sys, json

from app import db
from app.main import bp
from app.general import userIsAdmin, userConfirmed, navigation, getStrainInfo, figureToSvg, getStrains
from app.stats.stats import highlightStrainInScheme, PublicationPlot, MediumPlot
from app.main.forms import FilterResultsForm, SelectCompoundForm
from app.main.results import processResults, processRel
from app.model._data_columns import displayColumnNames, TableColumns, navigationTabs, primaryIdentifier, relTables
from app.stats.routes import ForMediumPlot, publicationStats

@bp.route('/')
@bp.route("/home")
@bp.route('/index')
def index():
	with open(os.path.join(current_app.root_path, 'stats', 'DatabaseStats.svg'), "r") as file:
		startSvg = file.read()
	return render_template("main/index.html", title="YCMD", stats=startSvg, navigation=navigation, category=False, admin=userIsAdmin(), confirmed=userConfirmed())

@bp.route('/about')
def about():
	return render_template("main/about.html", admin=userIsAdmin(), navigation=navigation, category="about", title="About Us", confirmed=userConfirmed())

@bp.route('/data/<category>', methods=["GET","POST"])
def data(category):
	parent=category.capitalize()+":"
	title=category.capitalize()+" Data"
	
	Tables=navigationTabs[category]["tables"]
	TableDisplay=navigationTabs[category]["display"]

	return render_template("main/data_start.html", title=title, admin=userIsAdmin(), parent=parent, navigation=navigation, active=False, category=category, Tables=Tables, TableDisplay=TableDisplay, confirmed=userConfirmed())

@bp.route('/data/<category>/result')
def results(category):
	activeTable=request.args.get("table", type=str)
	searchFor=request.args.get("search", "", type=str)

	selectionList=navigationTabs[category]["default"].copy()
	selectionList[3:3]=primaryIdentifier[activeTable]
	
	try:
		Tables=navigationTabs[category]["tables"].copy()
		TableDisplay=navigationTabs[category]["display"].copy()
	except KeyError:
		Tables=False
		TableDisplay=None	
	
	#result settings		
	choices=[(col, displayColumnNames[col]) for col in TableColumns[activeTable]]
	form=FilterResultsForm(choices, selectionList)
	form.process()
	
	#get table from db
	dataTable = pd.read_sql_query(f"select * from {activeTable}", db.get_engine(bind="data")).fillna("")
	numericSelection=[0]+[i+1 for i, elem in enumerate(dataTable.columns) if elem in selectionList]

	#filter, select cols to display, convert to html
	tableHtml=processResults(dataTable)

	return render_template("main/data_result.html", selection=json.dumps(numericSelection), admin=userIsAdmin(), search=searchFor, category=category, navigation=navigation, Tables=Tables, active=activeTable, table=tableHtml, TableDisplay=TableDisplay, confirmed=userConfirmed(), form=form) 

@bp.route('/strains')
def strains():
	Strains=pd.read_sql_query("select Strain_ID, Closest_Ancestor, Synonyms, Ploidity, Mating_Type, Link from RELATION_Strain", db.get_engine(bind="data")).fillna("").iloc[:,:20]	
	tableHtml=processResults(Strains, tableId="meta_table")
	return render_template("main/meta.html", admin=userIsAdmin(), navigation=navigation, category="strains", table=tableHtml, confirmed=userConfirmed())

@bp.route("/strain/redirect", methods=["POST"])
def redirectStrain():
	postStrain=request.get_json(force=True)["strain"]
	strainList=getStrains()
	if postStrain in strainList:
		response={"url": url_for("main.strainInfo", Name=postStrain)+"#ancestry_chart"}
	else:
		response={"url": False}
	return jsonify(response)

@bp.route("/strain")
def strainInfo():
	strainId=request.args.get("Name")
	if not strainId:
		return redirect(url_for("main.strains"))
	else:
		strainDict=getStrainInfo(strainId)
		scheme, selectedId=highlightStrainInScheme(strainDict["closestAncestor"])
		entries=pd.read_sql_query(f"select {', '.join(relTables)} from RELATION_Strain WHERE Strain_ID = '{strainId}'", db.get_engine(bind="data")).fillna("")
		entriesHtml=processRel(entries, tableId="strain_entries", searchId=strainId)
		return render_template("main/strain_info.html", admin=userIsAdmin(), selectedId=selectedId, scheme=scheme.decode("utf-8"), navigation=navigation, category="strains", entries=entriesHtml, strain=strainDict, confirmed=userConfirmed())

@bp.route('/media')
def media():
	Media=pd.read_sql_query("select Publication_Link, Medium_ID, pH, uniqueID from RELATION_Medium", db.get_engine(bind="data")).fillna("")
	tableHtml=processResults(Media, tableId="meta_table")	
	return render_template("main/meta.html", admin=userIsAdmin(), navigation=navigation, category="media", table=tableHtml, confirmed=userConfirmed())

@bp.route("/medium", methods=["GET","POST"])
def mediumInfo():	
	mediumId=request.args.get("Name")
	mediumMetaId=request.args.get("MediumID")
	if not mediumId and not mediumMetaId:
		return redirect(url_for("main.media"))
	else:
		if not mediumMetaId:
			mediumMetaId=pd.read_sql_query(f"select uniqueID from RELATION_Medium where Medium_ID='{mediumId}'", db.get_engine(bind="data"))["uniqueID"].iloc[0]
		if not mediumId:
			mediumId=pd.read_sql_query(f"select Medium_ID from RELATION_Medium where uniqueID='{mediumMetaId}'", db.get_engine(bind="data"))["Medium_ID"].iloc[0]
		selectedCompound=request.args.get("compound", "Glucose", type=str)
		choices=[("all", "all")]+[(compound, compound) for compound in sorted(ForMediumPlot["outmatrix_wide"].columns)]
		
		#set up form for compound selection	
		form=SelectCompoundForm(choices=choices, default=selectedCompound)
		form.process()

		#get data from data base
		pH=pd.read_sql_query(f"select pH from RELATION_Medium where Medium_ID='{mediumId}'", db.get_engine(bind="data")).iloc[0,0]
		Medium=pd.read_sql_query(f"select Component, PubChem, Value, Unit from META_MediumComposition where Medium_uniqueID='{mediumMetaId}'", db.get_engine(bind="data")).fillna("")
		entries=pd.read_sql_query(f"select {', '.join(relTables)} from RELATION_Medium WHERE Medium_ID = '{mediumId}'", db.get_engine(bind="data")).fillna("")
		
		#print(Medium["Component"], file=sys.stdout)
		#process data fro display
		tableHtml=processResults(Medium, tableId="medium_composition")
		entriesHtml=processRel(entries, tableId="medium_entries", searchId=mediumId)

		#plot medium, convert to svg
		fig=MediumPlot(ForMediumPlot["tsne_result"], ForMediumPlot["outmatrix_wide"], mediumMetaId, selectedCompound)		
		MediumRelPlot=figureToSvg(fig)

		#render template
		return render_template("main/medium_info.html", admin=userIsAdmin(), RelPlot=MediumRelPlot.decode("utf-8"), form=form, pH=pH, navigation=navigation, entries=entriesHtml, category="media", title=mediumId, table=tableHtml, confirmed=userConfirmed())

@bp.route('/publications')
def publications():
	Publications=pd.read_sql_query("select Author_Year, Year, Publication_Link, Title from RELATION_Publication", db.get_engine(bind="data")).fillna("")
	tableHtml=processResults(Publications, tableId="meta_table")
	return render_template("main/meta.html", admin=userIsAdmin(), navigation=navigation, category="publications", table=tableHtml, confirmed=userConfirmed())

@bp.route("/publication")
def publicationInfo():
	authorYear=request.args.get("Pub")
	selectedPublication=request.args.get("PubLink")
	if not authorYear and not selectedPublication:
		return redirect(url_for("main.publications"))
	else:
		if not authorYear:
			authorYear=pd.read_sql_query(f"select Author_Year from RELATION_Publication where Publication_Link='{selectedPublication}'", db.get_engine(bind="data"))["Author_Year"].iloc[0]
		if not selectedPublication:
			selectedPublication=pd.read_sql_query(f"select Publication_Link from RELATION_Publication where Author_Year='{authorYear}'", db.get_engine(bind="data"))["Publication_Link"].iloc[0]

		#get entries for publication
		entries=pd.read_sql_query(f"select {', '.join(relTables)} from RELATION_Publication WHERE Publication_Link = '{selectedPublication}'", db.get_engine(bind="data")).fillna("")
		entriesHtml=processRel(entries, tableId="publication_entries", searchId=authorYear)

		#plot publications, convert to svg
		fig=PublicationPlot(publicationStats, selectedPublication)
		PubRelPlot=figureToSvg(fig)
		
		publication=pd.read_sql_query(f"select Title, Authors, Affiliation, PublicationInfo, Abstract, Crossref from RELATION_Publication where Publication_Link='{selectedPublication}'", db.get_engine(bind="data")).iloc[0]
		publication["Affiliation"]=re.sub("Author information", "Affiliations", publication["Affiliation"])
		
		#generate hyperlinks from PublicationInfo
		Crossref=re.sub(r"\[(.*?)\]", "", publication["Crossref"]).strip()
		Crossref=re.split(r" |:\s*", Crossref)
		keys=Crossref[::2]
		values=Crossref[1::2]
		Crossref=dict(zip(keys, values))
		publication["Crossref"]=Crossref

		#convert dframe to dict
		publication=publication.to_dict()
		return render_template("main/publication_info.html", admin=userIsAdmin(), entries=entriesHtml, RelPlot=PubRelPlot.decode("utf-8"), navigation=navigation, category="publications", publication=publication, title=authorYear, confirmed=userConfirmed())
