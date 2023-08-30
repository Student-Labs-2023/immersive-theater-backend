from yoomoney import Quickpay, Client

token = "4100117820597048.953F382082D51C99E16601CB769CDB721757656D1AA5F172735FB35E2A0DE20160E9F3F13B7E43F16FDCFA079F593BBE559B097F229A08D2E6F41A59FC97BC32673FC812913FEA884E72E46D6F03C9B972685DE2E5BC8C20BD7B6B0BA58719644B7AB00F30B7353FB34A1813E7D816C0E694799EB85707DEB21B357FACBB22CB"

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

