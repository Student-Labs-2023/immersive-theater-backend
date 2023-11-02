from yoomoney import Quickpay, Client
from dotenv import load_dotenv
import os


load_dotenv()

token = os.getenv('YOOMONEY_TOKEN')

def createPayment(label, price, name):
    quickpay = Quickpay(
            receiver="4100117820597048",
            quickpay_form="shop",
            targets=name,
            paymentType="SB",
            sum=price,
            label=label
    )

    return str(quickpay.redirected_url), 200

