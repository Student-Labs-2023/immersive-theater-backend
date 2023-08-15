from yoomoney import Quickpay, Client

token = "4100117820597048.8BF22DD0BE2C11882D621EA119A53FEB7D68B89A156BB376DFF8E1AC7F1B2071833FFC242D78CF6FF71AB05A3315E92CFD4A7B3EE126B437D72B327DEE166EAD31E78AB89D3D1AE940F4E9F54F2A5BEFE823B21ED36FFF3B488732F9C408286C440BAEA1CE4EB5A3A8496165AB9E965E75FC6C7EF99247699B4947F0093A6223"

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

def checkPayment(label):
    client = Client(token)
    history = client.operation_history(label=label)
    if len(history.operations) != 0:
        return 'Ticket', 200
    else:
        return 'No payment found', 400

