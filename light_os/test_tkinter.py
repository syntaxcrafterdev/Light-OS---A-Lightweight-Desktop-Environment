import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Tkinter Test")
    
    label = tk.Label(root, text="Tkinter is working!")
    label.pack(padx=20, pady=20)
    
    button = tk.Button(root, text="Close", command=root.quit)
    button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
