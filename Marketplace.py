import uuid

from Parser import make_parser


class Marketplace(object):
    id = 0
    name = ""
    domains = list()
    subject = ""
    body = ""
    my_parser = object()
    parser = ""

    def __init__(self, name, domains, new_id):
        self.id = new_id
        self.name = name
        self.domains = domains
        self.fill_subject_and_body()
        self.fill_parser()

    def fill_subject_and_body(self):
        self.subject = {
            'ebay': 'order shipped',
            'amazon': 'order confirmation'
        }.get(self.name, 'order shipped')
        self.body = {
            'ebay': 'order shipped',
            'amazon': 'you ordered'
        }.get(self.name, 'order shipped')

    def fill_parser(self):
        self.my_parser = {
            'ebay': make_parser(self.name, self.id, 'Seller:', 'product-name', 'image for your order', 'product-price'),
            'amazon': make_parser(self.name, self.id, 'Seller:', 'product-name', 'image for your order', 'product-price')  #Note: this is the same as ebay's - I did not want to spend time on this line atm
        }.get(self.name, make_parser(self.name, self.id, 'Seller:', 'product-name', 'image for your order', 'product-price'))


def make_marketplace(name, domains):
    marketplace = Marketplace(name, domains, uuid.uuid4())
    return marketplace
