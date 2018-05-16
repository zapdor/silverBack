import uuid
import datetime


class User(object):
    id = 0
    email_type = ""
    email_address = ""
    password = ""
    url = ""
    mail_folder = ""
    lastFetched = datetime.date.min

    def __init__(self, email_type, email_address, password, new_id):
        self.email_type = email_type
        self.email_address = email_address
        self.password = password
        self.id = new_id
        self.lastFetched = datetime.date.min.strftime("%d-%b-%Y")
        self.fill_url_and_main_folder()

    def fill_url_and_main_folder(self):
        self.url = {
            'gmail': 'imap.gmail.com',
            'yahoo': 'imap.mail.yahoo.com'
        }.get(self.email_type, 'imap.gmail.com')
        self.mail_folder = {
            'gmail': 'inbox',
            'yahoo': 'inbox'
        }.get(self.email_type, '[Gmail]/All Mail')


def make_user(email_type, email_address, password):
    user = User(email_type, email_address, password, uuid.uuid4())
    return user

