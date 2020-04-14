import time
import os
import json
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

from model import db, User, Message, Chatroom
from datetime import datetime as dt

app = Flask(__name__)

# configuration
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'chat.db')

app.config.from_object(__name__)
#app.config.from_envvar('MINITWIT_SETTINGS', silent=True)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #here to silence deprecation warning

db.init_app(app)


@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	db.create_all()
	print('Initialized the database.')
	

def get_user_id(username):
	"""Convenience method to look up the id for a username."""
	rv = User.query.filter_by(user_name=username).first()
	return rv.user_id if rv else None


@app.route("/")
def default():
	return redirect(url_for("login_controller"))
	
@app.route("/login/", methods=["GET", "POST"])
def login_controller():
	# first check if the user is already logged in
	#session.clear()
	#if user is in session and requests this page, it means that user has not joined any chatroom
	if "user_id" in session:
		flash("Already logged in!")
		return redirect(url_for("profile", username=session["user_name"]))

	# if not, and the incoming request is via POST try to log them in
	elif request.method == "POST":
		#if action is login
		if request.form['btn'] == "login":
			#user
			user = User.query.filter_by(user_name=request.form['user']).first()
			
			
			#if user is in database
			if user is not None:
				#if password matches
				if check_password_hash(user.pw_hash, request.form['pass']):
					session["user_id"] = user.user_id
					session["user_name"] = user.user_name
					flash("User successfully logged in!")
					return redirect(url_for("profile", username=session["user_name"]))
				else:
					flash("Invalid password")
				
			
			else:
				flash("Invalid username")
		#if action is signup
		else:
			if not request.form['user']:
				flash('You have to enter a username')
				return render_template("loginPage.html")
			elif not request.form['email'] or \
					'@' not in request.form['email']:
				flash('You have to enter a valid email address')
				return render_template("loginPage.html")
			elif not request.form['pass']:
				flash('You have to enter a password')
				return render_template("loginPage.html")
			elif not request.form['pass2']:
				flash('You have to re-enter the password')
				return render_template("loginPage.html")
			#if name is already in customer table
			user = User.query.filter_by(user_name=request.form['user']).first()
			if user is not None:
				flash("Username already taken!")
				return render_template("loginPage.html")
			elif request.form['pass2'] != request.form['pass']:
				flash("Passwords don't match")
				return render_template("loginPage.html")
			#else add user to the customer table
			else:
				db.session.add(User(request.form['user'], request.form['email'], generate_password_hash(request.form['pass'])))
				db.session.commit()
				flash('You succesfully signed up and can login now')
				return redirect(url_for("login_controller"))
			
			       
			
	       

	# if all else fails, offer to log them in
	return render_template("loginPage.html")
    
@app.route("/profile/")
def profiles():
	#if user is in session and requests this page, it means that user has not joined any chatroom
	if "user_id" in session:
		user = User.query.filter_by(user_id = get_user_id(session["user_name"])).first()
		user.chatroom_joined = None
	return render_template("profiles.html", users=User.query.all())

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username=None):
	
	if not username:
		return redirect(url_for("profiles"))
	user = User.query.filter_by(user_name=username).first()
	
	#if user is in database
	if user is not None:
		# if specified, check to handle users looking up their own profile
		if "user_id" in session:
			#if user is in session and requests this page, it means that user has not joined any chatroom
			user= User.query.filter_by(user_id = get_user_id(session["user_name"])).first()
			user.chatroom_joined = None
			if session["user_name"] == username:
				chatrooms_created = Chatroom.query.filter_by(createdby_id = user.user_id).all()
				chatroom_joined = Chatroom.query.filter_by(chatroom_id = user.chatroom_joined).first()
				can_join = Chatroom.query.all()
				if request.method == "POST":
					if request.form["btn"] == "submit":
						if not request.form['chatroomname']:
							flash("Please enter a chatroom name  to register!")
							return render_template("curProfile.html",  can_join = can_join, joined = chatroom_joined, created = chatrooms_created)
						
						chatroom = Chatroom.query.filter_by(chatroom_name=request.form["chatroomname"]).first()
						#check if chatroom name already exists 
						if chatroom is not None:
							flash("Chatroom name already taken!")
							return render_template("curProfile.html", can_join = can_join, joined = chatroom_joined, created = chatrooms_created)
						
						#else add chatroom entry into the table
						else:
							db.session.add(Chatroom(request.form['chatroomname'], user.user_id))
							db.session.commit()
							
							flash("Chatroom successfully created")
							return redirect(url_for("profile", username=session["user_name"]))
					else:
						chatroom = Chatroom.query.filter_by(chatroom_name = request.form["btn"]).first()
						Chatroom.query.filter_by(chatroom_name = request.form["btn"]).delete()
						db.session.commit()
						Message.query.filter_by(chatroom_id = chatroom.chatroom_id).delete()
						db.session.commit()
						flash("Chatroom succesfully deleted")
						return redirect(url_for("profile", username = session["user_name"]))
				
				return render_template("curProfile.html",  can_join = can_join, joined = chatroom_joined, created = chatrooms_created)
				#display chatrooms that can be joined, already joined and created 
		
		return render_template("otherProfile.html", name = username)
	
	else:
		# cant find profile
		abort(404)
@app.route("/chatroom/")
def all_chatrooms():
	#if user is in session and requests this page, it means that user has not joined any chatroom
	if "user_id" in session:
		user= User.query.filter_by(user_id = get_user_id(session["user_name"])).first()
		user.chatroom_joined = None
	return render_template("chatrooms.html", chatrooms=Chatroom.query.all())


@app.route("/new_message", methods = ["POST"])
def add_new_message():
	chatroom = Chatroom.query.filter_by(chatroom_id = request.form["chatroom"]).first()
	#if chatorom exists, post message. else redirect to profile
	db.session.add(Message(get_user_id(session["user_name"]), Chatroom.query.filter_by(chatroom_id = request.form["chatroom"]).first().chatroom_id, request.form["message"]))
	db.session.commit()
	return "OK!"
	

@app.route("/items", methods = ["POST"])
def get_items():
	#if user is in session and requests this page, it means that user has not joined any chatroom
	if "user_id" in session:
		user= User.query.filter_by(user_id = get_user_id(session["user_name"])).first()
		user.chatroom_joined = None
	
	message_objects = Message.query.filter_by(chatroom_id = request.form["chatroom"]).all()
	messages = [[m.text, User.query.filter_by(user_id = m.author_id).first().user_name] for m in message_objects]
	
	return json.dumps(messages)

@app.route("/chatroom/<chatroomname>", methods = ["GET", "POST"])
def chat(chatroomname=None):
	#chatroom name not specified
	if not chatroomname:
		return redirect(url_for("all_chatrooms"))
	chatroom = Chatroom.query.filter_by(chatroom_name=chatroomname).first()
	    
	#chatroom name specified and in chatrooms
	if chatroom is not None:
		# check if method is post
		if request.method == "POST":
			if "user_id" in session:
				#chatroom left
				if request.form["btn"] == "leave chat room":
					user = User.query.filter_by(user_name=session["user_name"]).first()
					user.chatroom_joined = None
					db.session.commit()
					flash("Chatroom succesfully left")
					return redirect(url_for("profile", username = session["user_name"]))
					
		#if method is not post		
		else:
			if "user_id" in session:
				#joined chatroom
				user = User.query.filter_by(user_name=session["user_name"]).first()
				user.chatroom_joined = chatroom.chatroom_id
				db.session.commit()
				flash("Chatroom succesfully joined")
				return render_template("chatPage.html", chatroom = chatroom, user_name = session["user_name"])
			
		return render_template("chatPage.html", chatroom = chatroom)
	else:
		# cant find chatroompage
		abort(404)
		    

@app.route("/logout/")
def unlogger():
	# if logged in, log out, otherwise offer to log in
	if "user_id" in session:
		user= User.query.filter_by(user_id = get_user_id(session["user_name"])).first()
		user.chatroom_joined = None
		# note, here were calling the .clear() method for the python dictionary builtin
		session.clear()
		# flashes are stored in session["_flashes"], so we need to clear the session /before/ we set the flash message!
		flash("Successfully logged out!")
		# we got rid of logoutpage.html!
		return redirect(url_for("login_controller"))
	else:
		flash("Not currently logged in!")
		return redirect(url_for("login_controller"))

# needed to use sessions
# note that this is a terrible secret key

app.secret_key = "this is a terrible secret key"
			
if __name__ == "__main__":
	app.run()

