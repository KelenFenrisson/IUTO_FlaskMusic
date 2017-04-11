import yaml,os.path
from application import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))

    def get_id(self):
        return self.username

# album_genres = db.Table('album_genres',
#     db.Column('nom_genre', db.Integer, db.ForeignKey('genre.nom_genre')),
#     db.Column('album_id', db.Integer, db.ForeignKey('album.id_album'))
# )

class Album_Genre(db.Model):
	id_album_genre = db.Column(db.Integer,primary_key=True)
	id_album = db.Column(db.Integer,db.ForeignKey("album.id_album"))
	nom_genre = db.Column(db.String,db.ForeignKey("genre.nom_genre"))
	album=db.relationship("Album",backref=db.backref("album_genre",lazy="dynamic"))
	genre=db.relationship("Genre",backref=db.backref("album_genre",lazy="dynamic"))

class Album(db.Model):
	id_album = db.Column(db.Integer,primary_key=True)
	titre_album = db.Column(db.String(50))
	annee_album = db.Column(db.Integer)
	img_album = db.Column(db.String(100))
	id_artiste = db.Column(db.Integer,db.ForeignKey("artiste.id_artiste"))
	artiste = db.relationship("Artiste",backref=db.backref("albums",lazy="dynamic"))

	def __repr__(self):
		return "<Album (%d) %s>" %(self.id_album, self.titre_album)

class Artiste(db.Model):
	id_artiste = db.Column(db.Integer, primary_key=True)
	nom_artiste = db.Column(db.String(100))

	def __repr__(self):
		return "<Artiste (%d) %s>" %(self.id_artiste, self.nom_artiste)

class Genre(db.Model):
	nom_genre = db.Column(db.String(100), primary_key=True)

	def __repr__(self):
		return "<Genre %s >" %(self.nom_genre)

def get_artistes():
    return Artiste.query.all()

def get_albums():
    return Album.query.all()

def get_genres():
	return Genre.query.all()
