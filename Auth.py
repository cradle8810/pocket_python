import json
import os
import re
import requests
import sys


class get_code_param:
    consumer_key: str
    redirect_uri: str
    code: str
    access_token: str

    url = 'https://getpocket.com/v3/oauth/request'

    def __init__(self, consumer_key: str, redirect_uri: str):
        self.consumer_key = consumer_key
        self.redirect_uri = redirect_uri

    def get_code(self):
        payload = {
            "consumer_key": self.consumer_key,
            "redirect_uri": self.redirect_uri
        }
        res = requests.post(self.url, payload)
        self.code = res.content[5:].decode('utf-8')

    def print_auth_url(self):
        print(
            'https://getpocket.com/auth/authorize?request_token=' +
            str(self.code) + '&redirect_uri=' + self.redirect_uri
            )
        
    def get_authorization_key(self):
        url = 'https://getpocket.com/v3/oauth/authorize'

        payload = {
            "consumer_key": self.consumer_key,
            "code": self.code
        }
        res = requests.post(url, data=payload)
        
        # access_token=<token>&username=<mail>
        # access_token=rrrr-rrrrr-rrrrr-rrrr&username=example%40example.com
        self.access_token = re.split('[=\&]',res.content.decode('utf-8'))[1]


def main():

    try:
        os.environ['CONSUMER_KEY'] == None
    except KeyError:
        sys.stderr.write('Set your consumer_key to CONSUMER_KEY')
        os._exit(2)

    r = get_code_param(
        os.environ['CONSUMER_KEY'],
        "https://www.google.co.jp"
        )
    r.get_code()
    r.print_auth_url()

    input("Press Enter to continue...")
    r.get_authorization_key()

    print(r.access_token)


if __name__ == '__main__':
    main()
