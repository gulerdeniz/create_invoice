# → test amaçlı istek atar
from zeep import Client

client = Client("http://localhost:8000/soap?wsdl")

result = client.service.createInvoice(
    alici_isim="Deniz",
    satici_firma="İncehesap",
    urun_adi="KLEVV Cras V RGB 7200Mhz cl34 bellek",
    miktar=1,
    fiyat=27000.0,
    kdv_orani=0.20
)
print("Fatura No:", result)