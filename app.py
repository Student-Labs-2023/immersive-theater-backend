import os
from app import create_app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import Authors, PerfomanceAuthors, PerfomanceImages, Perfomances, AudioImages, Audio, Places
from app import db
from adminDashboard.admin import create_admin_dashboard

if __name__ == "__main__":
    app = create_app()
    
    create_admin_dashboard(app, db)
    
    app.run(host='0.0.0.0', port=5000)

