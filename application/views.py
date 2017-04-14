from flask import render_template, url_for, redirect, request
from flask_login import login_user, logout_user, login_required
from sqlalchemy import and_

from .app import app, db
from .form import LoginForm, NewUserForm, AlbumForm
from .models import User, Artiste, Genre, get_artistes, get_albums, get_albums_par_artiste, get_albums_par_genre, \
	get_genres, \
	ajouter_album, ajouter_album_genre, ajouter_genre, Album_Genre, Album, modifier_album

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


@app.route("/album/new/")
@login_required
def album_add():
	f = AlbumForm()
	genres = Genre.query.all()
	f.genres.choices = [(i, genres[i]) for i in range(0, len(genres))]
	mapping = dict((i, Genre.query.get(genres[i].nom_genre)) for i in range(len(genres)))
	return render_template("album-form.html", form=f, genres_dispos=mapping, artistes=Artiste.query.all())

@app.route("/album/update/<int:id>")
@login_required
def album_update(id):

	# On recupere l'album et ses genres
	a = Album.query.get(id)
	a_genres = [ag.nom_genre for ag in Album_Genre.query.filter(Album_Genre.id_album==a.id_album).all()]
	# On créée un formulaire et on dresse la liste des genres disponibles pour les cases à cocher
	f = AlbumForm()
	genres = Genre.query.all()
	mapping = dict((i, Genre.query.get(genres[i].nom_genre)) for i in range(len(genres)))
	f.genres.choices = [(i, genres[i]) for i in range(0, len(genres))]
	# On garde le referencement des genres dans un dico
	mapping = dict((i, Genre.query.get(genres[i].nom_genre)) for i in range(len(genres)))
	# On préremplit les champs du formulaire avec les données de l'instance d'Album a modifier
	f.album_id.data=a.id_album
	f.title.data=a.titre_album
	f.artist.data = a.artiste.nom_artiste
	f.releaseyear.data=a.annee_album
	f.img.data=a.img_album
	# Pour les genres, in recupère la clé du dico pour les genres de l'album pour précocher les cases
	f.genres.data = [key for (key,genre) in mapping.items() if genre.nom_genre in a_genres]

	return render_template("album-form.html", form=f, genres_dispos=mapping, artistes=Artiste.query.all())


@app.route("/album/save/", methods=("GET", "POST",))
@login_required
def album_save():
	f=AlbumForm()
	genres = Genre.query.all()
	mapping = dict((i, Genre.query.get(genres[i].nom_genre)) for i in range(len(genres)))
	print(f.genres.data, [mapping[g] for g in f.genres.data])

	print("Route OK erreurs={0}".format(f.errors, f.validate()),
		  "Titre album {0}valide".format( "non "*(not f.title.validate(f))),
		  "Année de sortie {0}valide".format( "non "*(not f.releaseyear.validate(f))),
		  "Artiste {0}valide".format( "non "*(not f.artist.validate(f))),
		  "Image {0}valide".format( "non "*(not f.img.validate(f))),
		  "Genres {0}valide".format( "non "*(not f.genres.validate(f))),
		  "Nouveau genre {0}valide".format( "non "*(not f.genre_add.validate(f))),
		  sep="\n")
	#f.validate_on_submit():
	if True:
		print('Validation OK')
		album=None


		if f.album_id.data!="":
			# Si l'id de l'abum est défini, c'est une modification
			album = modifier_album(f.album_id.data, f.title.data, f.releaseyear.data, f.img.data, f.get_artist_id())
			print('Modification album {0}'.format(album), album.id_album)


		else :
			#sinon, c'est l'ajout d'un nouvel album
			# On rajoute l'album dans la BDD
			album = ajouter_album(f.title.data, f.releaseyear.data, f.img.data, f.get_artist_id())
			print('Ajout album {0}'.format(album), album.id_album)

		# On associe l'album aux genres enregistrés par l'utilisateur
		if f.genre_add != "":
			new_genre = ajouter_genre(f.genre_add.data.capitalize())
			ajouter_album_genre(album.id_album, new_genre.nom_genre)
			print("Nouveau Genre ajouté")

		for g in f.genres.data:
			if Album_Genre.query.filter(and_(Album_Genre.id_album==f.album_id.data,
											 Album_Genre.nom_genre==mapping[g].nom_genre)).first() is None:

				ajouter_album_genre(album.id_album, mapping[g].nom_genre)

	next = f.next.data or url_for("album_list")
	return redirect(next)


