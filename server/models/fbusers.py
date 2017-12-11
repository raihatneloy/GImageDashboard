#!/usr/bin/env python

def fbuser_model(db):
    class FBUser(db.Model):
        __tablename__ = 'fbusers'
        id = db.Column('id', db.Integer, primary_key=True)
        name = db.Column('name', db.String(1000))
        fbid = db.Column('fbid', db.String(1000))
        access_token = db.Column('access_token', db.String(1000))
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

        def __init__(self, name, fbid, access_token):
            self.name = name
            self.fbid = fbid
            self.access_token = access_token

    return FBUser