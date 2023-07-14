from app import app
from app import db
from models import Perfomances

#TODO: Get access to the database to get performances
#      Database have id:string, name:string, image_link:string, authors:array.
@app.route('/perfomances', methods=['GET'])
def page_perfomances():
    page_num = request.args.get('page', default = 1, type = int)
    per_page_num = request.args.get('per_page', default = 5, type = int)
    engine = create_engine('sqlite:///')
    metadata.create_all(engine)
    tmp = Perfomances()
    db.session.add(tmp)
    result = db.session.query(Perfomances).filter(Perfomances.id < per_page_num)
    return engine.connect().execute(text(str(result))), 200


@app.route('/perfomances/<int:perfomance_id>', methods=['GET'])
def perfomance_by_id(perfomance_id):
    Perfomances(id=perfomance_id)
    return Perfomances.query.filter_by(id=perfomance_id).all(), 200
