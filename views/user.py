import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from .styles import BG_COLOR, ACCENT_COLOR, ACCENT_SOFT, FG_COLOR, SECONDARY_COLOR, CARD_COLOR, HEADER_FONT, SUBHEADER_FONT, load_icon
from PIL import Image, ImageTk
from .components import ScrollableFrame, SongRow

class UserFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.parent = parent
        self.current_playlist_idx = None
        self.details_images = []
        self.rows = []

        # Top Bar
        top_frame = tk.Frame(self, bg=BG_COLOR)
        top_frame.pack(fill="x", padx=20, pady=20)
        tk.Label(top_frame, text="SPINKIFY", font=HEADER_FONT, bg=BG_COLOR, fg=ACCENT_COLOR).pack(side="left")
        ttk.Button(top_frame, text="Logout", command=parent.show_login).pack(side="right")

        # Main Layout
        main_pane = tk.PanedWindow(self, orient="horizontal", bg=BG_COLOR, sashwidth=4, sashpad=0, showhandle=False, borderwidth=0)
        main_pane.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Sidebar with visual separator
        sidebar_container = tk.Frame(main_pane, bg=BG_COLOR)
        main_pane.add(sidebar_container, width=240)
        
        from .styles import SIDEBAR_BG, MINI_PLAYER_BG, BORDER_COLOR, ACCENT_SOFT
        self.sidebar = tk.Frame(sidebar_container, bg=SIDEBAR_BG)
        self.sidebar.pack(fill="both", expand=True, padx=(0, 1), pady=0)
        
        # Right border separator
        tk.Frame(sidebar_container, bg="#1a1a1a", width=1).pack(side="right", fill="y")
        
        # Library Section Header - Softer pink
        tk.Label(self.sidebar, text="Library", bg=SIDEBAR_BG, fg="#e085b4", font=SUBHEADER_FONT).pack(pady=(20, 12), padx=20, anchor="w")
        
        # Navigation Buttons Container
        nav_container = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        nav_container.pack(fill="x", padx=15, pady=(0, 10))
        
        # All Songs - Text Only, Perfectly Centered
        self.all_songs_frame = tk.Frame(nav_container, bg=ACCENT_COLOR, height=35)
        self.all_songs_frame.pack(fill="x", pady=4)
        self.all_songs_frame.pack_propagate(False)
        
        tk.Label(
            self.all_songs_frame,
            text="All Songs",
            bg=ACCENT_COLOR,
            fg=FG_COLOR,
            font=("Helvetica", 9, "bold")
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        self.all_songs_frame.bind("<Button-1>", lambda e: self.show_library())
        self.all_songs_frame.bind("<Enter>", lambda e: self._on_all_songs_hover(True))
        self.all_songs_frame.bind("<Leave>", lambda e: self._on_all_songs_hover(False))
        
        # Liked Songs - Slimmer outline button
        self.icon_heart_nav = load_icon("heart_filled.png", (16, 16))
        self.liked_frame = tk.Frame(nav_container, bg=SIDEBAR_BG, highlightbackground="#e085b4", highlightthickness=1, height=35)
        self.liked_frame.pack(fill="x", pady=4)
        self.liked_frame.pack_propagate(False)
        
        liked_inner = tk.Frame(self.liked_frame, bg=SIDEBAR_BG)
        liked_inner.pack(expand=True, fill="both", padx=1, pady=1)
        
        tk.Label(liked_inner, image=self.icon_heart_nav, bg=SIDEBAR_BG).pack(side="left", padx=(12, 6))
        tk.Label(liked_inner, text="Liked Songs", bg=SIDEBAR_BG, fg="#e085b4", font=("Helvetica", 9, "bold")).pack(side="left")
        
        self.liked_frame.bind("<Button-1>", lambda e: self.show_liked_songs())
        self.liked_frame.bind("<Enter>", lambda e: liked_inner.config(bg="#2a2a2a"))
        self.liked_frame.bind("<Leave>", lambda e: liked_inner.config(bg=SIDEBAR_BG))
        for child in liked_inner.winfo_children():
            child.bind("<Button-1>", lambda e: self.show_liked_songs())
            child.bind("<Enter>", lambda e: liked_inner.config(bg="#2a2a2a"))
            child.bind("<Leave>", lambda e: liked_inner.config(bg=SIDEBAR_BG))
        
        # Separator line
        tk.Frame(self.sidebar, bg="#1a1a1a", height=1).pack(fill="x", padx=20, pady=(16, 0))
        
        # Playlists Section - Softer header
        tk.Label(self.sidebar, text="Playlists", bg=SIDEBAR_BG, fg="#e085b4", font=SUBHEADER_FONT).pack(pady=(16, 8), padx=20, anchor="w")
        
        # Refined Playlist Listbox
        self.playlist_listbox = tk.Listbox(
            self.sidebar, 
            bg="#1f1f1f",
            fg="#d0d0d0", 
            selectbackground="#4d2a3a",
            selectforeground=FG_COLOR,
            borderwidth=0,
            highlightthickness=0,
            font=("Helvetica", 9), 
            activestyle="none",
            relief="flat"
        )
        self.playlist_listbox.pack(fill="both", expand=True, padx=25, pady=5)
        self.playlist_listbox.bind("<<ListboxSelect>>", self.on_playlist_select)
        
        # New Playlist Button - Compact and centered
        self.icon_plus = load_icon("plus.png", (14, 14))
        new_playlist_container = tk.Frame(self.sidebar, bg=SIDEBAR_BG)
        new_playlist_container.pack(fill="x", padx=25, pady=18)
        
        btn_inner = tk.Frame(new_playlist_container, bg="#2a2a2a", cursor="hand2")
        btn_inner.pack()
        
        tk.Label(btn_inner, image=self.icon_plus, bg="#2a2a2a").pack(side="left", padx=(12, 5), pady=6)
        tk.Label(btn_inner, text="New Playlist", bg="#2a2a2a", fg="#d0d0d0", font=("Helvetica", 8, "bold")).pack(side="left", padx=(0, 12), pady=6)
        
        btn_inner.bind("<Button-1>", lambda e: self.create_playlist())
        btn_inner.bind("<Enter>", lambda e: btn_inner.config(bg="#3a3a3a"))
        btn_inner.bind("<Leave>", lambda e: btn_inner.config(bg="#2a2a2a"))
        for child in btn_inner.winfo_children():
            child.bind("<Button-1>", lambda e: self.create_playlist())
            child.bind("<Enter>", lambda e: btn_inner.config(bg="#3a3a3a"))
            child.bind("<Leave>", lambda e: btn_inner.config(bg="#2a2a2a"))

        # Content
        content_container = tk.Frame(main_pane, bg=BG_COLOR)
        main_pane.add(content_container)
        
        self.content = tk.Frame(content_container, bg=BG_COLOR)
        self.content.pack(fill="both", expand=True)
        
        # Enhanced Header with subtitle
        header_frame = tk.Frame(self.content, bg=BG_COLOR)
        header_frame.pack(fill="x", padx=28, pady=(20, 8))
        
        tk.Label(header_frame, text="Your Music", font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(anchor="w")
        tk.Label(header_frame, text="Browse all songs in your library", font=("Helvetica", 9), bg=BG_COLOR, fg="#999999").pack(anchor="w", pady=(2, 0))

        # Enhanced Search Bar with rounded corners and shadow
        search_container = tk.Frame(self.content, bg=BG_COLOR)
        search_container.pack(fill="x", pady=(12, 16), padx=28)
        
        # Shadow effect (simulated with darker frame)
        search_shadow = tk.Frame(search_container, bg="#1a1a1a", height=46)
        search_shadow.pack(fill="x")
        search_shadow.pack_propagate(False)
        
        # Main search frame (rounded appearance)
        search_bg = tk.Frame(search_shadow, bg="#2a2a2a", height=44)
        search_bg.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.995)
        search_bg.pack_propagate(False)
        
        search_inner = tk.Frame(search_bg, bg="#2a2a2a")
        search_inner.pack(fill="both", expand=True, padx=16, pady=10)
        
        # Search icon
        self.icon_search = load_icon("search.png", (16, 16))
        tk.Label(search_inner, image=self.icon_search, bg="#2a2a2a").pack(side="left", padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_inner, 
            textvariable=self.search_var, 
            bg="#2a2a2a", 
            fg=FG_COLOR,
            insertbackground="#e085b4",
            bd=0, 
            font=("Helvetica", 10),
            relief="flat"
        )
        self.search_entry.pack(side="left", fill="both", expand=True)
        
        # Softer placeholder
        self.search_entry.insert(0, "Search by title or artist...")
        self.search_entry.config(fg="#777777")
        
        def on_focus_in(e):
            if self.search_entry.get() == "Search by title or artist...":
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg=FG_COLOR)
            search_bg.config(bg="#323232")
        
        def on_focus_out(e):
            if not self.search_entry.get():
                self.search_entry.insert(0, "Search by title or artist...")
                self.search_entry.config(fg="#777777")
            search_bg.config(bg="#2a2a2a")
        
        self.search_entry.bind("<FocusIn>", on_focus_in)
        self.search_entry.bind("<FocusOut>", on_focus_out)
        self.search_entry.bind("<Return>", lambda e: self.search_song())

        # Scrollable Song List with better spacing
        self.scroll_list = ScrollableFrame(self.content, bg=BG_COLOR)
        self.scroll_list.pack(fill="both", expand=True, padx=28, pady=(8, 12))

        # Mini Player (Bottom) - Modern Design
        self.mini_player = tk.Frame(self, bg=MINI_PLAYER_BG, height=80)
        self.mini_player.pack(fill="x", side="bottom")
        self.mini_player.pack_propagate(False)
        
        # Top border
        tk.Frame(self.mini_player, bg=BORDER_COLOR, height=1).pack(fill="x")

        # Mini Player Content
        mini_content = tk.Frame(self.mini_player, bg=MINI_PLAYER_BG)
        mini_content.pack(fill="both", expand=True, padx=25, pady=12)
        
        # Left: Cover + Info (Fixed width)
        left_section = tk.Frame(mini_content, bg=MINI_PLAYER_BG, width=240)
        left_section.pack(side="left", fill="y")
        left_section.pack_propagate(False)
        
        self.mini_img_lbl = tk.Label(left_section, bg=MINI_PLAYER_BG, cursor="hand2")
        self.mini_img_lbl.pack(side="left", padx=(0, 12))
        self.mini_img_lbl.bind("<Button-1>", lambda e: self.parent.show_now_playing())
        
        info_box = tk.Frame(left_section, bg=MINI_PLAYER_BG)
        info_box.pack(side="left", fill="y")
        
        self.lbl_mini_title = tk.Label(info_box, text="Select a song to begin", font=("Helvetica", 10, "bold"), bg=MINI_PLAYER_BG, fg=FG_COLOR, anchor="w")
        self.lbl_mini_title.pack(fill="x", anchor="w")
        self.lbl_mini_artist = tk.Label(info_box, text="♪ Ready to play", font=("Helvetica", 9), bg=MINI_PLAYER_BG, fg="#888888", anchor="w")
        self.lbl_mini_artist.pack(fill="x", anchor="w")
        
        # Center: Controls (Centered in remaining space)
        center_section = tk.Frame(mini_content, bg=MINI_PLAYER_BG)
        center_section.pack(side="left", expand=True, fill="both")
        
        ctrl_box = tk.Frame(center_section, bg=MINI_PLAYER_BG)
        ctrl_box.place(relx=0.5, rely=0.5, anchor="center")
        
        # Load icons - larger play button
        self.icon_prev = load_icon("prev.png", (26, 26))
        self.icon_play = load_icon("play.png", (38, 38))
        self.icon_pause = load_icon("pause.png", (38, 38))
        self.icon_next = load_icon("next.png", (26, 26))
        
        lbl_prev = tk.Label(ctrl_box, image=self.icon_prev, bg=MINI_PLAYER_BG, cursor="hand2")
        lbl_prev.pack(side="left", padx=14)
        lbl_prev.bind("<Button-1>", lambda e: self.prev_song())
        lbl_prev.bind("<Enter>", lambda e: lbl_prev.config(bg="#333333"))
        lbl_prev.bind("<Leave>", lambda e: lbl_prev.config(bg=MINI_PLAYER_BG))
        
        self.btn_mini_play = tk.Label(ctrl_box, image=self.icon_play, bg=MINI_PLAYER_BG, cursor="hand2")
        self.btn_mini_play.pack(side="left", padx=14)
        self.btn_mini_play.bind("<Button-1>", lambda e: self.toggle_play())
        self.btn_mini_play.bind("<Enter>", lambda e: self.btn_mini_play.config(bg="#333333"))
        self.btn_mini_play.bind("<Leave>", lambda e: self.btn_mini_play.config(bg=MINI_PLAYER_BG))
        
        lbl_next = tk.Label(ctrl_box, image=self.icon_next, bg=MINI_PLAYER_BG, cursor="hand2")
        lbl_next.pack(side="left", padx=14)
        lbl_next.bind("<Button-1>", lambda e: self.next_song())
        lbl_next.bind("<Enter>", lambda e: lbl_next.config(bg="#333333"))
        lbl_next.bind("<Leave>", lambda e: lbl_next.config(bg=MINI_PLAYER_BG))

        self.refresh_playlists()
        self.show_library()

    def refresh_playlists(self):
        self.playlist_listbox.delete(0, tk.END)
        playlists = self.controller.get_playlists()
        for p in playlists:
            self.playlist_listbox.insert(tk.END, p.name)

    def _on_all_songs_hover(self, is_hovering):
        """Helper method for All Songs button hover effect"""
        color = ACCENT_SOFT if is_hovering else ACCENT_COLOR
        self.all_songs_frame.config(bg=color)
        for child in self.all_songs_frame.winfo_children():
            child.config(bg=color)
            for grandchild in child.winfo_children():
                grandchild.config(bg=color)

    def show_library(self):
        self.current_playlist_idx = None
        self.refresh_song_list(self.controller.get_all_songs())

    def show_liked_songs(self):
        self.current_playlist_idx = None
        liked_songs = self.controller.get_liked_songs()
        self.refresh_song_list(liked_songs)

    def on_playlist_select(self, event):
        selection = self.playlist_listbox.curselection()
        if selection:
            idx = selection[0]
            self.current_playlist_idx = idx
            playlists = self.controller.get_playlists()
            songs = playlists[idx].get_songs()
            self.refresh_song_list(songs)

    def refresh_song_list(self, songs):
        # Clear existing rows
        for widget in self.scroll_list.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.rows = []
        if songs:
            for s in songs:
                # Pass explicit callbacks
                row = SongRow(
                    self.scroll_list.scrollable_frame, 
                    s, 
                    self.controller, 
                    on_play=self.play_specific_song, 
                    on_add=self.prompt_add_to_playlist,
                    width_hint=550
                )
                row.pack(fill="x", pady=3, padx=5)
                # Bind double-click here too for details
                row.bind("<Double-Button-1>", lambda e, song=s: self.show_song_details(song))
                self.rows.append(row)

    def create_playlist(self):
        name = simpledialog.askstring("New Playlist", "Enter playlist name:")
        if name:
            self.controller.create_playlist(name)
            self.refresh_playlists()

    def search_song(self):
        key = self.search_var.get()
        if key:
            node = self.controller.search_song(key)
            if node:
                self.refresh_song_list([node.data])
            else:
                messagebox.showinfo("Search", "No song found.")
        else:
            self.show_library()

    # Callbacks
    def play_specific_song(self, song_id):
        # Play directly
        success, msg = self.controller.play_song_id(song_id)
        
        # Always update UI because even if file is missing, player might be in 'demo mode' (is_playing=True)
        self.update_mini_player()
        
        if not success and "demo mode" not in msg.lower():
            # Only warn if it's a real error, not just demo mode fallback
            messagebox.showwarning("Error", msg)

    def prompt_add_to_playlist(self, song_id):
        playlists = self.controller.get_playlists()
        if not playlists:
            messagebox.showinfo("Info", "No playlists created.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Select Playlist")
        dialog.geometry("300x400")
        dialog.configure(bg=BG_COLOR)
        tk.Label(dialog, text="Add to Playlist:", bg=BG_COLOR, fg=ACCENT_COLOR, font=HEADER_FONT).pack(pady=10)
        lb = tk.Listbox(dialog, bg=SECONDARY_COLOR, fg=FG_COLOR, selectbackground=ACCENT_COLOR, borderwidth=0, font=SUBHEADER_FONT)
        lb.pack(fill="both", expand=True, padx=20, pady=10)
        for p in playlists:
            lb.insert(tk.END, p.name)
            
        def confirm():
            selection = lb.curselection()
            if selection:
                idx = selection[0]
                success, msg = self.controller.add_to_playlist(idx, song_id)
                messagebox.showinfo("Result", msg)
                dialog.destroy()
        
        ttk.Button(dialog, text="Add", command=confirm).pack(pady=20)

    def toggle_play(self):
        if self.controller.stop_music():
             self.update_mini_player()
        else:
            if not self.controller.player.is_playing and self.controller.player.current_song:
                 # Controller doesn't have resume?
                 # Re-play current song
                 self.controller.player.play(self.controller.player.current_song)
                 self.update_mini_player()

    def next_song(self):
        node, msg = self.controller.next_song()
        self.update_mini_player()

    def prev_song(self):
        node, msg = self.controller.prev_song()
        self.update_mini_player()

    def update_mini_player(self):
        state = self.controller.get_player_state()
        if state['current_song']:
            s = state['current_song'].data
            self.lbl_mini_title.config(text=s.title)
            self.lbl_mini_artist.config(text=s.artist)
            
            if state['is_playing']:
                self.btn_mini_play.config(image=self.icon_pause)
            else:
                self.btn_mini_play.config(image=self.icon_play)
            
            # Load Art
            if s.image_path:
                try:
                    img = Image.open(s.image_path).resize((50, 50), Image.Resampling.LANCZOS)
                    self.mini_photo = ImageTk.PhotoImage(img)
                    self.mini_img_lbl.config(image=self.mini_photo)
                except:
                    pass
        else:
            self.lbl_mini_title.config(text="Not Playing")
            self.lbl_mini_artist.config(text="")
            self.mini_img_lbl.config(image='')
            
    def show_song_details(self, song):
        d = tk.Toplevel(self)
        d.title("Song Details")
        d.geometry("400x500")
        d.configure(bg=BG_COLOR)
        
        # Cover
        cv = tk.Label(d, bg=BG_COLOR)
        cv.pack(pady=20)
        if song.image_path:
             try:
                img = Image.open(song.image_path).resize((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                cv.config(image=photo)
                cv.image = photo
             except: pass
        
        tk.Label(d, text=song.title, font=HEADER_FONT, bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        tk.Label(d, text=song.artist, font=("Helvetica", 14), bg=BG_COLOR, fg=ACCENT_COLOR).pack()
        tk.Label(d, text=f"{song.album} ({song.year})", font=("Helvetica", 12), bg=BG_COLOR, fg=FG_COLOR).pack(pady=5)
        tk.Label(d, text=f"Genre: {song.genre}", font=("Helvetica", 12), bg=BG_COLOR, fg=FG_COLOR).pack()
        
        # Favorite Toggle not implemented in modal yet, but in row yes.
        ttk.Button(d, text="Close", command=d.destroy).pack(pady=30)
