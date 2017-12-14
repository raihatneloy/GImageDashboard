#!/usr/bin/env python

def flickr_model(db):
    class Flickr(db.Model):
        __tablename__ = 'flickr'
        id = db.Column('id', db.Integer, primary_key=True)
        name = db.Column('name', db.String(1000))
        username = db.Column('username', db.String(1000))
        picture = db.Column('picture', db.String(1000))
        flickr_id = db.Column('flickr_id', db.String(1000))
        follower = db.Column('follower', db.String(1000))

        def __init__(self, name, username, picture, flickr_id, follower):
            self.name = name
            self.username = username
            self.picture = picture
            self.flickr_id = flickr_id
            self.follower = follower

    return Flickr

def add_new_flickr(db, Flickr, data):
    name = data.get('name')
    username = data.get('username')
    picture = data.get('picture')
    flickr_id = data.get('flickr_id')
    follower = data.get('follower')

    check_flickr = Flickr.query.filter(Flickr.flickr_id == flickr_id).all()

    if len(check_flickr) > 0:
        return {"Error": "Flickr user already in database"}

    new_flickr = Flickr(name, username, picture, flickr_id, follower)
    db.session.add(new_flickr)
    db.session.commit()

    return {"Success": "Flick user saved"}

def get_flickr(db, Flickr, data):
    add_new_flickr(db, Flickr, data)

    return Flickr.query.filter(Flickr.flickr_id == data.get('flickr_id')).first()