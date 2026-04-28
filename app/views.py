#-*- coding: utf-8 -*-
from app import app, db
from flask import render_template, request
from flask_paginate import Pagination, get_page_args
from app.models import Category, Media

@app.route('/')
@app.route('/index')
def index():
    categories = Category.query.all()
    categories = sorted(categories, key=lambda x: x.nb_medias(),reverse=True)
    #medias_years = list(set([y.year for y in Media.query.filter(Media.year).all()]))
    last_medias = Media.query.order_by(Media.id.desc()).limit(8)
    return render_template("index.html", categories=categories, last_medias=last_medias)


### CATEGORIES
@app.route('/category/<catname>')
def categories(catname, page=1):
    search = True if request.args.get('q') else False

    page, per_page, offset = get_page_args()
    category = Category.query.filter_by(slug=catname).first()
    pagination = Pagination(bs_version=3,page=page, per_page=per_page, total=category.medias.count(), search=search, record_name=category.name + ' medias')
    return render_template("medias.html", medias=sampling(category.medias.order_by(Media.rate.desc()), offset, per_page), pagination=pagination, title=catname.capitalize())

@app.route('/category/<catname>/<media>')
def artist(catname,media):
    media = Media.query.filter_by(slug=media).first()
    return render_template("media.html", media=media, title=media.name)



def sampling(selection, offset=0, limit=None):
    return selection[offset:(limit + offset if limit is not None else None)]


