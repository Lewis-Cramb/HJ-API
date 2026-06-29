from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime as dt
import requests as rqs

def buildCxml(order, invoice_number):
    # <cxml version=1.0 payloadID=x@haywardjardine.co.uk></cxml>
    cxml = Element('cXML')
    cxml.set('version', '1.0')
    cxml.set('payloadID', f'{dt.now().timestamp()}@haywardjardine.co.uk')
    cxml.set('timestamp', dt.now().isoformat())

    # <cxml><header><from_elem><from_cred domain=DUNS><identity>HJ-DUNS</identity></from_cred></from_elem></header></cxml>
    header = SubElement(cxml, 'Header')
    from_elem = SubElement(header, 'From')
    from_cred = SubElement(from_elem, 'Credential')
    from_cred.set('domain', 'DUNS')
    SubElement(from_cred, 'identity').text = '216612308'

    # <header><to_elem><to_cred domain=DUNS><identity>Coupla-DUNS</identity></from_cred></from_elem></header>
    to_elem = SubElement(header, 'To')
    to_cred = SubElement(to_elem, 'Credential')
    to_cred.set('domain', 'DUNS')
    SubElement(to_cred, 'identity').text = '' #HERE - buyerDUNS

    # <header><sender><sender_cred domain=DUNS><identity>Sender</identity><SharedSecret>secret</SharedSecret><UserAgent>Agent</UserAgent> ...
    sender = SubElement(header, 'Sender')
    sender_cred = SubElement(sender, 'Credential')
    sender_cred.set('domain', 'DUNS')
    SubElement(sender_cred, 'identity').text = '216612308'
    SubElement(sender_cred, 'SharedSecret').text = '' #HERE - shared secret
    SubElement(sender, 'UserAgent').text = 'HaywardJardine-Coupa-CXML' 

    # <cxml><request deploymentMode=production><InvoiceDetailRequest></InvoiceDetailRequest></request></cxml>
    request = SubElement(cxml, 'Request')
    request.set('deploymentMode', 'production')
    invoice_detail = SubElement(request, 'InvoiceDetailRequest')

    # <InvoiceDetailRequest><InvoiceDetailRequestHeader invoiceID=x purpose=standard operation=new invoiceDate=y></InvoiceDetailRequestHeader>...
    inv_header = SubElement(invoice_detail, 'InvoiceDetailRequestHeader')
    inv_header.set('invoiceID', f"{invoice_number}")
    inv_header.set('purpose', 'standard')
    inv_header.set('operation', 'new')
    inv_header.set('invoiceDate', f"{dt.now().isoformat()}")

    # <InvoiceDetailRequestHeader...><InvoiceDetailHeaderIndicator></IDHI><InvoiceDetailLineIndicator isAccInLine=yes taxLine=yes> ...
    SubElement(inv_header, 'InvoiceDetailHeaderIndicator')
    inv_line_ind = SubElement(inv_header, 'InvoiceDetailLineIndicator')
    inv_line_ind.set('isAccountingInLine', 'yes')
    inv_line_ind.set('isTaxInLine', 'yes')

    # <InvoiceDetailsRequestHeader><PaymentTerm payInNumberOfDays=30></PaymentTerm></InvoiceDetailsRequestHeader>
    payment_term = SubElement(inv_header, 'PaymentTerm')
    payment_term.set('payInNumberOfDays', '30')

    # <InvoiceDetailRequest><InvoiceDetailOrder><InvoiceDetailOrderInfo><OrderReference><DocumentReference payloadID=x> ...
    inv_order = SubElement(invoice_detail, 'InvoiceDetailOrder')

    order_info = SubElement(inv_order, 'InvoiceDetailOrderInfo')
    order_ref = SubElement(order_info, 'OrderReference')
    doc_ref = SubElement(order_ref, 'DocumentReference')
    doc_ref.set('payloadID', f"{order["order_reference"][:order["order_reference"].index("-")]}" ) #HERE

    # <InvoiceDetailOrder><InvoiceDetailItem><InvoiceLineNumber>x</><Description>y</><Quantity>z</>...
    total = 0
    for product in order['items'].items():
        line_item = SubElement(inv_order, 'InvoiceDetailItem')
        SubElement(line_item, 'InvoiceLineNumber').text = product["line_reference"]
        SubElement(line_item, 'Description').text = product["description"]
        SubElement(line_item, 'Quantity').text = product["quantity"]
        
        # <InvoiceDetailItem><UnitPrice><Money currency=GBP>0.0</Money></UnitPrice></InvoiceDetailItem>
        unit_price = SubElement(line_item, 'UnitPrice')
        money = SubElement(unit_price, 'Money')
        money.set('currency', 'GBP')
        money.text = product["subtotal"]
        total += product["subtotal"]

    # <InvoiceDetailRequest><InvoiceDetailSummary><SubtotalAmount><Money currency=GBP>0.0</Money></SubtotalAmount></InvoiceDetailSummary>...
    summary = SubElement(invoice_detail, 'InvoiceDetailSummary')
    subtotal = SubElement(summary, 'SubtotalAmount')
    subtotal_money = SubElement(subtotal, 'Money')
    subtotal_money.set('currency', 'GBP')
    subtotal_money.text = f"{total}" 


    cxml_payload = tostring(cxml, encoding='unicode')
    print(cxml_payload)
    # # Send to Coupa
    # response = rqs.post(
    #     "https://supplier.coupahost.com/cxml",
    #     headers={"Content-Type": "application/xml"},
    #     data=cxml_payload
    # ) 

    # print(response.status_code)
    # print(response.text)


