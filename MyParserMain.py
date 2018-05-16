import email
import imaplib
import sys
from datetime import datetime

from Marketplace import make_marketplace
from Transaction import make_transaction
from User import make_user


def main():
    user = make_user('gmail', 'eratedassignment@gmail.com', 'doingstuff123')
    marketplaces = [make_marketplace('ebay', ['ebay@ebay.com'])
                    ]

    mail_connector = imaplib.IMAP4_SSL(user.url)
    try:
        mail_connector.login(user.email_address, user.password)
    except imaplib.IMAP4.error:
        print('LOGIN FAILED!')
        sys.exit(1)

    mail_connector.select(user.mail_folder)

    searchterm_since = 'SENTSINCE {}'.format(user.lastFetched)
    for marketplace in marketplaces:
        searchterm_body = 'TEXT "{}"'.format(marketplace.body)
        searchterm_domains = ""
        for domain in marketplace.domains:
            if searchterm_domains == "":
                searchterm_domains = 'FROM "{}"'.format(domain)
            else:
                searchterm_domains = 'OR {} FROM "{}"'.format(searchterm_domains, domain)

    searchterm_allterms = '(({}) {} {})'.format(searchterm_domains, searchterm_since, searchterm_body)

    result, data = mail_connector.uid('search', None, searchterm_allterms)
    new_mails_uids = b','.join(data[0].split())
    # (RFC822) is used to fetch the messages bodies
    if len(new_mails_uids) < 1:
        print('OMG, they killed kenny! Also, everything is up to date')
        sys.exit(1)

    result, data = mail_connector.uid('fetch', new_mails_uids, '(RFC822)')

    del data[1::2]  # this removes everything except the messages from data
    new_raw_emails = [msg[1] for msg in data]
    new_email_messages = [email.message_from_bytes(raw_mail) for raw_mail in new_raw_emails]

    all_transactions = list()
    latest_fetch = datetime.min.strftime("%d-%b-%Y")

    for msg in new_email_messages:
        market = find_market_place(marketplaces, msg)
        created_at = email.utils.parsedate_to_datetime(msg['Date']).strftime("%d-%b-%Y")
        transaction = make_transaction(user.id, market.id, "", "", "", 0, created_at)
        parsed_transaction = market.my_parser.parse(msg, transaction)
        all_transactions.append(parsed_transaction)
        if latest_fetch < created_at:
            latest_fetch = created_at
    user.lastFetched = latest_fetch

    for transaction in all_transactions:
        with open('all_transactions.txt', 'a') as the_file:
            the_file.write(str(format_transaction(transaction)))


def format_transaction(transaction):
    formatted = 'id: {}\n' \
                '\tuser id: {}\r\n' \
                '\tmarketplace id: {}\r\n' \
                '\tseller name: {}\r\n' \
                '\titem name: {}\r\n' \
                '\timg url: {}\r\n' \
                '\tprice: {}\r\n' \
                '\tcreated at: {}\r\n' \
                '{}'.format(transaction.id, transaction.user_id, transaction.marketplace_id, transaction.seller_name, transaction.item_name, transaction.img_url, transaction.price, transaction.created_at, '\r\n')
    return formatted


def find_market_place(marketplaces, msg):
    for marketplace in marketplaces:
        if email.utils.parseaddr(msg['From'])[1] in marketplace.domains:
            return marketplace
    return None


if __name__ == "__main__":
    main()
