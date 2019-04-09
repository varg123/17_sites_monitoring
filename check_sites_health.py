import urllib.request
import whois
from datetime import datetime, timedelta
from urllib.parse import urlparse
import argparse

DAYS_MIN_PAID_COUNT = 31


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Путь к файлу с url')
    return parser.parse_args()


def load_urls4check(path):
    with open(path, 'rt', encoding='utf8') as file_with_url:
        return file_with_url.read().split('\n')


def is_server_respond_with_200(url):
    try:
        return urllib.request.urlopen(url).status == 200
    except urllib.error.URLError:
        return False


def get_domain_expiration_date(domain_name):
    whois_data = whois.whois(domain_name)
    expiration_date = whois_data['expiration_date']
    if isinstance(expiration_date, list):
        return expiration_date[0]
    return expiration_date


def get_valid_url(url):
    url_parse = urlparse(url)
    return '{}://{}'.format(url_parse.scheme, url_parse.netloc)


def is_domain_paid_for(expiration_date):
    if expiration_date is None:
        return False
    return (expiration_date-datetime.now()).days > DAYS_MIN_PAID_COUNT


def main():
    file_path = parse_args().file
    tmpl_domain_info = '''
    Домен: {}
    Ответ статусом HTTP 200: {}
    Проплачен более чем на {} дней: {}
    '''
    for url in load_urls4check(file_path):
        url_valid = get_valid_url(url)
        expiration_date = get_domain_expiration_date(url_valid)
        domain_info = tmpl_domain_info.format(
            url_valid,
            is_server_respond_with_200(url_valid),
            DAYS_MIN_PAID_COUNT,
            is_domain_paid_for(expiration_date)
        )
        print(domain_info)

if __name__ == '__main__':
    main()
