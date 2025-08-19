<div align="center">
  <h1>✨ Light OS</h1>
  <p><b>A sleek, lightweight desktop environment built with Python and Tkinter</b></p>
  
  ![Demo](https://via.placeholder.com/800x500/1a1a1a/ffffff?text=Light+OS+Demo)
  
  [![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
</div>

## 🚀 Features

- 🎨 **Modern Dark Theme** - Easy on the eyes with smooth animations
- 🧩 **Modular Widgets** - Customize your desktop with various widgets
- ⚡ **Performance Monitor** - Real-time system stats at a glance
- 🌦️ **Weather Integration** - Stay updated with current weather conditions
- 🚀 **App Launcher** - Quick access to your favorite applications
- 🛠️ **Developer Friendly** - Easy to extend and customize

## 🛠️ Installation

1. **Prerequisites**
   - Python 3.8+
   - pip package manager

2. **Installation**
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/light-os.git
   cd light-os
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run Light OS
   python -m light_os
   ```

## ⚙️ Configuration

### Weather Widget Setup
1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Create a `.env` file:
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

### Customization
Edit `utils/theme.py` to customize colors and appearance.

## 📁 Project Structure

```
light_os/
├── __main__.py         # Application entry point
├── desktop.py          # Desktop manager
├── widgets/            # Custom widgets
│   ├── app_launcher.py
│   ├── clock.py
│   ├── system_monitor.py
│   └── weather.py
└── utils/              # Utility modules
    ├── animations.py   # UI animations
    └── theme.py        # Theme configuration

## Keyboard Shortcuts

- `Ctrl+Alt+Delete`: Open system menu
- `Right-click` on desktop: Open context menu

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
