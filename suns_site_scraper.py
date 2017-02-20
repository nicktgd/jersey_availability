#!/usr/bin/env python3

import requests
import bs4
import re
import os
import random
from twitter import *

JERSEY_SITE = 'http://shop.suns.com/Devin_Booker_Jersey'
SITE_FILE = '/opt/jersey/suns_site.txt'
CREDS = '/opt/jersey/t.txt'
PHRASES = '/opt/jersey/phrases.txt'


def send_to_twitter(status):
    with open(CREDS) as f:
        lines = f.readlines()

    token = lines[0].strip()
    token_key = lines[1].strip()
    con_secret = lines[2].strip()
    con_secret_key = lines[3].strip()

    twitter = Twitter(auth=OAuth(token, token_key, con_secret, con_secret_key))
    twitter.statuses.update(status=status)


def get_site_content():
    res = requests.get(JERSEY_SITE)
    try:
        res.raise_for_status()
    except:
        # TODO: Log data instead of sending to stdout
        print('Something went wrong accessing the site')
    else:
        site_file = open(SITE_FILE, 'wb')
        for chunk in res.iter_content(100000):
            site_file.write(chunk)
        site_file.close()


def jersey_search():
    regex = re.compile('(.*)Devin Booker Black(.*)Jersey')
    soup = bs4.BeautifulSoup(open(SITE_FILE), "html.parser")
    elems = soup.select('div a span')
    if re.search(regex, str(elems)):
        send_to_twitter('Black Devin Booker jerseys are available! ' + JERSEY_SITE)
    else:
        with open(PHRASES) as f:
            lines = f.readlines() 
            send_to_twitter(random.choice(lines).strip('\n'))


if __name__ == '__main__':
    get_site_content()
    jersey_search()
