import sys
import tkinter as tk
from tkinter import filedialog

def pick_files():
    """GUI file picker; returns list of paths."""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    paths = filedialog.askopenfilenames(
        title='Select images',
        filetypes=[('Image files', '*.jpg *.jpeg *.png'), ('All files', '*.*')],
        multiple=True,
    )
    root.destroy()
    if not paths:
        print('No file selected. Exiting.')
        sys.exit(0)
    return list(paths)