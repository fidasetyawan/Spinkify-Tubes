import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Premium Dark Theme Colors
BG_COLOR = "#1f1f1f"           # Main background
SIDEBAR_BG = "#252525"         # Sidebar/panel background
CARD_COLOR = "#333333"         # Song cards, containers
ACCENT_COLOR = "#ff69b4"       # Primary pink accent
ACCENT_SOFT = "#ff86c4"        # Soft pink for hover/highlights
FG_COLOR = "#ffffff"           # Primary text
SECONDARY_COLOR = "#cfcfcf"    # Secondary text
BORDER_COLOR = "#404040"       # Subtle borders
MINI_PLAYER_BG = "#282828"     # Bottom control bar

# Fonts
HEADER_FONT = ("Helvetica", 20, "bold")
SUBHEADER_FONT = ("Helvetica", 12, "bold")
BODY_FONT = ("Helvetica", 10)
CAPTION_FONT = ("Helvetica", 9)

def load_icon(name, size=(24, 24)):
    path = os.path.join("assets", name)
    if os.path.exists(path):
        img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    return None

def setup_styles():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Frame
    style.configure("TFrame", background=BG_COLOR)
    style.configure("Card.TFrame", background=CARD_COLOR)
    style.configure("Sidebar.TFrame", background=SIDEBAR_BG)
    
    # Label
    style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=BODY_FONT)
    style.configure("Card.TLabel", background=CARD_COLOR, foreground=FG_COLOR, font=BODY_FONT)
    style.configure("Header.TLabel", font=HEADER_FONT, foreground=ACCENT_COLOR, background=BG_COLOR)
    
    # Button - Modern flat style
    style.configure("TButton", 
                    background=ACCENT_COLOR, 
                    foreground=FG_COLOR, 
                    borderwidth=0,
                    focuscolor='none',
                    font=BODY_FONT,
                    padding=10)
    style.map("TButton",
              background=[('active', ACCENT_SOFT), ('pressed', ACCENT_COLOR)])
    
    # Treeview
    style.configure("Treeview",
                    background=CARD_COLOR,
                    foreground=FG_COLOR,
                    fieldbackground=CARD_COLOR,
                    borderwidth=0,
                    rowheight=60)
    style.map('Treeview', background=[('selected', ACCENT_COLOR)])
