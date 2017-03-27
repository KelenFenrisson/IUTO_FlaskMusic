from .app import app,db
from flask import render_template,url_for,redirect,request


@app.route("/")
def home():
	return render_template("home.html",title="Music !!!",)
