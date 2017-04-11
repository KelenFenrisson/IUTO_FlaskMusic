from .app import app,db
from flask import render_template,url_for,redirect,request
from .models import User,Album,Artiste,Genre,get_artistes,get_albums,get_genres,Album_Genre

SITENAME="FL45K-MU51C"

@app.route("/")
def home():
	return render_template("home.html",title=SITENAME, pagetitle="Accueil")

########################### ARTISTES ##########################################
@app.route("/artist/list <string:msg>")
def artist_list(msg):
	return render_template("artist-list.html", title=SITENAME, pagetitle="Liste des artistes" ,message=msg , l_artists=get_artistes())

@app.route("/artist/add")
def artist_add():
	return render_template("artist-form.html", title=SITENAME, pagetitle="Ajouter un nouvel artiste" ,msg="" , l_artists=[])

@app.route("/artist/update")
def artist_update():
	return render_template("artist-form.html", title=SITENAME, pagetitle="Modifier les informations d'un artiste" ,msg="" , l_artists=[])

@app.route("/artist/save")
def artist_save():
	msg="Artiste non enregistré"
	return redirect(url_for("artist_list", msg=msg))

@app.route("/artist/delete")
def artist_delete():
	return render_template("artist-list.html", title=SITENAME, pagetitle="Liste des artistes" ,msg="" , l_artists=[])

# ########################### ALBUMS ############################################
# @app.route("/album/list")
# def artist_list():
# 	return render_template("artist-list.html",title=SITENAME,pagetitle="Liste des albums", l_artists=[])
#
# ########################### GENRES ############################################
#
# @app.route("/genre/list")
# def artist_list():
# 	return render_template("artist-list.html",title=SITENAME,pagetitle="Liste des genres", l_artists=[])
