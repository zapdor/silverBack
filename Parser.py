import email
import uuid
from bs4 import BeautifulSoup

from Transaction import Transaction


class Parser(Transaction):
    type = ""

    def __init__(self, type, marketplace_id, seller_name, item_name, img_url, price, new_id):
        super().__init__(0, marketplace_id, seller_name, item_name, img_url, price, 0, new_id)
        self.type = type

    def parse(self, msg, transaction):
        body = self.get_text_block(msg)

        seller_ref_begin = body.find(self.seller_name)
        seller_ref_begin += body[seller_ref_begin:len(body)].find(">")
        seller_ref_end = body[seller_ref_begin:len(body)].find("<")
        transaction.seller_name = body[seller_ref_begin+1:seller_ref_begin+seller_ref_end]

        item_ref_begin = body.find(self.item_name)
        item_ref_begin += body[item_ref_begin:len(body)].find(">")
        item_ref_begin += body[item_ref_begin+1:len(body)].find(">")
        item_ref_end = body[item_ref_begin:len(body)].find("<")
        transaction.item_name = body[item_ref_begin+2:item_ref_begin+item_ref_end].replace("\n","").replace("\r","").replace("=","").replace("...", "")

        img_url_ref_end = body.find(self.img_url)
        img_url_ref_begin = body[0:img_url_ref_end].rfind("http")
        img_url_ref_end = body[img_url_ref_begin:img_url_ref_end].find("\"")
        transaction.img_url = body[img_url_ref_begin:img_url_ref_begin+img_url_ref_end]

        price_ref_begin = body.find("$")
        price_ref_end = body[price_ref_begin+1:len(body)].find(" ")+1
        transaction.price = body[price_ref_begin+1:price_ref_begin+price_ref_end]

        return transaction

    # a mail can contain multiple payloads so:
    def get_text_block(self, email_message_instance):
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()


def make_parser(type, marketplace_id, seller_name, item_name, img_url, price):
    parser = Parser(type, marketplace_id, seller_name, item_name, img_url, price, uuid.uuid4())
    return parser
