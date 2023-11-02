from . models import Authors, PerformanceAuthors, PerformanceImages, Performances, AudioImages, Audios, Places, Payments, Base
from app.utils import get_all_info_about_performance, get_short_info_about_performance, generate_ticket, set_performance_used, check_user_access
from flask import Blueprint, request
from app.yoomoneyPayment import createPayment
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import requests
from dotenv import load_dotenv
import os


load_dotenv()

api = Blueprint('api', __name__)

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
session = sessionmaker(bind=engine)
s = session()

@api.route('/performances', methods=['GET'])
def page_performances():
    page_num = request.args.get('page', default = 1, type = int)
    per_page_num = request.args.get('per_page', default = 5, type = int)
    user_id = request.args.get('user_id', type=str)
    user_performances = request.args.get('user_performances', default = 0, type = int)

    result = list()
    
    for i in range((page_num - 1)*(per_page_num), page_num*per_page_num):
        performance = get_short_info_about_performance(i, user_id)
        if performance:
            result.append(performance)     
    return json.dumps({"data": result}), 200


@api.route('/performances/<int:performance_id>', methods=['GET'])
def performance_by_id(performance_id):
    user_id = request.args.get('user_id', type=str)
    result = get_all_info_about_performance(performance_id, user_id)
    if result.__class__ != Exception:
        return json.dumps(result), 200
    else: 
        return 'Invalid args', 400

@api.route('/payment', methods=['GET'])
def payment():
    user_id_num = request.args.get('user_id', default = None, type = str)
    performance_id_num = request.args.get('performance_id', default = None, type = int)
    label_str = str(user_id_num) + ':' + str(performance_id_num)
    for row in s.query(Performances).filter(Performances.id == performance_id_num):
        price = row.price
        performance_name = row.name
    return createPayment(label_str, price, performance_name)

@api.route('/notification', methods=['POST'])
def notification():
    label_str = request.form.to_dict()['label']
    operation_id = request.form.to_dict()['operation_id']
    sender = request.form.to_dict()['sender']
    amount = request.form.to_dict()['amount']
    generate_ticket(label_str, operation_id, sender, amount)
    return '', 200        
    
@api.route('/performance_used', methods=['POST'])
def performance_used():
    user_id = request.args.get('user_id', type=str)
    performance_id = request.args.get('performance_id', type=int)
    return set_performance_used(user_id, performance_id)

@api.route('/performance_access', methods=['POST'])
def performance_access():
    user_id = request.form.to_dict()['user_id']
    performance_id = request.form.to_dict()['performance_id']
    return check_user_access(user_id, performance_id)

