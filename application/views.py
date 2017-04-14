from flask import render_template, url_for, redirect, request
from flask_login import login_user, logout_user, login_required

from .app import app, db
from .form import LoginForm, NewUserForm, AlbumForm
from .models import User, Artiste, Genre, get_artistes, get_albums, get_albums_par_artiste, get_albums_par_genre, get_genres,\
	ajouter_album, ajouter_album_genre, ajouter_genre

SITENAME = "FL45K-MU51C"

########################### ACCUEIL ##########################################
@app.route("/")
def home():
	return render_template("album-list.html", title=SITENAME, pagetitle="Accueil", l_albums=get_albums())

########################### ARTISTES ##########################################
@app.route("/artist/list")
def artist_list():
	return render_template("artist-list.html", title=SITENAME, pagetitle="Liste des artistes", l_artists=get_artistes())

########################### GENRES ##########################################
@app.route("/genre/list")
def genre_list():
	return render_template("genre-list.html", title=SITENAME, pagetitle="Liste des genres", l_genres=get_genres())

########################### AUTHENTIFICATION ##########################################

@app.route("/login/", methods=("GET", "POST",))
def login():
	f = LoginForm()
	if not f.is_submitted():
		f.next.data = request.args.get("next")
	elif f.validate_on_submit():
		user = f.get_authenticated_user()
		if user:
			login_user(user)
			next = f.next.data or url_for("home")
			return redirect(next)
	return render_template("login.html", form=f)


@app.route("/logout/")
def logout():
	logout_user()
	return redirect(url_for('home'))


# ########################### NEW USER #########################################
@app.route("/user/new/", methods=("GET", "POST",))
def create_account():
	f = NewUserForm()
	if not f.is_submitted():
		f.next.data = request.args.get("next")
	elif f.validate_on_submit():
		from hashlib import sha256
		m = sha256()
		m.update(f.password.data.encode())
		user = User(username=f.username.data, password=m.hexdigest())
		if user:
			db.session.add(user)
			db.session.commit()
			login_user(user)
			next = f.next.data or url_for("home")
			return redirect(next)
	return render_template("usercreation-form.html", form=f)


# ########################### ALBUMS ###########################################
@app.route("/album/list")
def album_list():
	return render_template("album-list.html", title=SITENAME, pagetitle="Liste des albums", l_albums=get_albums())


@app.route("/album/by/artist <string:artist_id>")
def album_list_by_artist(artist_id):
	a = Artiste.query.get(artist_id)
	return render_template("album-list.html", title=SITENAME, pagetitle="Liste des albums de {0}".format(a.nom_artiste),l_albums=get_albums_par_artiste(a.id_artiste))


@app.route("/album/by/genre <string:genre>")
def album_list_by_genre(genre):
	return render_template("album-list.html", title=SITENAME, pagetitle="Liste des albums",l_albums=get_albums_par_genre(genre))


@app.route("/album/new/", methods=("GET", "POST",))
@login_required
def album_add():
	f = AlbumForm()
	genres = Genre.query.all()
	f.genres.choices = [(i, genres[i]) for i in range(0, len(genres))]
	mapping = dict((i, Genre.query.get(genres[i].nom_genre)) for i in range(len(genres)))


	print("Route OK erreurs={0}".format(f.errors, f.validate()),
		  "Titre album valide"*f.title.validate(f),
		  "Année de sortie valide" * f.releaseyear.validate(f),
		  "Artiste valide" * f.artist.validate(f),
		  "Image valide" * f.img.validate(f),
		  "Genres valides"* f.genres.validate(f),
		  "Nouveau genre valide" * f.genre_add.validate(f), sep="\n")

	if not f.is_submitted():
		print('Not Submitted OK', request.args.get("next"))
		f.next.data = request.args.get("next")

	elif f.validate_on_submit():
		print('Validation OK')

		# On rajoute l'album dans la BDD
		album=ajouter_album(f.title.data, f.releaseyear.data, f.img.data, f.get_artist_id())
		print('Ajout album {0}'.format(album), album.id_album)

		# On associe l'album aux genres enregistrés par l'utilisateur
		if f.genre_add:
			new_genre = ajouter_genre(f.genre_add.data.capitalize())
			print(new_genre.nom_genre)
			ajouter_album_genre(album.id_album, new_genre.nom_genre)
			print("Nouveau Genre ajouté")

		for g in f.genres.data:
			ajouter_album_genre(album.id_album, mapping[g].nom_genre)

		next = f.next.data or url_for("album_list")
		return redirect(next)

	return render_template("album-form.html", form=f, genres_dispos=mapping, artistes=Artiste.query.all())
