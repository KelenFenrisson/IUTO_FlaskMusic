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
    from .models import Artiste,Album,Avoir_genre,Genre

    #Création des artistes
    artistes = {}
    for album in albums:
        artiste = album["by"]
        if artiste not in artistes:
            art = Artiste(nom_artiste=artiste)
            db.session.add(art)
            artistes[a] = art
    db.session.commit()

	#Création des Genres
    genres = {}
    for album in albums:
        genre = album["genre"]
		for elem in genre:
	        if genre not in genres:
	            gen = Genre(nom_genre=genre)
	            db.session.add(gen)
	            genres[a] = gen
    db.session.commit()

    # création de tous les albums
    for album in albums:
        artiste = artistes[album["by"]]
        o = Book(id_album = album["entryId"],
				 titre_album = album["title"],
                 annee_album = album["releaseYear"],
                 img_album   = album["img"],
                 id_artiste   = album["by"])
        db.session.add(o)
    db.session.commit()

	#Création des Avoir_genre
	for album in albums:
		avoirGenre = album["genre"]
		for elem in avoirGenre:
			avoir = Avoir_genre(id_album=album["entryId"],nom_genre=elem)
			db.session.add(avoir)
	db.session.commit()
