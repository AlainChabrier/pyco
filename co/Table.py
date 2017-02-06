import json

import xlrd
from xlrd.sheet import Sheet

class Table:
     def __init__(self, data):
         self.data = data

     def getValues(self, col_name):
         if isinstance(self.data, Sheet):
            num_cols = self.data.ncols   # Number of columns
            num_rows = self.data.nrows # Number of rows
            for col_idx in range(0, num_cols):
                colname = self.data.cell(0, col_idx).value
                if (colname == col_name):
                    values = []
                    for row_idx in range(1, num_rows):
                        values.append(self.data.cell(row_idx, col_idx).value)
                    return values;