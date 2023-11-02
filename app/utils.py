from . models import Authors, PerformanceAuthors, PerformanceImages, Performances, AudioImages, Audios, Places, Payments
import string, random
from . import db 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import requests
from dotenv import load_dotenv
import os


load_dotenv()

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
session = sessionmaker(bind=engine)
s = session()

def check_user_access(user_id, performance_id):
    user_payment = s.query(Payments).filter(Payments.performance_id == performance_id).filter(
                   Payments.user_id == user_id).filter(Payments.performance_used == False).first()
    if not user_payment:
        return '' ,400
    return '', 200

def set_performance_used(user_id, performance_id):
    user_payment = s.query(Payments).filter(Payments.performance_id == performance_id).filter(
            Payments.user_id == user_id).filter(Payments.performance_used == False).first()
    if not user_payment:
        return 'Bad requests' ,400
    user_payment.performance_used = True
    db.session.commit()
    return '', 200

def generate_ticket(label_str, operation_id, sender, amount):
    user_id, performance_id = label_str.split(":")
    ticket = str()
    for i in range(1, 17):
        ticket += random.choice(string.ascii_letters)
        if i % 4 == 0 and i !=16:
            ticket += '-'
    payment = Payments(user_id=user_id, performance_id=performance_id, operation_id=operation_id, sender=sender, amount=amount, performance_used=False)
    db.session.add(payment)
    db.session.commit()
    return ticket

def get_short_info_about_performance(performance_id, user_id):
    result = dict()
    authors = list()
    images = list()
    first_place = list()
    

    for row in s.query(Performances).filter(Performances.id == performance_id):
        result.update({'id': row.id, 'tag': row.tag, 'name': row.name, 'image_link': row.thumbnail_link, 'duration': row.duration, 'price': row.price})

    for row in s.query(PerformanceAuthors, Authors).filter(
            PerformanceAuthors.author_id == Authors.id).filter(
            PerformanceAuthors.performance_id == performance_id).all():
                authors.append({'id': row.Authors.id, 'full_name': row.Authors.full_name,
                'image_link': row.Authors.thumbnail_link, 'role': row.PerformanceAuthors.role})
   
    if authors:
        result.update({'authors': authors})

    for row in s.query(Audios, AudioImages).filter(
            Audios.performance_id == performance_id).filter(
                    Audios.id == AudioImages.audio_id).all():
                if row.AudioImages.image_link:
                    images.append(row.AudioImages.image_link)

    for row in s.query(Audios, Places).filter(
            Audios.performance_id == performance_id).filter(
            Audios.place_id == Places.id):
                first_place.append({'place': {'name': row.Places.name, 'longitude': row.Places.longitude,
                                    'latitude': row.Places.latitude, 'address': row.Places.address},
                                    'name': row.Audios.name, 'audio_link': row.Audios.audio_link, 
                                    'short_audio_link': row.Audios.short_audio_link, 'images' : images})
    if first_place:
        result.update({'first_place': first_place})

    for row in s.query(Payments).filter(
            Payments.performance_id==performance_id).filter(
            Payments.user_id==user_id).filter(
            Payments.performance_used==False):
                result.update({'access': row.performance_used})
    
    
    return result
    

def get_all_info_about_performance(performance_id, user_id):
    result = dict()
    authors = list()
    images = list()
    audios = list()
    places = list()
    
    perf_query = s.query(Performances).filter(Performances.id == performance_id).first()
    if perf_query == None:
        return Exception("Invalid id")
    
    for row in s.query(PerformanceAuthors, Authors).filter(
            PerformanceAuthors.author_id == Authors.id).filter(
            PerformanceAuthors.performance_id == performance_id).all():
                authors.append({'id': row.Authors.id, 'full_name': row.Authors.full_name,
                'image_link': row.Authors.thumbnail_link, 'role': row.PerformanceAuthors.role})
    
    for row in s.query(Audios, AudioImages).filter(
            Audios.performance_id == performance_id).filter(
                    Audios.id == AudioImages.audio_id).all():
                if row.AudioImages.image_link:
                    images.append(row.AudioImages.image_link)

    for row in s.query(Audios, Places).filter(
            Audios.performance_id == performance_id).filter(
            Audios.place_id == Places.id).all():
                places.append({'place': {'name': row.Places.name, 'longitude': row.Places.longitude,
                                    'latitude': row.Places.latitude, 'address': row.Places.address},
                                    'name': row.Audios.name, 'audio_link': row.Audios.audio_link, 
                                    'short_audio_link': row.Audios.short_audio_link, 'images' : images})
    
    for row in s.query(Payments).filter(
            Payments.performance_id==performance_id).filter(
            Payments.user_id==user_id).filter(
            Payments.performance_used==False):
                result.update({'access': not row.performance_used})

    result.update({'id': perf_query.id, 'tag': perf_query.tag, 'name': perf_query.name, 'image_link': perf_query.thumbnail_link, 'description': perf_query.description, 'duration': perf_query.duration, 'authors': authors, 'images': images, 'audios': places, 'price': perf_query.price})

    return result
