import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from .styles import BG_COLOR, CARD_COLOR, ACCENT_COLOR, FG_COLOR, SECONDARY_COLOR, BODY_FONT, load_icon

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg=BG_COLOR):
        super().__init__(parent, bg=bg)
        
        # Custom styled scrollbar
        style = ttk.Style()
        style.configure("Custom.Vertical.TScrollbar",
                       background="#2a2a2a",
                       troughcolor=BG_COLOR,
                       borderwidth=0,
                       arrowsize=0,
                       width=8)
        style.map("Custom.Vertical.TScrollbar",
                 background=[('active', '#404040'), ('!active', '#2a2a2a')])
        
        self.canvas = tk.Canvas(self, bg=bg, bd=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview, style="Custom.Vertical.TScrollbar")
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_reqwidth())
        
        # Resize canvas window to match canvas width
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Mousewheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class SongRow(tk.Frame):
    def __init__(self, parent, song, controller, on_play, on_add, width_hint=600):
        # Outer frame for shadow effect
        super().__init__(parent, bg=BG_COLOR, height=74)
        self.song = song
        self.controller = controller
        self.on_play = on_play
        self.on_add = on_add
        self.pack_propagate(False)
        
        # Shadow frame (darker background)
        shadow_frame = tk.Frame(self, bg="#1a1a1a")
        shadow_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Main card frame
        self.card = tk.Frame(shadow_frame, bg=CARD_COLOR)
        self.card.pack(fill="both", expand=True)
        
        self.chk_var = tk.BooleanVar(value=song.is_favorite)

        # Layout: Image | Title - Artist | Fav | Hover Actions
        
        # Image with padding
        self.img_lbl = tk.Label(self.card, bg=CARD_COLOR)
        self.img_lbl.place(x=16, y=12, width=50, height=50)
        self._load_image()

        # Text - Better typography
        tk.Label(self.card, text=song.title, font=("Helvetica", 11, "bold"), bg=CARD_COLOR, fg=FG_COLOR, anchor="w").place(x=82, y=16, width=360, height=20)
        tk.Label(self.card, text=song.artist, font=("Helvetica", 9), bg=CARD_COLOR, fg="#b0b0b0", anchor="w").place(x=82, y=40, width=360, height=16)

        # Favorite Button - Larger with hover effect
        self.icon_heart_emp = load_icon("heart_outline.png", (24, 24))
        self.icon_heart_fil = load_icon("heart_filled.png", (24, 24))
        
        self.btn_fav = tk.Label(self.card, bg=CARD_COLOR, cursor="hand2")
        self.btn_fav.place(x=width_hint-52, y=25, width=28, height=28)
        self.update_fav_icon()
        self.btn_fav.bind("<Button-1>", self.toggle_fav)

        # Hover Actions
        self.actions_frame = tk.Frame(self.card, bg=CARD_COLOR)
        self.actions_frame.place(x=width_hint-145, y=20, width=90, height=34) 
        self.actions_frame.place_forget() # Hide initially

        self.icon_play_sm = load_icon("play_small.png", (28, 28))
        self.icon_plus_sm = load_icon("plus_small.png", (28, 28))

        lbl_play = tk.Label(self.actions_frame, image=self.icon_play_sm, bg=CARD_COLOR, cursor="hand2")
        lbl_play.pack(side="left", padx=6)
        lbl_play.bind("<Button-1>", self.on_play_click)

        lbl_add = tk.Label(self.actions_frame, image=self.icon_plus_sm, bg=CARD_COLOR, cursor="hand2")
        lbl_add.pack(side="left", padx=6)
        lbl_add.bind("<Button-1>", self.on_add_click)

        # Events
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Double-Button-1>", self.on_double_click)

    def _load_image(self):
        if self.song.image_path:
            try:
                img = Image.open(self.song.image_path).resize((50, 50), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                self.img_lbl.config(image=self.photo)
            except:
                pass
        else:
            # Placeholder or leave empty
            pass

    def update_fav_icon(self):
        if self.song.is_favorite:
            self.btn_fav.config(image=self.icon_heart_fil)
        else:
            self.btn_fav.config(image=self.icon_heart_emp)

    def toggle_fav(self, event):
        self.song.is_favorite = not self.song.is_favorite
        self.update_fav_icon()
        # Trigger save
        self.controller.update_song(self.song.id, self.song) 
        # Note: Controller update_song saves DB.

    def on_hover(self, event):
        self.config(bg="#2a2a2a")  # Lighter shadow on hover
        self.card.config(bg="#3a3a3a")  # Slightly lighter card
        self.img_lbl.config(bg="#3a3a3a")
        self.btn_fav.config(bg="#3a3a3a")
        self.actions_frame.place(relx=1.0, x=-145, y=20, anchor="ne")
        self.actions_frame.config(bg="#3a3a3a")
        self.actions_frame.lift()
        
    def on_leave(self, event):
        self.config(bg=BG_COLOR)
        self.card.config(bg=CARD_COLOR)
        self.img_lbl.config(bg=CARD_COLOR)
        self.btn_fav.config(bg=CARD_COLOR)
        self.actions_frame.place_forget()

    def on_play_click(self, event):
        if self.on_play:
            self.on_play(self.song.id)
    
    def on_add_click(self, event):
        if self.on_add:
            self.on_add(self.song.id)

    def on_double_click(self, event):
         # Show Detail Modal
         pass
