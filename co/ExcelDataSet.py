

import xlrd
from xlrd.sheet import Sheet

import json

class ExcelDataSet:
    def __init__(self, location):
        self.location = location
        self.book = xlrd.open_workbook(location)

    def display(self):
        print "Sheets ", self.book._sheet_names

    def to_json(self):
        self.data = {'name':self.location, 'tables':{}}
        for sheet_name in self.book.sheet_names():
            table = {'name':sheet_name, 'columns':[]}
            sheet = self.book.sheet_by_name(sheet_name)
            num_cols = sheet.ncols   # Number of columns
            num_rows = sheet.nrows # Number of rows
            for col_idx in range(0, num_cols):
                column = {'name':sheet.cell(0, col_idx).value}
                table['columns'].append(column)
                values = []
                for row_idx in range(1, num_rows):
                    values.append(sheet.cell(row_idx, col_idx).value)
                column["values"] = values
            #setattr(self.data['tables'], sheet_name, table)
            self.data['tables'][sheet_name] = table
        return json.dumps(self.data)

    def getTable(self, sheet_name):
        return Table(self.book.sheet_by_name(sheet_name))
