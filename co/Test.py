import json
import requests

class Test:
    def __init__(self):
        self.url = "http://www.google.com"

    def do(self, what):
        return requests.get(self.url)
