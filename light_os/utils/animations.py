import tkinter as tk
import time

class FadeIn:
    def __init__(self, window, duration=300):
        self.window = window
        self.duration = duration
        self.steps = 20
        self.step = 0
        self.alpha = 0.0
        
        # Set initial transparency
        self.window.attributes('-alpha', self.alpha)
        self.animate_in()
    
    def animate_in(self):
        if self.step <= self.steps:
            self.alpha = self.ease_out(self.step / self.steps)
            self.window.attributes('-alpha', self.alpha)
            self.step += 1
            self.window.after(self.duration // self.steps, self.animate_in)
    
    @staticmethod
    def ease_out(t):
        """Easing function for smooth animation"""
        return 1 - (1 - t) ** 2

class SlideIn:
    def __init__(self, widget, direction='right', duration=300):
        self.widget = widget
        self.direction = direction.lower()
        self.duration = duration
        self.steps = 20
        self.step = 0
        
        # Store original position
        self.original_geometry = widget.winfo_geometry()
        self.original_place_info = widget.place_info()
        
        # Hide widget initially
        if 'x' in self.original_place_info and 'y' in self.original_place_info:
            self.original_x = int(self.original_place_info['x'])
            self.original_y = int(self.original_place_info['y'])
        else:
            self.original_x = widget.winfo_x()
            self.original_y = widget.winfo_y()
        
        # Calculate target position based on direction
        screen_width = widget.winfo_screenwidth()
        screen_height = widget.winfo_screenheight()
        
        if self.direction == 'top':
            self.start_y = -widget.winfo_height()
            self.start_x = self.original_x
        elif self.direction == 'bottom':
            self.start_y = screen_height
            self.start_x = self.original_x
        elif self.direction == 'left':
            self.start_x = -widget.winfo_width()
            self.start_y = self.original_y
        else:  # right
            self.start_x = screen_width
            self.start_y = self.original_y
        
        # Set initial position
        widget.place(x=self.start_x, y=self.start_y)
        
        # Start animation
        self.animate()
    
    def animate(self):
        if self.step <= self.steps:
            # Calculate current position
            progress = self.ease_out(self.step / self.steps)
            
            if self.direction in ['top', 'bottom']:
                y = self.start_y + (self.original_y - self.start_y) * progress
                x = self.original_x
            else:  # left or right
                x = self.start_x + (self.original_x - self.start_x) * progress
                y = self.original_y
            
            # Update position
            self.widget.place(x=int(x), y=int(y))
            
            self.step += 1
            self.widget.after(self.duration // self.steps, self.animate)
    
    @staticmethod
    def ease_out(t):
        """Easing function for smooth animation"""
        return 1 - (1 - t) ** 3

class HoverEffect:
    def __init__(self, widget, color_from, color_to, duration=200):
        self.widget = widget
        # Convert to solid colors by removing alpha channel
        self.color_from = color_from[:7] if len(color_from) > 7 else color_from
        self.color_to = color_to[:7] if len(color_to) > 7 else color_to
        self.duration = duration
        self.steps = 10
        
        # Set initial color
        self.widget.config(bg=self.color_from)
        
        # Bind events
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        
        # Current animation ID
        self.anim_id = None
    
    def on_enter(self, event):
        self.animate(self.color_from, self.color_to)
    
    def on_leave(self, event):
        self.animate(self.color_to, self.color_from)
    
    def animate(self, from_color, to_color):
        if self.anim_id is not None:
            self.widget.after_cancel(self.anim_id)
        
        # Convert colors to RGB
        from_rgb = self.hex_to_rgb(from_color)
        to_rgb = self.hex_to_rgb(to_color)
        
        # Calculate color steps
        steps = []
        for i in range(self.steps + 1):
            r = from_rgb[0] + (to_rgb[0] - from_rgb[0]) * i / self.steps
            g = from_rgb[1] + (to_rgb[1] - from_rgb[1]) * i / self.steps
            b = from_rgb[2] + (to_rgb[2] - from_rgb[2]) * i / self.steps
            steps.append(self.rgb_to_hex((int(r), int(g), int(b))))
        
        # Start animation
        self.animate_step(0, steps)
    
    def animate_step(self, step, colors):
        if step < len(colors):
            self.widget.config(bg=colors[step])
            self.anim_id = self.widget.after(
                self.duration // len(colors),
                lambda: self.animate_step(step + 1, colors)
            )
    
    @staticmethod
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb
