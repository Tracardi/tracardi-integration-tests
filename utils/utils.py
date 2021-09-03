import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

x = {
    "access_token": "2e10d261eb29f8dcf1a6fd8dd50c15df04e7d69979f5387704799da8208788cd",
    "token_type": "bearer",
    "roles": [
        "admin"
    ]
}


class Endpoint:

    def __init__(self):
        self.token = self.auth()

    @staticmethod
    def host(path):
        return "{}:{}{}".format(os.environ['HOST'], os.environ['PORT'], path)

    def auth(self):
        response = requests.post(self.host('/token'), {"username": os.environ['LOGIN'], "password": os.environ['PASS']})
        data = response.json()
        return "{} {}".format(data['token_type'], data['access_token'])

    def request(self, endpoint, data=None, params=None, method='POST'):
        return requests.request(method, self.host(endpoint), data=data, params=params, headers={"Authorization": self.token})

    def post(self, endpoint, data=None):
        return self.request(endpoint, json.dumps(data), "post")

    def get(self, endpoint, params=None):
        return self.request(endpoint, params=params, method="get")

    def delete(self, endpoint, data=None, params=None):
        return self.request(endpoint, json.dumps(data), params=params, method="delete")
