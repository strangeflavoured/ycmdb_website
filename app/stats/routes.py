from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.ext.serializer import dumps
import pandas as pd
pd.options.mode.chained_assignment=None
import os, subprocess, pickle

from app import db
from app.stats import bp
from app.general import userIsAdmin, userConfirmed, figureToSvg, navigation
from app.stats.forms import RefreshForm
from app.stats.stats import generateNumOfEntriesPlot, makeMediumPlotAndConversion, getPublicationInfo
from app.model._data_columns import navigationTabs, primaryIdentifier
from app.model.models import User

statsFolder=current_app.config["BASEDIR"]+"/app/stats"
ForMediumPlot=pickle.load(open(statsFolder+"/Media.pkl", "rb"))
publicationStats=pickle.load(open(statsFolder+"/Publications.pkl", "rb"))["all_pubs"]

@bp.route("/refresh", methods=["GET","POST"])
@login_required
def refreshContent():
	form=RefreshForm()
	if userIsAdmin():
		if request.method=="POST":
			if form.index.data:				
				fig=generateNumOfEntriesPlot(navigationTabs)
				StatsPlot=figureToSvg(fig).decode("utf-8")
				svgFile=os.path.join(current_app.root_path, 'static', 'images', 'DatabaseStats.svg')
				with open(svgFile, "w+") as file:
					file.write(StatsPlot)
				flash("Refreshed index stats", "info")
			if form.medium.data:
				global ForMediumPlot
				ForMediumPlot=makeMediumPlotAndConversion()	
				flash("Refreshed medium stats", "info")	
			if form.count.data:
				try:
					with open(statsFolder+"/UpdateRELATIONcounters.out", "w+") as file:    	
						subprocess.run([current_app.config["RSCRIPT"], "--vanilla", statsFolder+"/UpdateRELATIONcounters.R", current_app.config["DB_NAME"],  current_app.config["DB_HOST"],  current_app.config["DB_USER"],  current_app.config["DB_PASSWORD"]], stdout=file, check=True)
					flash("Refreshed RELATION counts", "info")
				except subprocess.CalledProcessError:
					flash("RELATION counts could not be refreshed", "warning")
			if form.publication.data:
				global publicationStats
				publicationStats=getPublicationInfo(primaryIdentifier.keys())
				flash("Refreshed publication stats", "info")
		return render_template("stats/refresh.html", admin=userIsAdmin(), form=form, navigation=navigation, confirmed=userConfirmed())
	else:
		return redirect(url_for("main.index"))
