import json

class Goal:
    def __init__(self, data):
         self.data = data

    def __str__(self):
        return self.data["verbalization"]

    def to_json(self):
        print json.dumps(self.data)
        return json.dumps(self.data)