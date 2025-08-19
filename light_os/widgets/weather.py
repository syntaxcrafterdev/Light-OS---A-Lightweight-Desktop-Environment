import tkinter as tk
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import io
from utils.animations import HoverEffect

class WeatherWidget:
    def __init__(self, parent, x=20, y=150):
        self.parent = parent
        self.x = x
        self.y = y
        self.visible = True
        self.api_key = ""  # You'll need to get an API key from OpenWeatherMap
        self.city = "New York"
        self.units = "metric"  # or "imperial"
        
        # Create weather frame
        self.frame = tk.Frame(parent, bg='#1a1a1a', bd=0)
        self.frame.place(x=x, y=y)
        
        # Weather icon
        self.icon_label = tk.Label(self.frame, bg='#1a1a1a')
        self.icon_label.pack(anchor='w')
        
        # Temperature
        self.temp_font = ('Segoe UI', 16, 'bold')
        self.temp_label = tk.Label(
            self.frame,
            text="--°C",
            font=self.temp_font,
            fg='white',
            bg='#1a1a1a',
            padx=15,
            pady=5
        )
        self.temp_label.pack(anchor='w')
        
        # Weather description
        self.desc_font = ('Segoe UI', 10)
        self.desc_label = tk.Label(
            self.frame,
            text="No data",
            font=self.desc_font,
            fg='#cccccc',
            bg='#1a1a1a',
            padx=15,
            pady=5
        )
        self.desc_label.pack(anchor='w')
        
        # Location
        self.loc_font = ('Segoe UI', 9)
        self.loc_label = tk.Label(
            self.frame,
            text=self.city,
            font=self.loc_font,
            fg='#999999',
            bg='#1a1a1a',
            padx=15,
            pady=10
        )
        self.loc_label.pack(anchor='w')
        
        # Add hover effect
        HoverEffect(self.frame, '#1a1a1a', '#2d2d2d')
        
        # Bind right-click for context menu
        self.frame.bind("<Button-3>", self.show_context_menu)
        
        # Initial weather update
        self.update_weather()
    
    def update_weather(self):
        """Fetch and update weather data"""
        if self.visible and self.api_key:  # Only update if visible and API key is set
            try:
                # Get weather data from OpenWeatherMap API
                url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units={self.units}"
                response = requests.get(url)
                data = response.json()
                
                if response.status_code == 200:
                    # Update temperature
                    temp = data['main']['temp']
                    temp_unit = '°C' if self.units == 'metric' else '°F'
                    self.temp_label.config(text=f"{int(round(temp))}{temp_unit}")
                    
                    # Update description
                    desc = data['weather'][0]['description'].title()
                    self.desc_label.config(text=desc)
                    
                    # Update location
                    self.city = data['name']
                    self.loc_label.config(text=self.city)
                    
                    # Update icon
                    icon_code = data['weather'][0]['icon']
                    self.set_weather_icon(icon_code)
                
                # Schedule next update (every 30 minutes)
                self.parent.after(1800000, self.update_weather)
                
            except Exception as e:
                print(f"Error updating weather: {e}")
                # Retry after 5 minutes on error
                self.parent.after(300000, self.update_weather)
        else:
            # If not visible or no API key, try again in 1 minute
            self.parent.after(60000, self.update_weather)
    
    def set_weather_icon(self, icon_code):
        """Set the weather icon from OpenWeatherMap"""
        try:
            # Try to load icon from local cache first
            icon_path = f"assets/weather_icons/{icon_code}.png"
            img = Image.open(icon_path)
        except:
            try:
                # If not found locally, download from OpenWeatherMap
                url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                response = requests.get(url, stream=True)
                img = Image.open(io.BytesIO(response.content))
                
                # Save to cache for future use
                os.makedirs("assets/weather_icons", exist_ok=True)
                img.save(icon_path)
            except Exception as e:
                print(f"Error loading weather icon: {e}")
                return
        
        # Resize and set icon
        img = img.resize((64, 64), Image.Resampling.LANCZOS)
        self.weather_icon = ImageTk.PhotoImage(img)
        self.icon_label.config(image=self.weather_icon)
    
    def show_context_menu(self, event):
        """Show context menu for the weather widget"""
        menu = tk.Menu(self.parent, tearoff=0, bg='#2d2d2d', fg='white',
                      bd=0, font=('Segoe UI', 10))
        
        menu.add_command(label="Refresh", command=self.update_weather)
        menu.add_command(label="Change Location", command=self.change_location)
        menu.add_separator()
        menu.add_command(label="Hide Weather", command=self.toggle_visibility)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def change_location(self):
        """Open dialog to change location"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Change Location")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.configure(bg='#2d2d2d')
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        # Add widgets
        tk.Label(dialog, text="Enter city name:", bg='#2d2d2d', fg='white').pack(pady=10)
        
        city_var = tk.StringVar(value=self.city)
        entry = ttk.Entry(dialog, textvariable=city_var, width=30)
        entry.pack(pady=5, padx=20)
        entry.focus()
        
        def save_location():
            new_city = city_var.get().strip()
            if new_city:
                self.city = new_city
                self.update_weather()
                dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Save", command=save_location).pack(side='left', padx=5)
    
    def toggle_visibility(self):
        """Toggle widget visibility"""
        self.visible = not self.visible
        if self.visible:
            self.frame.place(x=self.x, y=self.y)
            self.update_weather()
        else:
            self.frame.place_forget()
    
    def set_position(self, x, y):
        """Set widget position"""
        self.x = x
        self.y = y
        self.frame.place(x=x, y=y)
    
    def destroy(self):
        """Clean up the widget"""
        self.frame.destroy()
