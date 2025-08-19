import tkinter as tk
from tkinter import ttk
import psutil
import platform
import os
import time
from utils.animations import HoverEffect

class SystemMonitor:
    def __init__(self, parent, x=20, y=300):
        self.parent = parent
        self.x = x
        self.y = y
        self.visible = True
        self.update_interval = 2000  # Update every 2 seconds
        
        # Create monitor frame
        self.frame = tk.Frame(parent, bg='#1a1a1a', bd=0)
        self.frame.place(x=x, y=y)
        
        # Title
        self.title_font = ('Segoe UI', 10, 'bold')
        self.title_label = tk.Label(
            self.frame,
            text="System Monitor",
            font=self.title_font,
            fg='white',
            bg='#1a1a1a',
            padx=15,
            pady=5
        )
        self.title_label.pack(anchor='w')
        
        # CPU usage
        self.cpu_frame = self.create_metric_frame("CPU:", "0%")
        self.cpu_bar = self.create_progress_bar()
        
        # Memory usage
        self.mem_frame = self.create_metric_frame("Memory:", "0%")
        self.mem_bar = self.create_progress_bar()
        
        # Disk usage
        self.disk_frame = self.create_metric_frame("Disk (C:):", "0%")
        self.disk_bar = self.create_progress_bar()
        
        # Network usage
        self.net_frame = self.create_metric_frame("Network:", "0 KB/s")
        
        # System info
        self.info_font = ('Segoe UI', 8)
        self.info_label = tk.Label(
            self.frame,
            text=self.get_system_info(),
            font=self.info_font,
            fg='#999999',
            bg='#1a1a1a',
            justify='left',
            padx=15,
            pady=10
        )
        self.info_label.pack(anchor='w', fill='x')
        
        # Add hover effect
        HoverEffect(self.frame, '#1a1a1a', '#2d2d2d')
        
        # Store previous network stats
        self.prev_net_io = psutil.net_io_counters()
        self.prev_time = time.time()
        
        # Bind right-click for context menu
        self.frame.bind("<Button-3>", self.show_context_menu)
        
        # Start updates
        self.update_metrics()
    
    def create_metric_frame(self, label_text, value_text):
        """Create a frame for a metric with label and value"""
        frame = tk.Frame(self.frame, bg='#1a1a1a')
        frame.pack(fill='x', padx=15, pady=2)
        
        # Label
        label = tk.Label(
            frame,
            text=label_text,
            font=('Segoe UI', 9),
            fg='#cccccc',
            bg='#1a1a1a',
            width=10,
            anchor='w'
        )
        label.pack(side='left')
        
        # Value
        value = tk.Label(
            frame,
            text=value_text,
            font=('Segoe UI', 9, 'bold'),
            fg='white',
            bg='#1a1a1a',
            width=8,
            anchor='e'
        )
        value.pack(side='right')
        
        return frame, value
    
    def create_progress_bar(self):
        """Create a progress bar for metrics"""
        frame = tk.Frame(self.frame, bg='#1a1a1a', height=4)
        frame.pack(fill='x', padx=15, pady=5)
        
        # Create a canvas for the progress bar
        canvas = tk.Canvas(frame, height=4, bg='#333333', highlightthickness=0)
        canvas.pack(fill='x')
        
        # Draw the background
        canvas.create_rectangle(0, 0, 200, 4, fill='#333333', outline='')
        
        # Draw the progress
        progress = canvas.create_rectangle(0, 0, 0, 4, fill='#4CAF50', outline='')
        
        return canvas, progress
    
    def update_metrics(self):
        """Update all system metrics"""
        if not self.visible:
            self.parent.after(self.update_interval, self.update_metrics)
            return
        
        try:
            # CPU Usage
            cpu_percent = psutil.cpu_percent(interval=None)
            self.update_metric(self.cpu_frame[1], self.cpu_bar, cpu_percent, f"{cpu_percent:.1f}%")
            
            # Memory Usage
            memory = psutil.virtual_memory()
            mem_percent = memory.percent
            mem_used = memory.used / (1024 ** 3)  # Convert to GB
            mem_total = memory.total / (1024 ** 3)
            self.update_metric(
                self.mem_frame[1], 
                self.mem_bar, 
                mem_percent, 
                f"{mem_percent:.1f}% ({mem_used:.1f}/{mem_total:.1f} GB)"
            )
            
            # Disk Usage (C: drive)
            try:
                disk = psutil.disk_usage('C:')
                disk_percent = disk.percent
                disk_used = disk.used / (1024 ** 3)  # Convert to GB
                disk_total = disk.total / (1024 ** 3)
                self.update_metric(
                    self.disk_frame[1],
                    self.disk_bar,
                    disk_percent,
                    f"{disk_percent:.1f}% ({disk_used:.1f}/{disk_total:.1f} GB)"
                )
            except Exception as e:
                print(f"Error getting disk usage: {e}")
            
            # Network Usage
            current_time = time.time()
            current_net_io = psutil.net_io_counters()
            time_diff = current_time - self.prev_time
            
            bytes_sent = current_net_io.bytes_sent - self.prev_net_io.bytes_sent
            bytes_recv = current_net_io.bytes_recv - self.prev_net_io.bytes_recv
            
            sent_speed = bytes_sent / time_diff
            recv_speed = bytes_recv / time_diff
            
            # Convert to appropriate units
            def format_speed(speed):
                for unit in ['B/s', 'KB/s', 'MB/s', 'GB/s']:
                    if speed < 1024 or unit == 'GB/s':
                        return f"{speed:.1f} {unit}"
                    speed /= 1024
            
            sent_str = format_speed(sent_speed)
            recv_str = format_speed(recv_speed)
            
            self.net_frame[1].config(text=f"↑{sent_str} ↓{recv_str}")
            
            # Update previous values
            self.prev_net_io = current_net_io
            self.prev_time = current_time
            
            # Update system info (less frequently)
            if int(time.time()) % 5 == 0:  # Update every 5 seconds
                self.info_label.config(text=self.get_system_info())
            
        except Exception as e:
            print(f"Error updating system metrics: {e}")
        
        # Schedule next update
        self.parent.after(self.update_interval, self.update_metrics)
    
    def update_metric(self, value_label, progress_bar, percent, text):
        """Update a single metric"""
        value_label.config(text=text)
        
        # Update progress bar
        canvas, progress = progress_bar
        width = canvas.winfo_width()
        if width <= 1:  # If not yet rendered, use default width
            width = 200
        
        progress_width = int((percent / 100) * width)
        canvas.coords(progress, 0, 0, progress_width, 4)
        
        # Change color based on usage
        if percent > 90:
            canvas.itemconfig(progress, fill='#f44336')  # Red
        elif percent > 70:
            canvas.itemconfig(progress, fill='#ff9800')  # Orange
        else:
            canvas.itemconfig(progress, fill='#4CAF50')  # Green
    
    def get_system_info(self):
        """Get basic system information"""
        try:
            # CPU Info
            cpu_info = f"CPU: {psutil.cpu_count(logical=False)}C/{psutil.cpu_count()}T {psutil.cpu_freq().current/1000:.1f}GHz"
            
            # OS Info
            os_info = f"{platform.system()} {platform.release()}"
            
            # Boot Time
            boot_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.boot_time()))
            
            # Uptime
            uptime_seconds = time.time() - psutil.boot_time()
            days = int(uptime_seconds // (24 * 3600))
            hours = int((uptime_seconds % (24 * 3600)) // 3600)
            uptime = f"{days}d {hours}h"
            
            return f"{cpu_info} | {os_info} | Boot: {boot_time} | Uptime: {uptime}"
            
        except Exception as e:
            print(f"Error getting system info: {e}")
            return "System information not available"
    
    def show_context_menu(self, event):
        """Show context menu for the system monitor"""
        menu = tk.Menu(self.parent, tearoff=0, bg='#2d2d2d', fg='white',
                      bd=0, font=('Segoe UI', 10))
        
        menu.add_command(label="Refresh", command=self.update_metrics)
        menu.add_separator()
        menu.add_command(label="Hide Monitor", command=self.toggle_visibility)
        menu.add_command(label="Settings")
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def toggle_visibility(self):
        """Toggle widget visibility"""
        self.visible = not self.visible
        if self.visible:
            self.frame.place(x=self.x, y=self.y)
            self.update_metrics()
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
