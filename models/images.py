#!/usr/bin/env python

def images_model(db):
    class Images(db.Model):
        __tablename__ = 'images'
        id = db.Column('id', db.Integer, primary_key=True)
        image_link = db.Column('link', db.String(100))
        thumbnail_link = db.Column('thumbnail', db.String(100))

        def __init__(self, image_link, thumbnail_link):
            self.image_link = image_link
            self.thumbnail_link = thumbnail_link

    return Images


def add_new_image(db, Images, data):
    image_link = data.get('link')
    thumbnail_link = data.get('thumbnail')

    check_image = Images.query.filter(Images.image_link == image_link).all()

    if len(check_image) > 0:
        return {"Error": "Image already in database"}

    new_image = Images(image_link, thumbnail_link)
    db.session.add(new_image)
    db.session.commit()

    return {"Success": "Image saved"}

def get_image(db, Images, data):
    add_new_image(db, Images, data)

    return Images.query.filter(Images.image_link == data.get('link')).first()