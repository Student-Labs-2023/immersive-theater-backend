import sys
sys.path.append("..")

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import Authors, PerfomanceAuthors, PerfomanceImages, Perfomances, AudioImages, Audio, Places 

def create_admin_dashboard(app, db):

    admin = Admin(app, name='Admin page', template_mode='bootstrap3')
    admin.add_view(ModelView(Authors, db.session, name='Авторы'))
    admin.add_view(ModelView(PerfomanceAuthors, db.session, name='Авторы спектакля'))
    admin.add_view(ModelView(PerfomanceImages, db.session, name='Фото спектакля'))
    admin.add_view(ModelView(Perfomances, db.session, name='Спектакли'))
    admin.add_view(ModelView(AudioImages, db.session, name='Фото аудио'))
    admin.add_view(ModelView(Audio, db.session, name='Аудио'))
    admin.add_view(ModelView(Places, db.session, name='Места'))
