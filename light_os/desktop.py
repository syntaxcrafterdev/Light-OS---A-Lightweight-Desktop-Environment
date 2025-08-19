import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import json
from utils.animations import FadeIn
from widgets.app_launcher import AppLauncher
from widgets.weather import WeatherWidget
from widgets.clock import ClockWidget
from widgets.system_monitor import SystemMonitor

class Desktop:
    def __init__(self, root):
        self.root = root
        self.root.title("Nexus OS")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#000000')
        
        # Initialize desktop components
        self.setup_desktop()
        self.setup_widgets()
        
        # Load user settings
        self.load_settings()
        
        # Apply fade-in animation
        FadeIn(self.root)
    
    def setup_desktop(self):
        # Main desktop canvas
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg='#000000')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Set wallpaper
        self.set_wallpaper("assets/wallpapers/default.jpg")
        
        # Bind right-click for context menu
        self.canvas.bind("<Button-3>", self.show_context_menu)
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-Alt-Delete>", self.show_system_menu)
        
    def setup_widgets(self):
        # Add desktop widgets
        self.clock = ClockWidget(self.canvas)
        self.weather = WeatherWidget(self.canvas)
        self.system_monitor = SystemMonitor(self.canvas)
        
        # App launcher (dock)
        self.app_launcher = AppLauncher(self.root)
        
    def set_wallpaper(self, image_path):
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                # Create a simple gradient if default wallpaper is missing
                self.create_default_wallpaper()
                return
                
            # Load and resize the image to fit the screen
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            self.wallpaper = Image.open(image_path)
            self.wallpaper = self.wallpaper.resize(
                (screen_width, screen_height),
                Image.Resampling.LANCZOS
            )
            self.bg_image = ImageTk.PhotoImage(self.wallpaper)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW)
        except Exception as e:
            print(f"Error setting wallpaper: {e}")
            self.canvas.config(bg='#1a1a1a')
    
    def load_settings(self):
        self.settings_file = "config/settings.json"
        default_settings = {
            "wallpaper": "assets/wallpapers/default.jpg",
            "theme": "dark",
            "widgets": {"clock": True, "weather": True, "system": True}
        }
        
        try:
            os.makedirs("config", exist_ok=True)
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    self.settings = {**default_settings, **json.load(f)}
            else:
                self.settings = default_settings
                self.save_settings()
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.settings = default_settings
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def show_context_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0, bg='#2d2d2d', fg='white',
                      bd=0, font=('Segoe UI', 10))
        
        menu.add_command(label="Change Wallpaper", command=self.change_wallpaper)
        menu.add_separator()
        menu.add_command(label="Create Shortcut")
        menu.add_command(label="Refresh Desktop")
        menu.add_separator()
        menu.add_command(label="Display Settings")
        menu.add_command(label="System Settings")
        menu.add_separator()
        menu.add_command(label="Lock Screen")
        menu.add_command(label="Sign Out", command=self.sign_out)
        menu.add_command(label="Shut Down", command=self.shutdown)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def show_system_menu(self, event=None):
        # Advanced system menu with task manager, etc.
        pass
    
    def change_wallpaper(self):
        # Implement wallpaper changer
        pass
    
    def sign_out(self):
        # Save session and sign out
        self.root.quit()
    
    def shutdown(self):
        # Clean up and exit
        self.root.destroy()
