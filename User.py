import re
import uuid
import datetime
import time


class User(object):
    id = 0
    email_type = ""
    email_address = ""
    password = ""
    url = ""
    mail_folder = ""
    last_fetched = datetime.date.min
    last_fetch_file = "my_last_fetch.txt"

    def __init__(self, email_type, email_address, password, new_id):
        self.email_type = email_type
        self.email_address = email_address
        self.password = password
        self.id = new_id
        self.fill_url_and_main_folder()
        try:
            self.last_fetched = self.read_date_from_file(self.last_fetch_file)
        except (FileExistsError, IOError):
            self.update_date_to_file(self.last_fetch_file, self.last_fetched)

    def fill_url_and_main_folder(self):
        self.url = {
            'gmail': 'imap.gmail.com',
            'yahoo': 'imap.mail.yahoo.com'
        }.get(self.email_type, 'imap.gmail.com')
        self.mail_folder = {
            'gmail': 'inbox',
            'yahoo': 'inbox'
        }.get(self.email_type, 'inbox')

    def read_date_from_file(self, filepath):
        with open(filepath, 'r') as f:
            content = [line.strip() for line in f.readlines()]
        try:
            datepattern = '%d-%b-%Y'
            raw_date = content[0]
            date = datetime.datetime.strptime(raw_date, datepattern)
            return date
        except IndexError:
            print('Error! expected file to contain date!')

    def update_date_to_file(self, filepath, date):
        self.last_fetched = date
        with open(filepath, 'w+') as file:
            file.write(self.last_fetched.strftime('%d-%b-%Y'))


def make_user(email_type, email_address, password):
    user = User(email_type, email_address, password, uuid.uuid4())
    return user
