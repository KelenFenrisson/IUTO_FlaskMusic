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
def changepass(username,oldpassword,newpassword):
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
    else:
        print("Votre ancien mot de passe est incorrect")
