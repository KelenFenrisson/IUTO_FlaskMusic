import yaml,os.path
from application import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))

    def get_id(self):
        return self.username

class Album(db.Model):
	id_album = db.Column(db.Integer,primary_key=True)
	titre_album = db.Column(db.String(50))
	annee_album = db.Column(db.Integer)
	img_album = db.Column(db.String(100))
	id_artiste = db.Column(db.Integer,db.ForeignKey("artiste.id_artiste"))
	artiste = db.relationship("Artiste",backref=db.backref("albums",lazy="dynamic"))

	def __repr__(self):
		return "<Album (%d) %s>" %(self.id, self.title_album)

class Artiste(db.Model):
	id_artiste = db.Column(db.Integer, primary_key=True)
	nom_artiste = db.Column(db.String(100))

	def __repr__(self):
		return "<Artiste (%d) %s>" %(self.id, self.name)

class Genre(db.Model):
	nom_genre = db.Column(db.String(100), primary_key=True)

	def __repr__(self):
		return "<Genre %s >" %(self.nom_genre)

class Avoir_genre(db.Model):
	id_genre = db.Column(db.Integer, primary_key=True)
	id_album = db.Column(db.Integer,db.ForeignKey("album.id_album"))
	nom_genre = db.Column(db.String(100),db.ForeignKey("genre.nom_genre"))
	id_album = db.relationship("Album",backref=db.backref("genres",lazy="dynamic"))
	nom_genre = db.relationship("Genre",backref=db.backref("albums",lazy="dynamic"))
