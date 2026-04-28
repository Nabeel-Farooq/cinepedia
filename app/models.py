#-*- coding: utf-8 -*-
from app import db
from sqlalchemy import event
from slugify import slugify


class Media(db.Model):
    __tablename__ =  'Media'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150), index=True, unique=True)
    name = db.Column(db.String(150), index=True, unique=True)
    year = db.Column(db.Integer, index=True)
    description = db.Column(db.Text)
    rate = db.Column(db.Float, index=True)
    img_url = db.Column(db.String(150))
    url = db.Column(db.String(150))
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'))

    def __repr__(self):
        return '<Media %r>' % self.name

    def get_larger_img(self):
        if self.img_url is not None:
            return self.img_url.replace('64s','128s')

class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), index=True)
    slug = db.Column(db.String(150), index=True, unique=True)
    medias = db.relationship('Media', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category %r>' % self.name

    def nb_medias(self):
        return self.medias.count()


def media_before_insert_listener(mapper, connection, target):
    target.slug = slugify(target.name)

def category_before_insert_listener(mapper, connection, target):
    target.slug = slugify(target.name)

event.listen(Media, 'before_insert', media_before_insert_listener)
event.listen(Category, 'before_insert', category_before_insert_listener)
