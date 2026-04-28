#-*- coding: utf-8 -*-
from app import app, db
from flask import render_template, request, jsonify
from app.models import Media, Category
import json

@app.route('/_rate')
def rate():
    model = request.args.get('type', '', type=str)
    obj_id = request.args.get('id', 0, type=int)
    note = request.args.get('note', 0, type=float)

    if model == "album":
        album = Album.query.get(obj_id)
        album.rate = note
        db.session.add(album)

    db.session.commit()
    return jsonify("ok")


@app.route('/_all.json')
def all():
    film_id = Category.query.filter_by(slug="film")[0].id
    serie_id = Category.query.filter_by(slug="serie")[0].id
    anime_id = Category.query.filter_by(slug="anime")[0].id
    jeu_id = Category.query.filter_by(slug="jeu")[0].id
    films = Media.query.filter_by(category_id=film_id).all()
    series = Media.query.filter_by(category_id=serie_id).all()
    animes = Media.query.filter_by(category_id=anime_id).all()
    jeux = Media.query.filter_by(category_id=jeu_id).all()

    return json.dumps({'status':True,'error':None,'data':
                {
                    'films': [{"img":a.img_url, "slug":a.slug, "display":a.name+" - "+str(a.year)} for a in films],
                    'series': [{"img":a.img_url, "slug":a.slug, "display":a.name+" - "+str(a.year)} for a in series],
                    'animes': [{"img":a.img_url, "slug":a.slug, "display":a.name+" - "+str(a.year)} for a in animes],
                    'jeux': [{"img":a.img_url, "slug":a.slug, "display":a.name+" - "+str(a.year)} for a in jeux],
                }
               })

