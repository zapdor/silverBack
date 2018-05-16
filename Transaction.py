import uuid
import datetime


class Transaction(object):
    id = 0
    user_id = ""
    marketplace_id = ""
    seller_name = ""
    item_name = ""
    img_url = ""
    price = 0
    created_at = datetime.date.min

    def __init__(self, user_id, marketplace_id, seller_name, item_name, img_url, price, created_at, new_id):
        self.user_id = user_id
        self.marketplace_id = marketplace_id
        self.seller_name = seller_name
        self.item_name = item_name
        self.img_url = img_url
        self.price = price
        self.created_at = created_at
        self.id = new_id


def make_transaction(user_id, marketplace_id, seller_name, item_name, img_url, price, created_at):
    transaction = Transaction(user_id, marketplace_id, seller_name, item_name, img_url, price, created_at, uuid.uuid4())
    return transaction
