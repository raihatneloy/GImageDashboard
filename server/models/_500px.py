#!/usr/bin/env python

def _500px_model(db):
    class _500px(db.Model):
        __tablename__ = '_500px'
        id = db.Column('id', db.Integer, primary_key=True)
        username = db.Column('username', db.String(1000))
        name = db.Column('name', db.String(1000))
        _500pxid = db.Column('_500pxid', db.String(1000))
        picture = db.Column('picture', db.String(1000))
        cover = db.Column('cover', db.String(1000))

        def __init__(self, name, username, _500pxid, picture, cover):
            self.name = name
            self.username = username
            self._500pxid = _500pxid
            self.picture = picture
            self.cover = cover
    
    return _500px

def add_new_500px(db, _500px, data):
    name = data.get('name')
    _500pxid = data.get('_500pxid')
    username = data.get('username')
    picture = data.get('picture')
    cover = data.get('cover')

    check_500px = _500px.query.filter(_500px._500pxid == _500pxid).all()

    if len(check_500px) > 0:
        return {'Error': '500px user already in database'}

    new_500px = _500px(name, username, _500pxid, picture, cover)
    db.session.add(new_500px)
    db.session.commit()

    return {'Success': 'User saved'}

def get_500px(db, _500px, data):
    x = add_new_500px(db, _500px, data)
    print x

    return _500px.query.filter(_500px._500pxid == data.get('_500pxid')).first()