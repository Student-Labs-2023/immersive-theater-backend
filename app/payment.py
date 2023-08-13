import os
import asyncio
from SberQR import AsyncSberQR

member_id = '00003698'  
tid = '29148600'  # ID  терминала/Точки. Получить в ЛК Сбрербанк бизнес на странице Информация о точке
id_qr = '3001039094'  # Номер наклейки с QR-кодом. Получить в ЛК Сбрербанк бизнес Информация о точке/список оборудования
client_id = '8754fe76-3e87-48c5-8e52-7597414b4b35'  # получить на api.developer.sber.ru
client_secret = '53105a42-b0f1-42e6-9b4d-1961a70d5288'  # получить на api.developer.sber.ru

#
crt_from_pkcs12 = f'{os.getcwd()}/client_cert.crt'  # Для асинхронной версии требуется распаковать сертификат
key_from_pkcs12 = f'{os.getcwd()}/private.key'  # Для асинхронной версии требуется распаковать приватный ключ
pkcs12_password = 'ManjaroUser2204'  # Пароль от файла сертификат. Получается на api.developer.sber.ru
russian_crt = f'{os.getcwd()}/Cert_CA.pem'  # Сертификат мин.цифры для установления SSL соединения

sber_qr = AsyncSberQR(member_id=member_id, id_qr=tid, tid=tid,
                      client_id=client_id, client_secret=client_secret,
                      crt_file_path=crt_from_pkcs12, key_file_path=key_from_pkcs12,
                      pkcs12_password=pkcs12_password,
                      russian_crt=russian_crt)
positions = [{"position_name": 'Товар за 10 рублей',
              "position_count": 1,
              "position_sum": 1,
              "position_description": 'Какой-то товар за 10 рублей'}
             ]

async def main_func(order_sum, order_number, positions):
    data = await sber_qr.creation(
        description=f'Оплата заказа {order_number}',
        order_sum=order_sum,
        order_number=order_number,
        positions=positions)
    logger.info(f'{data}')
    # Сохраним QR в файл qr.png
    qrcode.make(data['order_form_url']).save("qr.png")
    await check_paid(data['order_id'], order_number)


async def check_paid(order_id, order_number):
    data_status = await sber_qr.status(order_id, order_number)
    if data_status['order_state'] != 'PAID':
        print('Заказ не оплачен, отменяем')
        await revoke_payment(order_id)
    else:
        cancel_result = await sber_qr.cancel(order_id,
                                             operation_id=data_status[0]['operation_id'],
                                             cancel_operation_sum=data_status[0]['operation_sum'],
                                             auth_code=data_status[0]['auth_code'],
                                             operation_type=CancelType.REVERSE,
                                             sbp_payer_id=None)  # sbp_payer_id номер телефона клиента в формате +79998887766, если возврат по СБП
        # CancelType.REVERSE - Если прошло менее 24 часов с оплаты
        # CancelType.REFUND - Если прошло более 24 часов с оплаты
        logger.info(f'{cancel_result}')

async def revoke_payment(order_id):
    data_revoke = await sber_qr.revoke(order_id)
    logger.info(f'Revoke result: {data_revoke}')


if __name__ == '__main__':
    positions = [
        {"position_name": "Что-то а 10 рублей",
         "position_count": 1,
         "position_sum": 1000,
         "position_description": "Какой-то товар за 10 рублей"}]
    asyncio.run(main_func(1000, "4", positions))
