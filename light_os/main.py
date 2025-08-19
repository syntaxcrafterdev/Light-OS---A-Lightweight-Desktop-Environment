import tkinter as tk
from desktop import Desktop
from utils.theme import set_theme
import ctypes

def main():
    # Set DPI awareness for better scaling on high-DPI displays
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    root = tk.Tk()
    set_theme()
    app = Desktop(root)
    root.mainloop()

if __name__ == "__main__":
    main()
