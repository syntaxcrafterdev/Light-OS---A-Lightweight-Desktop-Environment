import tkinter as tk
from tkinter import font as tkfont
import time
from utils.animations import HoverEffect

class ClockWidget:
    def __init__(self, parent, x=20, y=20):
        self.parent = parent
        self.x = x
        self.y = y
        self.visible = True
        
        # Create clock frame with solid color (Tkinter doesn't support alpha in colors)
        self.frame = tk.Frame(parent, bg='#1a1a1a', bd=0)
        self.frame.place(x=x, y=y)
        
        # Time label
        self.time_font = tkfont.Font(family='Segoe UI', size=24, weight='bold')
        self.time_label = tk.Label(
            self.frame, 
            text="00:00:00",
            font=self.time_font,
            fg='white',
            bg='#1a1a1a',
            padx=15,
            pady=5
        )
        self.time_label.pack(expand=True, fill='both')
        
        # Date label
        self.date_font = tkfont.Font(family='Segoe UI', size=10)
        self.date_label = tk.Label(
            self.frame,
            text="",
            font=self.date_font,
            fg='#cccccc',
            bg='#1a1a1a',
            padx=15,
            pady=5
        )
        self.date_label.pack(expand=True, fill='both')
        
        # Add hover effect
        HoverEffect(self.frame, '#1a1a1a80', '#2d2d2dcc')
        
        # Bind right-click for context menu
        self.frame.bind("<Button-3>", self.show_context_menu)
        
        # Start clock
        self.update_clock()
    
    def update_clock(self):
        """Update the clock display"""
        if self.visible:
            # Get current time
            current_time = time.strftime('%H:%M:%S')
            current_date = time.strftime('%A, %B %d, %Y')
            
            # Update labels
            self.time_label.config(text=current_time)
            self.date_label.config(text=current_date)
            
            # Schedule next update
            self.parent.after(1000, self.update_clock)
    
    def show_context_menu(self, event):
        """Show context menu for the clock"""
        menu = tk.Menu(self.parent, tearoff=0, bg='#2d2d2d', fg='white',
                      bd=0, font=('Segoe UI', 10))
        
        menu.add_command(label="Hide Clock", command=self.toggle_visibility)
        menu.add_separator()
        menu.add_command(label="Change Position")
        menu.add_command(label="Settings")
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def toggle_visibility(self):
        """Toggle clock visibility"""
        self.visible = not self.visible
        if self.visible:
            self.frame.place(x=self.x, y=self.y)
            self.update_clock()
        else:
            self.frame.place_forget()
    
    def set_position(self, x, y):
        """Set the position of the clock"""
        self.x = x
        self.y = y
        self.frame.place(x=x, y=y)
    
    def destroy(self):
        """Clean up the widget"""
        self.frame.destroy()
