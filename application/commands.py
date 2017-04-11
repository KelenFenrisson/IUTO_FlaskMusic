from .app import manager, db

# création des tables
@manager.command
def syncdb():
	db.create_all()

# Ajout d'un nouvel utilisateur
@manager.command
def newUser(username,password):
	from .models import User
	from hashlib import sha256
	m = sha256()
	m.update(password.encode())
	u = User(username=username , password=m.hexdigest())
	db.session.add(u)
	db.session.commit()

# Modification du mot de passe
@manager.command
def changePass(username,oldpassword,newpassword):
	from .models import User
	from hashlib import sha256
	old = sha256()
	old.update(oldpassword.encode())
	u = User.query.get(username)
	if old.hexdigest()==u.password:
		new = sha256()
		new.update(newpassword.encode())
		u.password = new.hexdigest()
		db.session.commit()
		print("Votre mot de passe est bien modifié")
	else:
		print("Votre ancien mot de passe est incorrect")


@manager.command
def loaddb(filename):
	# création de toutes les tables
	db.create_all()

	import yaml
	albums = yaml.load(open(filename))

	# import des modèles
	from .models import User,Album,Artiste,Genre,get_artistes,get_albums,get_genres,Album_Genre

	artistes=set()
	genres=set()
	artiste = None
	genre = None
	for album in albums:

		#Création des artistes
		nom_artiste = album["by"]
		artiste = Artiste(nom_artiste=nom_artiste)
		if nom_artiste not in artistes:
			db.session.add(artiste)
			db.session.commit()
			artistes.add(nom_artiste)


		# création de tous les albums
		o = Album(id_album = album["entryId"],
		titre_album = album["title"],
		annee_album = album["releaseYear"],
		img_album   = album["img"],
		id_artiste   = album["by"])
		db.session.add(o)
		db.session.commit()


		#Création des Genres
		nom_genre = album["genre"]
		id_album= album["entryId"]

		for elem in nom_genre:
			elem = elem.capitalize()
			genre = Genre(nom_genre=elem)
			if elem not in genres:
				db.session.add(genre)
				db.session.commit()
				genres.add(elem)
			album_genre = Album_Genre(id_album = id_album , nom_genre = elem)
			db.session.add(album_genre)
			db.session.commit()
