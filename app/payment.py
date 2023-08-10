import os
import asyncio
from SberQR import AsyncSberQR

member_id = '00003698'  
tid = ''  # ID  терминала/Точки. Получить в ЛК Сбрербанк бизнес на странице Информация о точке
id_qr = ''  # Номер наклейки с QR-кодом. Получить в ЛК Сбрербанк бизнес Информация о точке/список оборудования
client_id = ''  # получить на api.developer.sber.ru
client_secret = ''  # получить на api.developer.sber.ru

#
crt_from_pkcs12 = f'{os.getcwd()}/cert.crt'  # Для асинхронной версии требуется распаковать сертификат
key_from_pkcs12 = f'{os.getcwd()}/private.key'  # Для асинхронной версии требуется распаковать приватный ключ
pkcs12_password = 'SomeSecret'  # Пароль от файла сертификат. Получается на api.developer.sber.ru
russian_crt = f'{os.getcwd()}/Cert_CA.pem'  # Сертификат мин.цифры для установления SSL соединения

sber_qr = AsyncSberQR(member_id=member_id, id_qr=tid, tid=tid,
                      client_id=client_id, client_secret=client_secret,
                      crt_file_path=crt_from_pkcs12, key_file_path=key_from_pkcs12,
                      pkcs12_password=pkcs12_password,
                      russian_crt=russian_crt)
positions = [{"position_name": 'Товар за 10 рублей',
              "position_count": 1,
              "position_sum": 1000,
              "position_description": 'Какой-то товар за 10 рублей'}
             ]
async def creation_qr():
    data = await sber_qr.creation(description=f'Оплата заказа 3', order_sum=1000, order_number="3", positions=positions)
    print(data)
    
asyncio.run(creation_qr())
