import sys
sys.path.append("..")

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import Authors, PerformanceAuthors, PerformanceImages, Performances, AudioImages, Audios, Places, Payments

class AdminView(ModelView):
    def __init__(self, model, *args, **kwargs):
        self.column_list = [c.key for c in model.__table__.columns]
        self.form_columns = self.column_list
        super(AdminView, self).__init__(model, *args, **kwargs)

def create_admin_dashboard(app, db):

    admin = Admin(app, name='Admin page', template_mode='bootstrap3')
    admin.add_view(AdminView(Authors, db.session, name='Авторы'))
    admin.add_view(AdminView(PerformanceAuthors, db.session, name='Авторы спектакля'))
    admin.add_view(AdminView(PerformanceImages, db.session, name='Фото спектакля'))
    admin.add_view(AdminView(Performances, db.session, name='Спектакли'))
    admin.add_view(AdminView(AudioImages, db.session, name='Фото аудио'))
    admin.add_view(AdminView(Audios, db.session, name='Аудио'))
    admin.add_view(AdminView(Places, db.session, name='Места'))
    admin.add_view(AdminView(Payments, db.session, name='Оплата'))

