from flask import Flask, request, Response
from lxml import etree
from database import get_db
from service import create_invoice

app = Flask(__name__)

WSDL = """<?xml version="1.0" encoding="UTF-8"?>
<definitions name="InvoiceService"
             targetNamespace="http://invoice.service/"
             xmlns="http://schemas.xmlsoap.org/wsdl/"
             xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
             xmlns:tns="http://invoice.service/"
             xmlns:xsd="http://www.w3.org/2001/XMLSchema">

  <message name="createInvoiceRequest">
    <part name="alici_isim" type="xsd:string"/>
    <part name="satici_firma" type="xsd:string"/>
    <part name="urun_adi" type="xsd:string"/>
    <part name="miktar" type="xsd:int"/>
    <part name="fiyat" type="xsd:float"/>
    <part name="kdv_orani" type="xsd:float"/>
  </message>

  <message name="createInvoiceResponse">
    <part name="fatura_no" type="xsd:string"/>
  </message>

  <portType name="InvoicePortType">
    <operation name="createInvoice">
      <input message="tns:createInvoiceRequest"/>
      <output message="tns:createInvoiceResponse"/>
    </operation>
  </portType>

  <binding name="InvoiceBinding" type="tns:InvoicePortType">
    <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="createInvoice">
      <soap:operation soapAction="createInvoice"/>
      <input><soap:body use="encoded" namespace="http://invoice.service/" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/></input>
      <output><soap:body use="encoded" namespace="http://invoice.service/" encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"/></output>
    </operation>
  </binding>

  <service name="InvoiceService">
    <port name="InvoicePort" binding="tns:InvoiceBinding">
      <soap:address location="http://localhost:8000/soap"/>
    </port>
  </service>
</definitions>"""


@app.route("/soap", methods=["GET"])
def wsdl():
    return Response(WSDL, mimetype="text/xml")


@app.route("/soap", methods=["POST"])
def soap_endpoint():
    try:
        tree = etree.fromstring(request.data)
        ns = {
            "soap": "http://schemas.xmlsoap.org/soap/envelope/",
            "inv": "http://invoice.service/"
        }

        body = tree.find(".//inv:createInvoice", ns)
        if body is None:
            body = tree.find(".//{http://invoice.service/}createInvoice")

        alici_isim = body.find("alici_isim").text
        satici_firma = body.find("satici_firma").text
        urun_adi = body.find("urun_adi").text
        miktar = int(body.find("miktar").text)
        fiyat = float(body.find("fiyat").text)
        kdv_orani = float(body.find("kdv_orani").text)

        db = next(get_db())
        invoice = create_invoice(alici_isim, satici_firma, urun_adi, miktar, fiyat, kdv_orani, db)

        response_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <createInvoiceResponse xmlns="http://invoice.service/">
      <fatura_no>{invoice.fatura_no}</fatura_no>
    </createInvoiceResponse>
  </soap:Body>
</soap:Envelope>"""

        return Response(response_xml, mimetype="text/xml")

    except Exception as e:
        error_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <soap:Fault>
      <faultcode>Server</faultcode>
      <faultstring>{str(e)}</faultstring>
    </soap:Fault>
  </soap:Body>
</soap:Envelope>"""
        return Response(error_xml, mimetype="text/xml", status=500)


if __name__ == "__main__":
    print("SOAP server çalışıyor: http://localhost:8000/soap")
    app.run(host="0.0.0.0", port=8000)