from . models import Authors, PerfomanceAuthors, PerfomanceImages, Perfomances, AudioImages, Audio, Places
from app.utils import get_all_info_about_perfomance
from flask import Blueprint, request
import json

api = Blueprint('api', __name__)

@api.route('/perfomances', methods=['GET'])
def page_perfomances():
    page_num = request.args.get('page', default = 1, type = int)
    per_page_num = request.args.get('per_page', default = 5, type = int)
    result = dict()
    perf_query = Perfomances.query.filter(Perfomances.id.in_([page_num*per_page_num, page_num*per_page_num+per_page_num])).all()  #TODO: Check first perfomances from page
    for perfomance in perf_query:
        authors = dict()
        authors_id_query = PerfomanceAuthors.query.filter_by(perfomance_id=perfomance.id).all()
        for author in authors_id_query:
            authors_query = Authors.query.filter_by(id=author.author_id).first()
            authors.update({'id': authors_query.id, 'full_name': authors_query.full_name, 'image_link': authors_query.thumbnail_link, 'role': author.role})
        result.update({'id': perfomance.id, 'name': perfomance.name, 'image_link': perfomance.cover_image_link, 'authors':authors})
    return json.dumps(result), 200


@api.route('/perfomances/<int:perfomance_id>', methods=['GET'])
def perfomance_by_id(perfomance_id):
    result = get_all_info_about_perfomance(perfomance_id)
    if result.__class__ != Exception:
        return json.dumps(result), 200
    else: 
        return '', 400