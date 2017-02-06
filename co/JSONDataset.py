import json

class JSONDataset:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "JSON dataset " + str(self.data["name"])

    def to_json(self):
        return json.dumps(self.data)

    def getTable(self, sheet_name):
        return self.data["tables"][sheet_name]['rows']