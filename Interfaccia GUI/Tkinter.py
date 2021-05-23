import numpy as np
import tkinter as tk
from tkinter import filedialog
file=''

def FileImport():
    global file
    file=filedialog.askopenfilename()
    label=tk.Label(root, text="Selected:"+file).pack()

root=tk.Tk()
root.title('Main')
label=tk.Label(root, text="Upload a file:", fg="purple").pack()
button=tk.Button(root, text='Upload',fg="blue", command=FileImport)
button.pack()

root.mainloop()
uploaded_file=np.fromfile(file)
print(uploaded_file)