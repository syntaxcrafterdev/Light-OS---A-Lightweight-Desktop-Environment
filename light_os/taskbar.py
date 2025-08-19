import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import time
from utils.animations import SlideIn

class Taskbar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#1a1a1a', height=40)
        self.parent = parent
        self.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.setup_taskbar()
        
        # Apply slide-in animation
        SlideIn(self, 'bottom')
    
    def setup_taskbar(self):
        # Start button
        self.start_btn = tk.Button(self, text="Nexus", bg='#2d2d2d', fg='white',
                                 bd=0, padx=15, font=('Segoe UI', 10, 'bold'),
                                 command=self.toggle_start_menu)
        self.start_btn.pack(side=tk.LEFT, fill=tk.Y)
        
        # Task view (for open apps)
        self.task_view = tk.Frame(self, bg='#1a1a1a')
        self.task_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # System tray
        self.tray = tk.Frame(self, bg='#1a1a1a')
        self.tray.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add system tray icons (example: clock, network, volume)
        self.add_tray_icons()
        
        # Start menu (initially hidden)
        self.start_menu = None
    
    def add_tray_icons(self):
        # Clock
        self.clock_label = tk.Label(self.tray, text="", bg='#1a1a1a', fg='white', 
                                  font=('Segoe UI', 9))
        self.clock_label.pack(side=tk.RIGHT, padx=5)
        self.update_clock()
        
        # Network icon
        self.add_tray_icon("network.png", "Network")
        
        # Volume icon
        self.add_tray_icon("volume.png", "Volume")
        
        # Battery icon
        self.add_tray_icon("battery.png", "Battery")
    
    def add_tray_icon(self, icon_name, tooltip):
        try:
            icon_path = f"assets/icons/{icon_name}"
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                img = img.resize((20, 20), Image.Resampling.LANCZOS)
                icon = ImageTk.PhotoImage(img)
                
                btn = tk.Label(self.tray, image=icon, bg='#1a1a1a')
                btn.image = icon  # Keep a reference
                btn.pack(side=tk.RIGHT, padx=2)
                
                # Add tooltip
                self.add_tooltip(btn, tooltip)
        except Exception as e:
            print(f"Error loading tray icon {icon_name}: {e}")
    
    def add_tooltip(self, widget, text):
        widget.bind("<Enter>", lambda e, t=text: self.show_tooltip(e, t))
        widget.bind("<Leave>", lambda e: self.hide_tooltip())
    
    def show_tooltip(self, event, text):
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx() + 25
        y += event.widget.winfo_rooty() + 25
        
        self.tooltip = tk.Toplevel(event.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=text, bg="#2d2d2d", fg="white", 
                        relief='solid', borderwidth=1, padx=5, pady=2)
        label.pack()
    
    def hide_tooltip(self):
        if hasattr(self, 'tooltip') and self.tooltip.winfo_exists():
            self.tooltip.destroy()
    
    def update_clock(self):
        current_time = time.strftime('%H:%M')
        self.clock_label.config(text=current_time)
        self.after(1000, self.update_clock)
    
    def toggle_start_menu(self):
        if hasattr(self, 'start_menu') and self.start_menu.winfo_exists():
            self.hide_start_menu()
        else:
            self.show_start_menu()
    
    def show_start_menu(self):
        if hasattr(self, 'start_menu') and self.start_menu.winfo_exists():
            return
            
        self.start_menu = tk.Toplevel(self, bg='#2d2d2d', bd=0)
        self.start_menu.overrideredirect(True)
        self.start_menu.attributes('-topmost', True)
        
        # Position menu above taskbar
        x = 0
        y = self.winfo_rooty() - 500  # Menu height
        self.start_menu.geometry(f"300x500+{x}+{y}")
        
        # Add menu content
        self.setup_start_menu_content()
        
        # Bind focus out event
        self.start_menu.bind("<FocusOut>", lambda e: self.hide_start_menu())
    
    def hide_start_menu(self):
        if hasattr(self, 'start_menu') and self.start_menu.winfo_exists():
            self.start_menu.destroy()
    
    def setup_start_menu_content(self):
        # User profile section
        user_frame = tk.Frame(self.start_menu, bg='#1a73e8', padx=10, pady=10)
        user_frame.pack(fill=tk.X)
        
        user_icon = tk.Label(user_frame, text="👤", font=('Segoe UI', 24), 
                            bg='#1a73e8', fg='white')
        user_icon.pack(side=tk.LEFT, padx=5)
        
        user_info = tk.Frame(user_frame, bg='#1a73e8')
        user_info.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(user_info, text="User", font=('Segoe UI', 10), 
                bg='#1a73e8', fg='rgba(255,255,255,0.9)').pack(anchor='w')
        tk.Label(user_info, text="user@nexus", font=('Segoe UI', 8), 
                bg='#1a73e8', fg='rgba(255,255,255,0.7)').pack(anchor='w')
        
        # App list
        app_frame = tk.Frame(self.start_menu, bg='#2d2d2d')
        app_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add some app shortcuts
        apps = [
            ("📁", "File Explorer", self.open_file_explorer),
            ("🌐", "Web Browser", self.open_browser),
            ("📝", "Text Editor", self.open_text_editor),
            ("⚙️", "Settings", self.open_settings),
            ("📊", "System Monitor", self.open_system_monitor),
            ("🎮", "Games", self.open_games),
            ("📚", "Documents", self.open_documents)
        ]
        
        for icon, name, cmd in apps:
            btn = tk.Button(app_frame, text=f"  {icon}  {name}", 
                          anchor='w', bd=0, padx=10, pady=8,
                          bg='#2d2d2d', fg='white',
                          font=('Segoe UI', 10),
                          command=cmd)
            btn.pack(fill=tk.X, pady=1)
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#3d3d3d'))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#2d2d2d'))
        
        # Power options at the bottom
        power_frame = tk.Frame(self.start_menu, bg='#252525', height=40)
        power_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        power_icons = [
            ("🔒", "Lock", self.lock_screen),
            ("👤", "Sign out", self.sign_out),
            ("⏻", "Power", self.shutdown)
        ]
        
        for icon, tooltip, cmd in power_icons:
            btn = tk.Button(power_frame, text=icon, bg='#252525', fg='white',
                          bd=0, padx=10, font=('Segoe UI', 12),
                          command=cmd)
            btn.pack(side=tk.LEFT, fill=tk.Y)
            self.add_tooltip(btn, tooltip)
    
    # Placeholder methods for menu actions
    def open_file_explorer(self):
        print("Opening File Explorer")
    
    def open_browser(self):
        print("Opening Web Browser")
    
    def open_text_editor(self):
        print("Opening Text Editor")
    
    def open_settings(self):
        print("Opening Settings")
    
    def open_system_monitor(self):
        print("Opening System Monitor")
    
    def open_games(self):
        print("Opening Games")
    
    def open_documents(self):
        print("Opening Documents")
    
    def lock_screen(self):
        print("Locking screen")
        self.hide_start_menu()
    
    def sign_out(self):
        print("Signing out")
        self.hide_start_menu()
        self.parent.quit()
    
    def shutdown(self):
        print("Shutting down")
        self.parent.destroy()
