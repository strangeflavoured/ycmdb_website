from app.model._data_columns import displayColumnNames
from flask import url_for, flash

def PubLink(Id):
	if Id[:3]=="PMC":
		return f"<a target='_blank' rel='noopener noreferrer' href='https://www.ncbi.nlm.nih.gov/pmc/articles/{Id}/'>{Id}</a>"
	elif Id[:3]=="doi":
		return f"<a target='_blank' rel='noopener noreferrer' href='https://dx.doi.org/{Id}'>{Id}</a>"
	else:
		return f"<a target='_blank' rel='noopener noreferrer' href='https://pubmed.ncbi.nlm.nih.gov/{Id}/'>{Id}</a>"

def processResults(dataframe, selectionList=False, tableId="results_table"):
	#create links
	try:
		dataframe["Publication_Link"] = dataframe["Publication_Link"].apply(lambda x: PubLink(x))
	except KeyError:
		pass
	try:
		dataframe["Strain_ID"] = dataframe["Strain_ID"].apply(lambda x: f"<a href='{url_for('main.strainInfo', Name=x)}'>{x}</a>")
	except KeyError:
		pass
	try:
		dataframe["Medium_ID"] = dataframe["Medium_ID"].apply(lambda x: f"<a href='{url_for('main.mediumInfo', Name=x)}'>{x}</a>")
	except KeyError:
		pass
	try:
		dataframe["Author_Year"] = dataframe["Author_Year"].apply(lambda x: f"<a href='{url_for('main.publicationInfo', Pub=x)}'>{x}</a>")
	except KeyError:
		pass
	try:
		dataframe["PubChem"] = dataframe["PubChem"].apply(lambda x: f"<a target='_blank' rel='noopener noreferrer' href='https://pubchem.ncbi.nlm.nih.gov/compound/{x}'>{x}</a>")
	except KeyError:
		pass
	try:
		dataframe["Link"] = dataframe["Link"].apply(lambda x: f"<a target='_blank' rel='noopener noreferrer' href='{x}'>{x}</a>")
	except KeyError:
		pass
	try:
		dataframe["SGD_ID"] = dataframe["SGD_ID"].apply(lambda x: f"<a target='_blank' rel='noopener noreferrer' href='https://www.yeastgenome.org/locus/{x}'>{x}</a>")
	except KeyError:
		pass
	try:
		dataframe["Uniprot_ID"] = dataframe["Uniprot_ID"].apply(lambda x: f"<a target='_blank' rel='noopener noreferrer' href='https://www.uniprot.org/uniprot/{x}'>{x}</a>")
	except KeyError:
		pass
	try:
		dataframe["SwissProt_ID"] = dataframe["SwissProt_ID"].apply(lambda x: f"<a target='_blank' rel='noopener noreferrer' href='https://www.uniprot.org/uniprot/{x}'>{x}</a>")
	except KeyError:
		pass
	try:
		dataframe["ChEBI_ID"] = dataframe["ChEBI_ID"].apply(lambda x: f"<a target='_blank' rel='noopener noreferrer' href='https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:{x}'>{x}</a>")
	except KeyError:
		pass
	try:
		dataframe["EC_Nr"] = dataframe["EC_Nr"].apply(lambda x: f"<a target='_blank' rel='noopener noreferrer' href='https://enzyme.expasy.org/EC/{x}'>{x}</a>")
	except KeyError:
		pass	
	try:
		dataframe=dataframe[selectionList]
	except KeyError:
		pass


	dataframe=dataframe.rename(columns=displayColumnNames)	
	dataframe.index=list(range(1,len(dataframe.index)+1))

	dataframe = dataframe.to_html(escape=False, border = True, table_id=tableId, classes = ["table", "table-striped", "table-bordered", "table-hover", "table-fixed"])
	return(dataframe+"<style>td{white-space:nowrap;} th{white-space:nowrap;}</style>")

def redirectResults(table, searchId):
	if table[:3]=="MET":
		category="metabolic"
	if table[:3]=="GEX":
		category="proteomic"
	else:
		category="biophysical"
	return f"<a href='{url_for('main.results', category=category, table=table, search=searchId)}'>{displayColumnNames[table]}</a>"

def processRel(dataframe, tableId, searchId):
	dataframe=dataframe[dataframe>0]
	dataframe=dataframe.dropna(axis="columns", how="all")
	dataframe=dataframe.transpose()
	dataframe.reset_index(level=0, inplace=True)
	dataframe=dataframe.rename(columns={"index": "Table", 0: "Number of Entries"})
	dataframe["Table"]=dataframe["Table"].apply(lambda x: redirectResults(x, searchId))
	dataframe = dataframe.to_html(index=False, escape=False, border = True, table_id=tableId, classes = ["table", "table-striped", "table-bordered", "table-hover", "table-fixed"])
	return(dataframe+"<style>td{white-space:nowrap;} th{white-space:nowrap;}</style>")