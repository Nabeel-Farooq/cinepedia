from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(Media, db.session))
admin.add_view(ModelView(Category, db.session))
