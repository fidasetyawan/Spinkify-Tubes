import tkinter as tk
from tkinter import ttk, messagebox
from .styles import BG_COLOR, ACCENT_COLOR, FG_COLOR, CARD_COLOR, SECONDARY_COLOR, BORDER_COLOR, load_icon
from PIL import Image, ImageTk

class NowPlayingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.parent = parent
        
        # Back Button - Modern style
        back_btn = tk.Label(self, text="← Back", bg=BG_COLOR, fg="#999999", font=("Helvetica", 10), cursor="hand2")
        back_btn.place(x=25, y=25)
        back_btn.bind("<Button-1>", lambda e: parent.show_user())
        back_btn.bind("<Enter>", lambda e: back_btn.config(fg=ACCENT_COLOR))
        back_btn.bind("<Leave>", lambda e: back_btn.config(fg="#999999"))
        
        # Main Container - Centered
        main_container = tk.Frame(self, bg=BG_COLOR)
        main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Card with subtle shadow effect (simulated with frames)
        shadow_frame = tk.Frame(main_container, bg="#1a1a1a")
        shadow_frame.pack(padx=3, pady=3)
        
        content_card = tk.Frame(shadow_frame, bg=CARD_COLOR)
        content_card.pack(padx=40, pady=40)
        
        # Album Art - Larger
        self.img_label = tk.Label(content_card, bg=CARD_COLOR)
        self.img_label.pack(pady=(0, 25))
        
        # Song Info
        self.lbl_title = tk.Label(
            content_card, 
            text="Not Playing", 
            font=("Helvetica", 22, "bold"), 
            bg=CARD_COLOR, 
            fg=FG_COLOR
        )
        self.lbl_title.pack(pady=(0, 8))
        
        # Artist + Favorite
        artist_container = tk.Frame(content_card, bg=CARD_COLOR)
        artist_container.pack(pady=(0, 30))
        
        self.lbl_artist = tk.Label(
            artist_container, 
            text="Artist", 
            font=("Helvetica", 14), 
            bg=CARD_COLOR, 
            fg="#b8b8b8"
        )
        self.lbl_artist.pack(side="left", padx=(0, 12))
        
        # Favorite button
        self.icon_heart_emp = load_icon("heart_outline.png", (24, 24))
        self.icon_heart_fil = load_icon("heart_filled.png", (24, 24))
        
        self.btn_fav = tk.Label(artist_container, bg=CARD_COLOR, cursor="hand2")
        self.btn_fav.pack(side="left")
        self.btn_fav.bind("<Button-1>", self.toggle_fav)
        
        # Controls - Modern circular style
        ctrl_container = tk.Frame(content_card, bg=CARD_COLOR)
        ctrl_container.pack(pady=(10, 0))
        
        # Load icons
        self.icon_prev = load_icon("prev.png", (28, 28))
        self.icon_play = load_icon("play.png", (42, 42))
        self.icon_pause = load_icon("pause.png", (42, 42))
        self.icon_next = load_icon("next.png", (28, 28))
        
        # Prev button
        prev_frame = tk.Frame(ctrl_container, bg="#2a2a2a", width=50, height=50)
        prev_frame.pack(side="left", padx=15)
        prev_frame.pack_propagate(False)
        
        lbl_prev = tk.Label(prev_frame, image=self.icon_prev, bg="#2a2a2a", cursor="hand2")
        lbl_prev.place(relx=0.5, rely=0.5, anchor="center")
        lbl_prev.bind("<Button-1>", lambda e: self.prev_song())
        
        def on_prev_enter(e):
            prev_frame.config(bg="#3a3a3a")
            lbl_prev.config(bg="#3a3a3a")
        def on_prev_leave(e):
            prev_frame.config(bg="#2a2a2a")
            lbl_prev.config(bg="#2a2a2a")
        
        prev_frame.bind("<Enter>", on_prev_enter)
        prev_frame.bind("<Leave>", on_prev_leave)
        lbl_prev.bind("<Enter>", on_prev_enter)
        lbl_prev.bind("<Leave>", on_prev_leave)
        
        # Play/Pause button - Dark with pink border (not solid pink)
        play_outer = tk.Frame(ctrl_container, bg=ACCENT_COLOR, width=62, height=62)
        play_outer.pack(side="left", padx=15)
        play_outer.pack_propagate(False)
        
        play_frame = tk.Frame(play_outer, bg="#252525", width=58, height=58)
        play_frame.place(relx=0.5, rely=0.5, anchor="center")
        play_frame.pack_propagate(False)
        
        self.btn_play = tk.Label(play_frame, image=self.icon_play, bg="#252525", cursor="hand2")
        self.btn_play.place(relx=0.5, rely=0.5, anchor="center")
        self.btn_play.bind("<Button-1>", lambda e: self.toggle_play())
        
        def on_play_enter(e):
            play_frame.config(bg="#2a2a2a")
            self.btn_play.config(bg="#2a2a2a")
        def on_play_leave(e):
            play_frame.config(bg="#252525")
            self.btn_play.config(bg="#252525")
        
        play_frame.bind("<Enter>", on_play_enter)
        play_frame.bind("<Leave>", on_play_leave)
        self.btn_play.bind("<Enter>", on_play_enter)
        self.btn_play.bind("<Leave>", on_play_leave)
        
        self.play_frame = play_frame  # Store reference for updates
        
        # Next button
        next_frame = tk.Frame(ctrl_container, bg="#2a2a2a", width=50, height=50)
        next_frame.pack(side="left", padx=15)
        next_frame.pack_propagate(False)
        
        lbl_next = tk.Label(next_frame, image=self.icon_next, bg="#2a2a2a", cursor="hand2")
        lbl_next.place(relx=0.5, rely=0.5, anchor="center")
        lbl_next.bind("<Button-1>", lambda e: self.next_song())
        
        def on_next_enter(e):
            next_frame.config(bg="#3a3a3a")
            lbl_next.config(bg="#3a3a3a")
        def on_next_leave(e):
            next_frame.config(bg="#2a2a2a")
            lbl_next.config(bg="#2a2a2a")
        
        next_frame.bind("<Enter>", on_next_enter)
        next_frame.bind("<Leave>", on_next_leave)
        lbl_next.bind("<Enter>", on_next_enter)
        lbl_next.bind("<Leave>", on_next_leave)
        
        self.update_view()

    def update_view(self):
        state = self.controller.get_player_state()
        if state['current_song']:
            s = state['current_song'].data
            self.lbl_title.config(text=s.title)
            self.lbl_artist.config(text=s.artist)
            
            # Update Fav
            if s.is_favorite:
                self.btn_fav.config(image=self.icon_heart_fil)
            else:
                self.btn_fav.config(image=self.icon_heart_emp)
            
            # Load Image
            if s.image_path:
                try:
                    img = Image.open(s.image_path)
                    img = img.resize((280, 280), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.img_label.config(image=photo)
                    self.img_label.image = photo
                except Exception as e:
                    print(f"Error loading image: {e}")
                    self.img_label.config(image='', text="♪", font=("Helvetica", 80), fg="#404040")
            else:
                self.img_label.config(image='', text="♪", font=("Helvetica", 80), fg="#404040")
            
            if state['is_playing']:
                self.btn_play.config(image=self.icon_pause)
            else:
                self.btn_play.config(image=self.icon_play)
                
        else:
            self.lbl_title.config(text="Not Playing")
            self.lbl_artist.config(text="")
            self.img_label.config(image='', text="♪", font=("Helvetica", 80), fg="#404040")
            self.btn_play.config(image=self.icon_play)
            self.btn_fav.config(image='')

    def toggle_fav(self, event=None):
        state = self.controller.get_player_state()
        if state['current_song']:
            s = state['current_song'].data
            s.is_favorite = not s.is_favorite
            self.controller.update_song(s.id, s)
            self.update_view()

    def toggle_play(self):
        if self.controller.stop_music():
             self.update_view()
        else:
             state = self.controller.get_player_state()
             if state['current_song']:
                 self.controller.player.play(state['current_song'])
                 self.update_view()

    def next_song(self):
        node, msg = self.controller.next_song()
        if node:
            self.update_view()
        else:
            messagebox.showinfo("Info", msg)

    def prev_song(self):
        node, msg = self.controller.prev_song()
        if node:
            self.update_view()
        else:
            messagebox.showinfo("Info", msg)
