import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import json
from utils.animations import HoverEffect, SlideIn

class AppLauncher:
    def __init__(self, parent):
        self.parent = parent
        self.apps = []
        self.icon_size = 48
        self.visible = True
        
        # Create the launcher bar
        self.create_launcher()
        
        # Load apps
        self.load_apps()
        
        # Add default apps if none found
        if not self.apps:
            self.add_default_apps()
    
    def create_launcher(self):
        """Create the app launcher/dock"""
        # Main frame for the launcher
        self.frame = tk.Frame(self.parent, bg='#1a1a1a', bd=0)
        self.frame.place(relx=0.5, rely=1.0, anchor='s', y=-20)
        
        # Container for app icons
        self.apps_frame = tk.Frame(self.frame, bg='#1a1a1a')
        self.apps_frame.pack(side='left', padx=10, pady=5)
        
        # Add some padding at the bottom for visual balance
        tk.Frame(self.frame, width=10, bg='#1a1a1a').pack(side='right')
        
        # Bind right-click for context menu
        self.frame.bind("<Button-3>", self.show_context_menu)
        
        # Apply slide-in animation
        SlideIn(self.frame, 'bottom')
    
    def load_apps(self):
        """Load apps from configuration"""
        config_path = "config/apps.json"
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    self.apps = json.load(f)
                    self.update_launcher()
        except Exception as e:
            print(f"Error loading apps: {e}")
    
    def save_apps(self):
        """Save apps to configuration"""
        config_path = "config/apps.json"
        try:
            os.makedirs("config", exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(self.apps, f, indent=4)
        except Exception as e:
            print(f"Error saving apps: {e}")
    
    def add_default_apps(self):
        """Add some default apps"""
        self.apps = [
            {"name": "File Explorer", "icon": "📁", "command": "explorer"},
            {"name": "Web Browser", "icon": "🌐", "command": "start msedge"},
            {"name": "Text Editor", "icon": "📝", "command": "notepad"},
            {"name": "Terminal", "icon": "💻", "command": "cmd"},
            {"name": "Calculator", "icon": "🧮", "command": "calc"},
            {"name": "Settings", "icon": "⚙️", "command": "ms-settings:"}
        ]
        self.save_apps()
        self.update_launcher()
    
    def update_launcher(self):
        """Update the launcher with current apps"""
        # Clear existing widgets
        for widget in self.apps_frame.winfo_children():
            widget.destroy()
        
        # Add app buttons
        for app in self.apps:
            self.add_app_button(app)
    
    def add_app_button(self, app):
        """Add a single app button to the launcher"""
        btn_frame = tk.Frame(self.apps_frame, bg='transparent')
        btn_frame.pack(side='left', padx=2)
        
        # Create button with icon
        btn = tk.Label(
            btn_frame,
            text=app.get('icon', '📁'),
            font=('Segoe UI Emoji', 24),
            bg='transparent',
            fg='white',
            cursor='hand2',
            padx=5,
            pady=5
        )
        btn.pack()
        
        # Add tooltip
        self.add_tooltip(btn, app['name'])
        
        # Bind events
        btn.bind("<Button-1>", lambda e, cmd=app.get('command', ''): self.launch_app(cmd))
        
        # Add hover effect
        HoverEffect(btn, 'transparent', '#3d3d3dcc')
    
    def add_tooltip(self, widget, text):
        """Add a tooltip to a widget"""
        widget.tooltip = None
        
        def on_enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            widget.tooltip = tk.Toplevel(widget)
            widget.tooltip.wm_overrideredirect(True)
            widget.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(
                widget.tooltip, 
                text=text, 
                bg="#2d2d2d", 
                fg="white",
                relief='solid', 
                borderwidth=1,
                padx=5, 
                pady=2
            )
            label.pack()
        
        def on_leave(event):
            if widget.tooltip:
                widget.tooltip.destroy()
                widget.tooltip = None
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def launch_app(self, command):
        """Launch an application"""
        try:
            if command:
                os.system(f"start {command}")
        except Exception as e:
            print(f"Error launching app: {e}")
    
    def show_context_menu(self, event):
        """Show context menu for the launcher"""
        menu = tk.Menu(self.parent, tearoff=0, bg='#2d2d2d', fg='white',
                      bd=0, font=('Segoe UI', 10))
        
        menu.add_command(label="Add Application", command=self.add_application)
        menu.add_command(label="Edit Launcher", command=self.edit_launcher)
        menu.add_separator()
        menu.add_command(label="Hide Launcher", command=self.toggle_visibility)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def add_application(self):
        """Open dialog to add a new application"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Application")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.configure(bg='#2d2d2d')
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Form fields
        fields = [
            ("Name:", ""),
            ("Command:", ""),
            ("Icon (emoji or filename):", "📁")
        ]
        
        entries = []
        for i, (label_text, default) in enumerate(fields):
            frame = tk.Frame(dialog, bg='#2d2d2d')
            frame.pack(fill='x', padx=20, pady=5)
            
            tk.Label(frame, text=label_text, bg='#2d2d2d', fg='white',
                    font=('Segoe UI', 10)).pack(side='left')
            
            entry = ttk.Entry(frame, width=30)
            entry.insert(0, default)
            entry.pack(side='right', fill='x', expand=True)
            entries.append(entry)
        
        # Preview
        preview_frame = tk.Frame(dialog, bg='#2d2d2d', pady=10)
        preview_frame.pack(fill='x')
        
        preview_label = tk.Label(preview_frame, text="Preview:", 
                               bg='#2d2d2d', fg='white')
        preview_label.pack()
        
        preview_btn = tk.Label(preview_frame, text="📁", 
                             font=('Segoe UI Emoji', 24),
                             bg='#3d3d3d', fg='white')
        preview_btn.pack(pady=5)
        
        # Update preview when typing
        def update_preview():
            try:
                preview_btn.config(text=entries[2].get())
            except:
                pass
        
        for entry in entries:
            entry.bind('<KeyRelease>', lambda e: update_preview())
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        def save_app():
            name = entries[0].get().strip()
            command = entries[1].get().strip()
            icon = entries[2].get().strip()
            
            if name and command:
                self.apps.append({
                    "name": name,
                    "command": command,
                    "icon": icon
                })
                self.save_apps()
                self.update_launcher()
                dialog.destroy()
        
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Add", command=save_app).pack(side='left', padx=5)
    
    def edit_launcher(self):
        """Open dialog to edit launcher settings"""
        print("Edit launcher settings")
    
    def toggle_visibility(self):
        """Toggle launcher visibility"""
        self.visible = not self.visible
        if self.visible:
            self.frame.place(relx=0.5, rely=1.0, anchor='s', y=-20)
        else:
            self.frame.place_forget()
    
    def destroy(self):
        """Clean up the launcher"""
        if hasattr(self, 'frame') and self.frame.winfo_exists():
            self.frame.destroy()
