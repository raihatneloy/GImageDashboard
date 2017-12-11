#!/usr/bin/env python

def users_model(db):
	favorite_images = db.Table(
			'favorite_images',
			db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
			db.Column('image_id', db.Integer, db.ForeignKey('images.id'))
		)

	pinned_pages = db.Table(
			'pinned_pages',
			db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
			db.Column('page_id', db.Integer, db.ForeignKey('pages.id'))
		)

	class Users(db.Model):
		__tablename__ = 'users'
		id = db.Column('id', db.Integer, primary_key=True)
		username = db.Column('username', db.String(100))
		name = db.Column('name', db.String(100))
		email = db.Column('email', db.String(100))
		password = db.Column('password', db.String(100))
		favorites = db.relationship("Images",
						secondary=favorite_images
					)
		pages = db.relationship("Pages",
						secondary=pinned_pages
					)
		fbuser = db.relationship('FBUser',
						backref='fbusers'
					)

		def __init__(self, username, name, email, password):
			self.username = username
			self.name = name
			self.email = email
			self.password = password

	return Users, favorite_images, pinned_pages


def add_new_user(db, Users, data):
	username = data.get('username')
	name = data.get('name')
	email = data.get('email')
	password = data.get('password')

	check_user = Users.query.filter(Users.username == username).all()
	
	if len(check_user) > 0:
		return {"Error": "Username already exists"}

	check_user = Users.query.filter(Users.email == email).all()

	if len(check_user) > 0:
		return {"Error": "This email is already registered"}

	new_user = Users(username, name, email, password)
	db.session.add(new_user)
	db.session.commit()

	return {"Success" : "User registered"}