import tkinter as tk
from tkinter import ttk

# Color schemes
THEMES = {
    'dark': {
        'primary': '#1a73e8',
        'secondary': '#2d2d2d',
        'background': '#1a1a1a',
        'surface': '#252525',
        'text_primary': '#ffffff',
        'text_secondary': '#b3b3b3',
        'accent': '#1a73e8',
        'error': '#cf6679',
        'success': '#4caf50',
        'warning': '#ff9800',
        'border': '#3d3d3d',
        'hover': '#3d3d3d',
        'active': '#4d4d4d',
    },
    'light': {
        'primary': '#1976d2',
        'secondary': '#f5f5f5',
        'background': '#ffffff',
        'surface': '#f0f0f0',
        'text_primary': '#212121',
        'text_secondary': '#666666',
        'accent': '#1976d2',
        'error': '#d32f2f',
        'success': '#388e3c',
        'warning': '#f57c00',
        'border': '#e0e0e0',
        'hover': '#e0e0e0',
        'active': '#d0d0d0',
    }
}

# Current theme
current_theme = 'dark'

def set_theme(theme_name='dark'):
    """Set the application theme"""
    global current_theme
    if theme_name in THEMES:
        current_theme = theme_name
        apply_theme()
    else:
        print(f"Theme '{theme_name}' not found. Using default theme.")
        current_theme = 'dark'
        apply_theme()

def get_theme():
    """Get the current theme colors"""
    return THEMES.get(current_theme, THEMES['dark'])

def apply_theme():
    """Apply the current theme to ttk styles"""
    theme = get_theme()
    
    # Create style object
    style = ttk.Style()
    
    # Configure the main window background
    style.configure('.', background=theme['background'])
    
    # Configure ttk widgets
    style.configure('TFrame', background=theme['background'])
    style.configure('TLabel', background=theme['background'], 
                   foreground=theme['text_primary'])
    style.configure('TButton', background=theme['secondary'], 
                   foreground=theme['text_primary'],
                   borderwidth=1, relief='flat')
    style.map('TButton',
             background=[('active', theme['hover']), 
                        ('pressed', theme['active'])])
    
    # Configure entry widgets
    style.configure('TEntry', fieldbackground=theme['surface'],
                   foreground=theme['text_primary'],
                   borderwidth=1, relief='solid')
    
    # Configure scrollbars
    style.configure('Vertical.TScrollbar', background=theme['secondary'],
                   arrowcolor=theme['text_primary'],
                   bordercolor=theme['border'],
                   arrowsize=12)
    
    # Configure notebook (tabs)
    style.configure('TNotebook', background=theme['background'],
                   borderwidth=0)
    style.configure('TNotebook.Tab', 
                   background=theme['secondary'],
                   foreground=theme['text_primary'],
                   padding=[10, 5],
                   borderwidth=0)
    style.map('TNotebook.Tab',
             background=[('selected', theme['primary']), 
                        ('active', theme['hover'])],
             foreground=[('selected', '#ffffff'),
                       ('active', theme['text_primary'])],
             expand=[('selected', [1, 1, 1, 0])])
    
    # Configure treeview
    style.configure('Treeview', 
                   background=theme['surface'],
                   foreground=theme['text_primary'],
                   fieldbackground=theme['surface'],
                   borderwidth=0,
                   rowheight=25)
    style.map('Treeview', 
             background=[('selected', theme['primary'])],
             foreground=[('selected', '#ffffff')])
    
    # Configure scrollbars for treeview
    style.configure('Treeview.Horizontal.TSeparator', 
                   background=theme['border'])
    style.configure('Treeview', 
                   rowheight=25,
                   background=theme['surface'],
                   fieldbackground=theme['surface'],
                   foreground=theme['text_primary'],
                   borderwidth=0)
    style.map('Treeview', 
             background=[('selected', theme['primary'])],
             foreground=[('selected', '#ffffff')])
    
    # Configure progressbar
    style.configure('Horizontal.TProgressbar',
                   background=theme['primary'],
                   troughcolor=theme['surface'],
                   borderwidth=0,
                   lightcolor=theme['primary'],
                   darkcolor=theme['primary'])
    
    # Configure checkbutton and radiobutton
    style.configure('TCheckbutton',
                   background=theme['background'],
                   foreground=theme['text_primary'])
    style.configure('TRadiobutton',
                   background=theme['background'],
                   foreground=theme['text_primary'])
    
    # Configure combobox
    style.map('TCombobox',
             fieldbackground=[('readonly', theme['surface'])],
             selectbackground=[('readonly', theme['surface'])],
             selectforeground=[('readonly', theme['text_primary'])])
    
    # Configure scrollbar
    style.configure('TScrollbar',
                   background=theme['secondary'],
                   troughcolor=theme['background'],
                   arrowcolor=theme['text_primary'],
                   bordercolor=theme['border'],
                   arrowsize=12)
    style.map('TScrollbar',
             background=[('active', theme['hover']), 
                        ('pressed', theme['active'])])

# Initialize with default theme
set_theme('dark')
