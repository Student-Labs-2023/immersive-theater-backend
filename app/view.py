from . models import Authors, PerfomanceAuthors, PerfomanceImages, Perfomances, AudioImages, Audio, Places
from app.utils import int_to_str_duration
from flask import Blueprint, request
import json

api = Blueprint('api', __name__)

@api.route('/perfomances', methods=['GET'])
def page_perfomances():
    page_num = request.args.get('page', default = 1, type = int)
    per_page_num = request.args.get('per_page', default = 5, type = int)
    result = dict()
    perf_query = Perfomances.query.filter(Perfomances.id.in_([page_num*per_page_num, page_num*per_page_num+per_page_num])).all()  #TODO: Check first performances from page
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
    result = dict()
    authors = dict()
    images = list()
    audios = list()
    place = dict()
    perf_query = Perfomances.query.filter_by(id=perfomance_id).first()
    if not perf_query:
        return 'Not valid id', 400
    authors_id_query = PerfomanceAuthors.query.filter_by(perfomance_id=perfomance_id).all()
    for author in authors_id_query:
        authors_query = Authors.query.filter_by(id=author.author_id).first()
        authors.update({'id': authors_query.id, 'full_name': authors_query.full_name, 'image_link': authors_query.thumbnail_link, 'role': author.role})
    audios_query = Audio.query.filter_by(perfomance_id=perfomance_id).all()
    for audio in audios_query:
        audio_images_query = AudioImages.query.filter_by(audio_id=audio.id).all()
        audio_images = list()
        for audio_image in audio_images_query:
            audio_images.apiend(str(audio_image.image_link))
        places_query = Places.query.filter_by(id=audio.place_id).first()
        place.update({'name': places_query.name, 'latitude': places_query.latitude, 'longitude': places_query.longitude})
        audios.apiend({'place': place, 'name':audio.name, 'audio_link': audio.audio_link, 'short_audio_link': audio.short_audio_link, images: audio_images})

    images_query = PerfomanceImages.query.filter_by(perfomance_id=perfomance_id).all()
    for image in images_query:
        images.apiend(str(image.image_link))
    result.update({'id': perf_query.id, 'name': perf_query.name, 'image_link': perf_query.thumbnail_link, 'description': perf_query.description, 'duration': int_to_str_duration(perf_query.duration), 'authots': authors, 'images': images, 'audios': audios})
    return json.dumps(result), 200
