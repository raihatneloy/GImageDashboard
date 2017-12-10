#!/usr/bin/env python

def pages_model(db):
    class Pages(db.Model):
        __tablename__ = 'pages'
        id = db.Column('id', db.Integer, primary_key=True)
        name = db.Column('name', db.String(1000))
        page_id = db.Column('page_id', db.String(1000))
        cover = db.Column('cover', db.String(1000))
        picture = db.Column('picture', db.String(1000))

        def __init__(self, name, page_id, cover, picture):
            self.name = name
            self.page_id = page_id
            self.cover = cover
            self.picture = picture

    return Pages

def add_new_page(db, Pages, data):
    name = data.get('name')
    page_id = data.get('id')
    cover = data.get('cover')
    picture = data.get('picture')

    check_page = Pages.query.filter(Pages.page_id == page_id).all()

    if len(check_page) > 0:
        return {"Error": "Page already in database"}

    new_page = Pages(name, page_id, cover, picture)
    db.session.add(new_page)
    db.session.commit()

    return{"Success": "Page saved"}

def get_page(db, Pages,data):
    add_new_page(db, Pages, data)

    return Pages.query.filter(Pages.page_id == data.get('id')).first()