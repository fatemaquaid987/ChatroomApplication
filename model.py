from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	# attributes
	user_id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(24), nullable=False)
	email = db.Column(db.String(80), nullable=False)
	pw_hash = db.Column(db.String(64), nullable=False)
	chatroom_joined = db.Column(db.Integer, db.ForeignKey('chatroom.chatroom_id'), nullable=True)
	messages = db.relationship('Message', backref='author')
	chatroom = db.relationship('Chatroom', backref = 'createdby', foreign_keys = 'Chatroom.createdby_id')

	def __init__(self, username, email, pw_hash):
		self.user_name = username
		self.email = email
		self.pw_hash = pw_hash

	def __repr__(self):
		return '<User {}>'.format(self.user_name)

class Message(db.Model):
	message_id = db.Column(db.Integer, primary_key=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
	chatroom_id = db.Column(db.Integer, db.ForeignKey("chatroom.chatroom_id", ondelete='CASCADE'), nullable=False)
	chatrooms = db.relationship('Chatroom', backref = db.backref('messages', passive_deletes=True))
	text = db.Column(db.Text, nullable=False)
	

	def __init__(self, author_id, chatroom_id, text):
			self.author_id = author_id
			self.chatroom_id = chatroom_id
			self.text = text

	def __repr__(self):
			return '<Message {}'.format(self.message_id)



class Chatroom(db.Model):
	chatroom_id = db.Column(db.Integer, primary_key=True)
	chatroom_name = db.Column(db.String(24), nullable=False)
	createdby_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
	messages_in = db.relationship('Message', backref='inchatroom')
	users = db.relationship('User', backref='joinedchatroom', foreign_keys = 'User.chatroom_joined')

	def __init__(self, name, createdby_id):
			self.chatroom_name = name;
			self.createdby_id = createdby_id
			

	def __repr__(self):
			return '<Chatroom {}'.format(self.chatroom_id)



