import os
import sys
import traceback

def main():
    print("Starting Nexus OS...")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    
    # Add the current directory to the path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {script_dir}")
    sys.path.insert(0, script_dir)
    
    try:
        print("Importing tkinter...")
        import tkinter as tk
        print("Tkinter imported successfully")
        
        print("Creating root window...")
        root = tk.Tk()
        root.title("Test Window")
        
        # Test label
        label = tk.Label(root, text="If you can see this, Tkinter is working!")
        label.pack(padx=20, pady=20)
        
        try:
            import ctypes
            print("Setting DPI awareness...")
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            print(f"Warning: Could not set DPI awareness: {e}")
        
        # Try to import and initialize the desktop
        try:
            print("Importing desktop module...")
            from desktop import Desktop
            from utils.theme import set_theme
            
            print("Setting theme...")
            set_theme()
            
            print("Creating Desktop instance...")
            app = Desktop(root)
        except Exception as e:
            print(f"Error in desktop initialization: {e}")
            print("Traceback:")
            traceback.print_exc()
            
            # Show error in the window
            error_label = tk.Label(root, text=f"Error: {str(e)}", fg="red")
            error_label.pack(pady=10)
            
            trace_text = tk.Text(root, height=10, width=50)
            trace_text.insert(tk.END, traceback.format_exc())
            trace_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        print("Starting mainloop...")
        root.mainloop()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        print("Traceback:")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
