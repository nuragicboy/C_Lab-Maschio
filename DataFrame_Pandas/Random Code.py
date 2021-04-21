import pandas as pd
import numpy as np

# Creating a DataFrame by passing a NumPy array, with a datetime index and labeled column
dates = pd.date_range("20130101", periods=6)
df = pd.DataFrame(np.random.randn(6, 5), index=dates, columns=list("ABCDE"))
#print(df)

# view the top (primi 5) and bottom (ultimi 5) rows of the frame
print(df.head())
print(df.tail())

# Veloci analisi statistiche
D = df.describe()

print(D)