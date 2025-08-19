# Nexus OS - A Lightweight Desktop Environment

Nexus OS is a modern, lightweight desktop environment built with Python and Tkinter. It provides a clean, customizable interface with various widgets and features typically found in a desktop operating system.

## Features

- **Modern UI**: Sleek, dark-themed interface with smooth animations
- **Customizable Widgets**: Add, remove, and configure desktop widgets
- **App Launcher**: Quick access to your favorite applications
- **System Monitoring**: Real-time CPU, memory, and disk usage monitoring
- **Weather Updates**: Current weather information (requires API key)
- **Responsive Design**: Adapts to different screen sizes

## Installation

1. **Prerequisites**:
   - Python 3.8 or higher
   - pip (Python package manager)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Configuration

### Weather Widget
To enable the weather widget:
1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Create a `.env` file in the project root:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

### Customization
You can customize the appearance by modifying the theme settings in `utils/theme.py`.

## Project Structure

```
light_os/
├── main.py              # Main application entry point
├── desktop.py           # Desktop manager
├── taskbar.py           # Taskbar implementation
├── utils/               # Utility modules
│   ├── animations.py    # Animation effects
│   └── theme.py         # Theme and styling
├── widgets/             # Desktop widgets
│   ├── app_launcher.py  # Application launcher
│   ├── clock.py         # Clock widget
│   ├── system_monitor.py # System monitoring
│   └── weather.py       # Weather widget
├── assets/              # Static assets
│   ├── icons/           # Application icons
│   └── wallpapers/      # Desktop wallpapers
└── config/              # Configuration files
    └── apps.json        # Application shortcuts
```

## Keyboard Shortcuts

- `Ctrl+Alt+Delete`: Open system menu
- `Right-click` on desktop: Open context menu

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
