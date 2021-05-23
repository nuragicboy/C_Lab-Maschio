import tkinter.filedialog as filedialog  # Python3
import pandas as pd

file = filedialog.askopenfilename(title="Titolo")

df = pd.read_excel(file, sheet_name='Sheet1')

print(df)
