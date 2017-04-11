from .app import app,db
from flask import render_template,url_for,redirect,request
from .models import User,Album,Artiste,Genre,get_artistes,get_albums,get_genres,Album_Genre,get_albums_par_artiste,get_albums_par_genre
from flask_login import login_user, current_user, logout_user,login_required
from .form import LoginForm

SITENAME="FL45K-MU51C"

@app.route("/")
def home():
	return render_template("home.html",title=SITENAME, pagetitle="Accueil")

########################### ARTISTES ##########################################
@app.route("/artist/list")
def artist_list():
	return render_template("artist-list.html", title=SITENAME, pagetitle="Liste des artistes"  , l_artists=get_artistes())

@app.route("/artist/add")
@login_required
def artist_add():
	return render_template("artist-form.html", title=SITENAME, pagetitle="Ajouter un nouvel artiste" ,msg="" , l_artists=[])

@app.route("/artist/update")
@login_required
def artist_update():
	return render_template("artist-form.html", title=SITENAME, pagetitle="Modifier les informations d'un artiste" ,msg="" , l_artists=[])

@app.route("/artist/save")
@login_required
def artist_save():
	msg="Artiste non enregistré"
	return redirect(url_for("artist_list", msg=msg))

@app.route("/artist/delete")
@login_required
def artist_delete():
	return render_template("artist-list.html", title=SITENAME, pagetitle="Liste des artistes" ,msg="" , l_artists=[])


########################### AUTHENTIFICATION ##########################################

@app.route("/login/", methods=("GET","POST",))
def login():
	f=LoginForm()
	if not f.is_submitted():
		f.next.data = request.args.get("next")
	elif f.validate_on_submit():
		user = f.get_authenticated_user()
		if user:
			login_user(user)
			next = f.next.data or url_for("home")
			return redirect(next)
	return render_template("login.html",form=f)

@app.route("/logout/")
def logout():
	logout_user()
	return redirect(url_for('home'))

# ########################### ALBUMS ############################################
@app.route("/album/list")
def album_list():
	return render_template("album-list.html",title=SITENAME,pagetitle="Liste des albums", l_albums=get_albums())

@app.route("/album/by/artist <string:artist_id>")
def album_list_by_artist(artist_id):
	a=Artiste.query.get(artist_id)
	return render_template("album-list.html",title=SITENAME,pagetitle="Liste des albums de {0}".format(a.nom_artiste), l_albums=get_albums_par_artiste(a.id_artiste))

@app.route("/album/by/genre <string:genre>")
def album_list_by_genre(genre):
	return render_template("album-list.html",title=SITENAME,pagetitle="Liste des albums", l_albums=get_albums_par_genre(genre))


# ########################### GENRES ############################################
#
# @app.route("/genre/list")
# def artist_list():
# 	return render_template("artist-list.html",title=SITENAME,pagetitle="Liste des genres", l_artists=[])
