from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
admin = Admin(app, name='cinepedia', template_mode='bootstrap3')

from app import views, models, ajax
from models import Category, Media

class MediaView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False

admin.add_view(MediaView(Media, db.session))
admin.add_view(ModelView(Category, db.session))

@app.template_filter('pluralize')
def pluralize(number, singular = '', plural = 's'):
    if number == 1:
        return singular
    else:
        return plural


