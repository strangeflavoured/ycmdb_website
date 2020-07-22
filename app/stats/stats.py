import pandas as pd
import re
from flask import url_for, flash, current_app
import numpy as np
from lxml import etree
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colours
import seaborn as sns
import pickle

from app import db
from app.model._data_columns import displayColumnNames

def StringToInt(string, undefined="null"):
	try:
		val=int(string)
	except ValueError:
		if undefined=="null":
			val=0
		elif undefined.lower() in ["nan", "na"]:
			val=float('NaN')
		else:
			val=None
	return val

def Eval(expression, undefined="NaN"):
	try:
		val=eval(expression)
	except NameError:
		if undefined in ["NaN", "nan", "NA", "na"]:
			val=float('NaN')
		elif undefined=="keep":
			val=expression
		elif undefined=="null":
			val=0
		else:
			val=None
	return val

def highlightStrainInScheme(closestAncestor):
	root=etree.parse("app/static/images/SchemeStrainsYCMDB.svg").getroot()
	nsmap=root.nsmap.copy()
	nsmap["xmlns"]=nsmap.pop(None)
	node=root.xpath(f".//svg:text[svg:tspan='{closestAncestor.strip()}']", namespaces=nsmap)
	rect=root.xpath(f".//svg:g/svg:rect", namespaces=nsmap)
	node[0].attrib["style"]=node[0].attrib["style"].replace("fill:#00","fill:#AA")
	rect[0].attrib["style"]=rect[0].attrib["style"].replace("opacity:0.0","opacity:0.7")
	return (etree.tostring(root), node[0].attrib["id"])

def makeMediumPlotAndConversion():
	# get table with medium Ids
	MediumIDs=pd.read_sql_query("select Medium_ID from RELATION_Medium", db.get_engine(bind="data")).fillna("").to_dict("list")["Medium_ID"]

	# get medium components
	MediumTable=pd.read_sql_query("select * from META_MediumComposition", db.get_engine(bind="data")).fillna(float("nan"))
	MediumTable["PubChem"]=MediumTable["PubChem"].apply(lambda x: StringToInt(x, undefined="nan")).astype("Int64")

	# unique compounds
	uniqueMediumCompounds = MediumTable["Component"].unique()
	uniqueUnits = MediumTable["Unit"].unique()
	uniquePubChemIDs = MediumTable["PubChem"].dropna().unique()
	uniquePubChemIDs =[str(x) for x in uniquePubChemIDs]
	#pubchem Query molecular weight
	pubChemUrl = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{','.join(uniquePubChemIDs)}/property/MolecularWeight,MolecularFormula,IUPACName/CSV"
	uniquePubChemIDs = pd.read_csv(pubChemUrl)

	# extract number of carbons from formula
	tmp = uniquePubChemIDs["MolecularFormula"].apply(lambda x: re.sub(".*C([0-9]+)[A-Z].*","\\1", x))
	tmp = tmp.apply(lambda x: re.sub(".*C[A-Z].*","1", x))
	tmp = tmp.apply(lambda x: StringToInt(x))
	uniquePubChemIDs["nC"]=tmp

	# original names in db of the unique compounds (also unify in MediumTable)
	YCMNames={}
	for index, cid in enumerate(uniquePubChemIDs["CID"]):
		ixCID = np.array([cid==pub for pub in MediumTable["PubChem"].fillna(False)], dtype="bool")
		components = MediumTable["Component"][ixCID]
		YCMNames[cid]=components
		MediumTable["Component"][MediumTable["PubChem"]==str(cid)] = components
	uniquePubChemIDs["YCMNames"] = YCMNames

	# convert to base unit g/l
	conversion = pd.DataFrame({"formula":np.repeat("",len(uniqueUnits))}, index=uniqueUnits)

	conversion.loc["mM","formula"] =  "*1e-3 * molar_mass_g_mol"
	conversion.loc["uM","formula"] = "*1e-6 * molar_mass_g_mol"
	conversion.loc["\xb5M","formula"] = "*1e-6 * molar_mass_g_mol"
	conversion.loc["%","formula"] = "*10"   # assuming (w/v)
	conversion.loc["% (w/v)","formula"] = "*10"
	conversion.loc["g/l","formula"] = "*1"
	conversion.loc["mg/l","formula"] = "*10e-3"
	#conversion.loc["ml","formula"] = "*float('NaN')"
	conversion.loc["g/L","formula"] = "*1"
	conversion.loc["mg/L","formula"] = "*10e-3"
	conversion.loc["\xb5g/L","formula"] = "*10e-6"
	conversion.loc["ug/L","formula"] = "*10e-6"
	conversion.loc["M","formula"] = "* molar_mass_g_mol"
	conversion.loc["mg/ml","formula"] = "*1"
	conversion.loc["g/mol carbon","formula"] = "* mol_total_carbon_per_litre"
	conversion.loc["mg/mol carbon","formula"] = "*10e-3 * mol_total_carbon_per_litre"
	#conversion.loc["ml/mol carbon","formula"] = "*float('NaN')" # density must de known, not available via pubchem easily *10e-3 * mol_total_carbon_per_litre"
	#conversion.loc["% (v/v)","formula"] = "*float('NaN')" # mixed compound
	conversion.loc["ug/l","formula"] = "*10e-6"
	conversion.loc["g/1ml aqua dest.","formula"] = "*10e3"

	conversion.loc["NA","formula"] = "*float('NaN')"
	conversion.loc["","formula"] = "*float('NaN')"

	# substitute molar_mass_g_mol
	MediumTable["conversion"] = [str(i)+str(j) for i,j in zip(MediumTable["Value"], conversion.loc[MediumTable["Unit"],"formula"])]
	for index, conv in enumerate(MediumTable["conversion"]):		
		accessIndex=uniquePubChemIDs.where(MediumTable["PubChem"][index]==uniquePubChemIDs["CID"]).dropna().index
		if not accessIndex.empty:
			MediumTable["conversion"][index]=conv.replace("molar_mass_g_mol", str(uniquePubChemIDs["MolecularWeight"][accessIndex].iloc[0]))
		else:
			MediumTable["conversion"][index]=conv.replace("molar_mass_g_mol", "float('nan')")
	
	# deal with remaining mol_carbon units (number of carbons required)
	ixMolCUnits = MediumTable["Unit"].apply(lambda x: StringToInt(re.sub(".*(/mol carbon).*","1", x))) # find all entries with the unit
	ixMolCMedia = MediumTable["Medium_uniqueID"][ixMolCUnits==1].unique() # find all media that contain compound with the unit
	csourceix = np.array(MediumTable["PubChem"].isin([702, 5793, 6255, 6036])) # mask carbon sources: ethanol and glucose
  
	for MediumId in ixMolCMedia:
		# find values for ethanol or glucose
		entriesCsourceCurrentMedium = MediumTable[np.array(MediumTable["Medium_uniqueID"]==MediumId) & csourceix]

		# divide by mol weight, multiply wth number of carbons
		g_l = entriesCsourceCurrentMedium["conversion"].apply(lambda x: Eval(x))
		ix_in_pubchem_Table = uniquePubChemIDs["CID"].isin(entriesCsourceCurrentMedium["PubChem"])
		mol_C_per_litre = np.nansum(np.array(g_l)/np.array(uniquePubChemIDs["MolecularWeight"][ix_in_pubchem_Table]) * np.array(uniquePubChemIDs["nC"][ix_in_pubchem_Table]))
		#substitute value for mol_total_carbon_per_litre
		MediumTable["conversion"][MediumTable["Medium_uniqueID"]==MediumId] = MediumTable["conversion"].apply(lambda x: x.replace('mol_total_carbon_per_litre', str(mol_C_per_litre)))
	
	# evaluate conversion formula
	MediumTable["Value_g_l"] =  MediumTable["conversion"].apply(lambda x: Eval(x))
		
	# sort media into long list
	outmatrix = MediumTable[["Medium_uniqueID","Value_g_l","Component","PubChem"]]	
	outmatrix = outmatrix.dropna(subset=["PubChem"]) # remove entries without ID	
	outmatrix = outmatrix[["Medium_uniqueID","Value_g_l","Component"]] # remove Pubchem Col

	# spread stacked values to matrix
	#adds new column for each value of Component, which contains the value Value_g_l
	outmatrix_wide = outmatrix.pivot_table(index="Medium_uniqueID", columns="Component", values="Value_g_l")
	#outmatrix_wide=outmatrix_wide.fillna(0)#keeping nan makes count possible

	# do the visualization via tSNE
	tsne_out=TSNE(perplexity=1, random_state=6).fit_transform(outmatrix_wide.fillna(0))

	# pickle results
	pickleFile=current_app.config["BASEDIR"]+"/app/stats/Media.pkl"
	pickle.dump({"tsne_result": tsne_out, "outmatrix_wide": outmatrix_wide, "mediumIds": MediumIDs}, open(pickleFile, "wb+"))
	return {"tsne_result": tsne_out, "outmatrix_wide": outmatrix_wide, "mediumIds": MediumIDs}

# generate Plot for medium_info.html
def MediumPlot(tsne_result, outmatrix_wide, medium_ID_selected, compound_selected):
	#number of compounds in all media
	ncompounds = outmatrix_wide.count(axis=1)
	
	# selected medium ( from dropdown above)
	selected = outmatrix_wide.index == medium_ID_selected

	#create url for each medium
	mediumUrls=[url_for("main.mediumInfo", compound=compound_selected, MediumID=medium)+"#medium_plot" for medium in outmatrix_wide.index]

	# plot
	plt.style.use("seaborn-deep")
	fig, ax = plt.subplots(1,1)

	if compound_selected!="all":
		# selected compond for color mapping
		concentration = outmatrix_wide[compound_selected]
		minConc=np.amin(concentration)
		maxConc=np.amax(concentration)
		meanConc=np.mean(concentration)
		norm=colours.LogNorm(vmin=minConc, vmax=maxConc)

		#plot media
		sc=ax.scatter(tsne_result[:,0], tsne_result[:,1], s=np.log(ncompounds)*3+2, c=concentration, norm=norm, cmap=cm.viridis)
		
		#make colorbar
		cbar=fig.colorbar(sc, ax=ax)
		cbar.set_label('Concentration g/L', rotation=270, labelpad=10)
	else:
		#plot all media
		sc=ax.scatter(tsne_result[:,0], tsne_result[:,1], s=np.log(ncompounds)*3+2)
	
	sc.set_urls(mediumUrls)
	ax.scatter(tsne_result[selected,0], tsne_result[selected,1], s = 30, facecolor = "none", edgecolors="#AA0000", linewidth=1) # selected medium is marked
	ax.set_yticks([])
	ax.set_xticks([])
	
	ax.grid(False)
	fig.tight_layout()

	return fig

def getPublicationInfo(list_data_tables):  
	# get list of all publications
	all_pubs=pd.read_sql_query(f"select Publication_Link, Year, {', '.join(list_data_tables)} from RELATION_Publication", db.get_engine(bind="data"))
	
	# compile pub stats
	pub_matrix=all_pubs.drop(columns=["Publication_Link", "Year"])
	n_datatypes = pub_matrix.copy().replace(0, np.nan).count(axis="columns")
	n_data = pub_matrix.sum(axis="columns")
	all_pubs[["Publication_Link", "Year"]]
	all_pubs["n_datatypes"]=n_datatypes
	all_pubs["n_data"]=n_data
	all_pubs=all_pubs.set_index("Publication_Link")

	# drop entries where there are no dtypes
	all_pubs = all_pubs[all_pubs["n_datatypes"]!=0]	

	# pickle results
	pickleFile=current_app.config["BASEDIR"]+"/app/stats/Publications.pkl"
	pickle.dump({"all_pubs": all_pubs}, open(pickleFile, "wb+"))
	return all_pubs

def PublicationPlot(all_pubs, pub_ID_selected):
	# selected publication
	selected = all_pubs.index == pub_ID_selected
	pub_years=all_pubs["Year"]

	#create url for each publication
	publicationUrls=[url_for("main.publicationInfo", PubLink=publication)+"#publication_plot" for publication in all_pubs.index]

	# do the plot
	plt.style.use("seaborn-deep")
	fig, ax = plt.subplots(1,1)
	sc=ax.scatter(all_pubs["n_datatypes"], all_pubs["n_data"], s=20, c=pub_years, cmap=cm.viridis)
	sc.set_urls(publicationUrls)
	ax.scatter(all_pubs["n_datatypes"][selected], all_pubs["n_data"][selected], s = 60, facecolor = "none", edgecolors="#AA0000", linewidth=1) # selected medium is marked
	ax.set_yscale("log")
	ax.set_xlabel("Number of different data types")
	ax.set_ylabel("Number of data points", labelpad=10)
	cbar=fig.colorbar(sc, ax=ax)
	cbar.set_label('Year of Publication', rotation=270, labelpad=20)
	ax.grid(False)
	fig.tight_layout()

	return fig

def CountEntriesInTable(table):
	return len(pd.read_sql_query(f"select uniqueID from {table}", db.get_engine(bind="data")).index)

# generate bar plot for number of all entries
def generateNumOfEntriesPlot(navigationTabs):
	#set up plot theme
	plt.style.use("seaborn-deep")
	colours=sns.color_palette("deep").as_hex()
	catColours={"metabolic":colours[0], "proteomic":colours[1], "biophysical":colours[2]}

	#create dict of dicts as container for stat values
	tableCounts=pd.DataFrame(columns=["colour","display", "count", "url"])	
	for category in navigationTabs.keys():
		for table in navigationTabs[category]["tables"]:
			tableCounts.loc[len(tableCounts)]={"colour":catColours[category], "display":displayColumnNames[table], "count":CountEntriesInTable(table), "url":url_for("main.results", category=category, table=table)}
	
	# do the plot	
	fig, ax = plt.subplots(figsize=(20,10))
	bars=ax.bar(tableCounts["display"], height=tableCounts["count"], color=tableCounts["colour"])
	ax.set_yscale("log")
	for rect, label in zip(ax.patches, tableCounts["count"]):
		ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height()*10**(-.17), label, size=13, color="w", ha='center', va='bottom')
	for bar, url in zip(bars, tableCounts["url"]):
		bar.set_url(url)
	ax.set_xticklabels(tableCounts["display"], rotation=45, ha="right", size=15)
	ax.set_ylabel("Number of Entries", size=20)
	ax.set_yticks([])
	ax.grid(False)
	fig.tight_layout()

	return fig
