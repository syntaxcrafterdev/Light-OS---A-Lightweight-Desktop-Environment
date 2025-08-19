print("Testing imports...")

try:
    import tkinter as tk
    print("✓ tkinter")
except ImportError as e:
    print(f"✗ tkinter: {e}")

try:
    from PIL import Image, ImageTk
    print("✓ PIL (Pillow)")
except ImportError as e:
    print(f"✗ PIL (Pillow): {e}")

try:
    import psutil
    print("✓ psutil")
except ImportError as e:
    print(f"✗ psutil: {e}")

print("\nTesting local imports...")

try:
    from desktop import Desktop
    print("✓ desktop")
except ImportError as e:
    print(f"✗ desktop: {e}")

try:
    from utils.theme import set_theme
    print("✓ utils.theme")
except ImportError as e:
    print(f"✗ utils.theme: {e}")

print("\nTesting widget imports...")

try:
    from widgets.clock import ClockWidget
    print("✓ widgets.clock")
except ImportError as e:
    print(f"✗ widgets.clock: {e}")

try:
    from widgets.weather import WeatherWidget
    print("✓ widgets.weather")
except ImportError as e:
    print(f"✗ widgets.weather: {e}")

try:
    from widgets.system_monitor import SystemMonitor
    print("✓ widgets.system_monitor")
except ImportError as e:
    print(f"✗ widgets.system_monitor: {e}")

print("\nTest complete.")
