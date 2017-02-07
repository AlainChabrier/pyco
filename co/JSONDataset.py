import json

class JSONDataset:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "JSON dataset " + str(self.data["name"])

    def setName(self, name):
        self.data['name'] = name

    def addTable(self, tableName, rows):
        self.data['tables'][tableName] = {}
        self.data['tables'][tableName]['rows'] = rows

    def to_json(self):
        return json.dumps(self.data)

    def getTable(self, sheet_name):
        return self.data["tables"][sheet_name]['rows']