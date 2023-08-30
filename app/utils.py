from . models import Authors, PerfomanceAuthors, PerfomanceImages, Perfomances, AudioImages, Audio, Places, Payments
import string, random
from . import db 
import requests

def check_user_access(user_id, perfomance_id):
    user_payment = Payments.query.filter_by(perfomance_id=perfomance_id, user_id=user_id, perfomance_used=False).first()
    if not user_payment:
        return '' ,400
    return '', 200


def set_perfomance_used(user_id, perfomance_id):
    user_payment = Payments.query.filter_by(perfomance_id=perfomance_id, user_id=user_id, perfomance_used=False).first()
    if not user_payment:
        return 'Bad requests' ,400
    user_payment.perfomance_used = True
    db.session.commit()
    return '', 200

def generate_ticket(label_str, operation_id, sender, amount):
    user_id, perfomance_id = label_str.split(":")
    ticket = str()
    for i in range(1, 17):
        ticket += random.choice(string.ascii_letters)
        if i % 4 == 0 and i !=16:
            ticket += '-'
    payment = Payments(user_id=user_id, perfomance_id=perfomance_id, operation_id=operation_id, sender=sender, amount=amount, perfomance_used=False)
    db.session.add(payment)
    db.session.commit()
    return ticket


def get_all_info_about_perfomance(perfomance_id, user_id):
    result = dict()
    authors = list()
    images = list()
    audios = list()
    place = dict()
    
    perf_query = Perfomances.query.filter_by(id=perfomance_id).first()
    if not perf_query:
        return Exception("Invalid id")
    
    authors_id_query = PerfomanceAuthors.query.filter_by(perfomance_id=perfomance_id).all()
    for author in authors_id_query:
        authors_query = Authors.query.filter_by(id=author.author_id).first()
        authors.append({'id': authors_query.id, 'full_name': authors_query.full_name, 'image_link': authors_query.thumbnail_link, 'role': author.role})
    
    audios_query = Audio.query.filter_by(perfomance_id=perfomance_id).all()
    for audio in audios_query:
        audio_images_query = AudioImages.query.filter_by(audio_id=audio.id).all()
        audio_images = list()
        for audio_image in audio_images_query:
            audio_images.append(str(audio_image.image_link))
        places_query = Places.query.filter_by(id=audio.place_id).first()
        audios.append({'place': {'name': places_query.name, 'latitude': places_query.latitude, 'longitude': places_query.longitude, 'address': places_query.address}, 'name':audio.name, 'audio_link': audio.audio_link, 'short_audio_link': audio.short_audio_link, 'images': audio_images})
    
    images_query = PerfomanceImages.query.filter_by(perfomance_id=perfomance_id).all()
    for image in images_query:
        images.append(str(image.image_link))
    
    payment_query = Payments.query.filter_by(perfomance_id=perfomance_id, user_id=user_id, perfomance_used=False).first()
    if not payment_query:
        access = False
    else:
        access = True

    result.update({'id': perf_query.id, 'tag': perf_query.tag, 'name': perf_query.name, 'image_link': perf_query.thumbnail_link, 'description': perf_query.description, 'duration': perf_query.duration, 'authors': authors, 'images': images, 'audios': audios, 'price': perf_query.price, 'access': access})

    return result
