import tkinter as tk
from .styles import BG_COLOR, setup_styles
from .auth import LoginFrame
from .admin import AdminFrame
from .user import UserFrame
from .player import NowPlayingFrame

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("SPINKIFY")
        self.geometry("900x600")
        self.configure(bg=BG_COLOR)
        
        setup_styles()

        self.current_frame = None
        self.show_login()

    def switch_frame(self, frame_class):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self, self.controller)
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self):
        self.switch_frame(LoginFrame)

    def show_admin(self):
        self.switch_frame(AdminFrame)

    def show_user(self):
        self.switch_frame(UserFrame)
        
    def show_now_playing(self):
        self.switch_frame(NowPlayingFrame)
