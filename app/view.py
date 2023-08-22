from . models import Authors, PerfomanceAuthors, PerfomanceImages, Perfomances, AudioImages, Audio, Places
from app.utils import get_all_info_about_perfomance, generate_ticket
from flask import Blueprint, request
from app.yoomoneyPayment import createPayment, checkPayment
import json
import requests
from . minioWorker import upload_file


api = Blueprint('api', __name__)

@api.route('/perfomances', methods=['GET'])
def page_perfomances():
    page_num = request.args.get('page', default = 1, type = int)
    per_page_num = request.args.get('per_page', default = 5, type = int)
    result = list()
    perf_query = Perfomances.query.filter(Perfomances.id >= (page_num-1)*per_page_num, Perfomances.id <= page_num*per_page_num).all()
    for perfomance in perf_query:
        authors = list()
        place = dict()
        images = list()
        authors_id_query = PerfomanceAuthors.query.filter_by(perfomance_id=perfomance.id).all()
        for author in authors_id_query:
            authors_query = Authors.query.filter_by(id=author.author_id).first()
            authors.append({'id': authors_query.id, 'full_name': authors_query.full_name, 'image_link': authors_query.thumbnail_link, 'role': author.role})
        audio_query = Audio.query.filter_by(perfomance_id=perfomance.id).first()
        place_id = audio_query.place_id
        audio_id = audio_query.id
        audio_images_query = AudioImages.query.filter_by(audio_id=audio_id).all()
        for audio_image in audio_images_query:
            images.append(audio_image.image_link)
        place_query = Places.query.filter_by(id=place_id).first()
        place.update({'name': place_query.name, 'latitude': place_query.latitude, 'longitude': place_query.longitude, 'address': place_query.address})
        result.append({'id': perfomance.id, 'tag':perfomance.tag, 'name': perfomance.name, 'image_link':perfomance.cover_image_link, 'authors':authors, 'duration': perfomance.duration, 'first_place': {'place': place, 'name': audio_query.name,'audio_link': audio_query.audio_link, 'short_audio_link': audio_query.short_audio_link, 'images': images}, 'price': perfomance.price})
    return json.dumps({"data": result}), 200


@api.route('/perfomances/<int:perfomance_id>', methods=['GET'])
def perfomance_by_id(perfomance_id):
    result = get_all_info_about_perfomance(perfomance_id)
    if result.__class__ != Exception:
        return json.dumps(result), 200
    else: 
        return '', 400

@api.route('/payment', methods=['GET'])
def payment():
    user_id_num = request.args.get('user_id', default = None, type = str)
    performance_id_num = request.args.get('performance_id', default = None, type = int)
    label_str = str(user_id_num) + ':' + str(performance_id_num)
    price = Perfomances.query.filter_by(id=performance_id_num).first().price
    performance_name = Perfomances.query.filter_by(id=performance_id_num).first().name
    return createPayment(label_str, price, performance_name)

@api.route('/notification', methods=['POST'])
def notification():
    label_str = request.form.to_dict()['label']
    generate_ticket(label_str)
    return '', 200        
    

