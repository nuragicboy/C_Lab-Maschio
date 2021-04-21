import pandas as pd

My_Excel = 'Test_Python.xlsx'

xl = pd.ExcelFile(My_Excel)

print(xl.sheet_names)

df1 = xl.parse('Foglio1')

print(df1)

