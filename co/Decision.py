import json

class Decision:
     def __init__(self, data):
         self.data = data

     def __str__(self):
         return json.dumps(self.data)

     def to_json(self):
         return json.dumps(self.data)

     def getValue(self, property_name):
         return self.data[property_name]
         