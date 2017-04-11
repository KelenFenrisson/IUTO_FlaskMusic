from .app import app,manager,db,login_manager
import application.views
import application.commands
from .models import User,Album,Artiste,Genre,get_artistes,get_albums,get_genres,Album_Genre
