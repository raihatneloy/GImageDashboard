#!/usr/bin/env python

def badge_model(db):
    class Badge(db.Model):
        __tablename__ = 'badge'
        id = db.Column('id', db.Integer, primary_key=True)
        badge_id =  db.Column('badge_id', db.Integer)
        name = db.Column('name', db.String(1000))
        title = db.Column('title', db.String(1000))
        country = db.Column('country', db.String(1000))
        catagory = db.Column('catagory', db.String(1000))
        month = db.Column('month', db.String(1000))
        year = db.Column('year', db.String(1000))

        def __init__(self, badge_id, name, title, country, catagory, month, year):
            self.badge_id = badge_id
            self.name = name
            self.title = title
            self.country = country
            self.catagory = catagory
            self.month = month
            self.year = year

    return Badge

def add_or_update_badge(db, Badge, data):
    badge_id = data.get('badge_id')
    name = data.get('name')
    title = data.get('title')
    country = data.get('country')
    catagory = data.get('catagory')
    month = data.get('month')
    year = data.get('year')

    check_badge = Badge.query.filter(Badge.badge_id == badge_id).all()

    if len(check_badge) > 0:
        badge_object = check_badge[0]
        badge_object.badge_id = badge_id
        badge_object.name     = name
        badge_object.title    = title
        badge_object.country  = country
        badge_object.catagory = catagory
        badge_object.month    = month
        badge_object.year     = year

    else:
        badge_object = Badge(
                badge_id,
                name,
                title,
                country,
                catagory,
                month,
                year
            )

        db.session.add(badge_object)

    db.session.commit()

    return badge_object

