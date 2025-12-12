import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from .styles import BG_COLOR, ACCENT_COLOR, FG_COLOR, CARD_COLOR, HEADER_FONT, BODY_FONT

class AdminFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.parent = parent
        
        # Header
        header_frame = tk.Frame(self, bg=BG_COLOR)
        header_frame.pack(fill="x", padx=20, pady=20)
        tk.Label(header_frame, text="Admin Dashboard", font=HEADER_FONT, bg=BG_COLOR, fg=ACCENT_COLOR).pack(side="left")
        ttk.Button(header_frame, text="Logout", command=parent.show_login).pack(side="right")

        # Content
        content_frame = tk.Frame(self, bg=BG_COLOR)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Left: Form Card
        form_card = tk.LabelFrame(content_frame, text="Manage Song", bg=CARD_COLOR, fg=ACCENT_COLOR, font=("Helvetica", 12, "bold"))
        form_card.pack(side="left", fill="y", padx=(0, 10), ipadx=10, ipady=10)
        
        # Helper to create rows
        def add_field(row, label):
            tk.Label(form_card, text=label, bg=CARD_COLOR, fg=FG_COLOR, font=BODY_FONT).grid(row=row, column=0, sticky="e", pady=5, padx=5)
            entry = tk.Entry(form_card, bg=BG_COLOR, fg=FG_COLOR, insertbackground="white")
            entry.grid(row=row, column=1, pady=5, padx=5)
            return entry

        self.entry_id = add_field(0, "ID:")
        self.entry_title = add_field(1, "Title:")
        self.entry_artist = add_field(2, "Artist:")
        self.entry_genre = add_field(3, "Genre:")
        self.entry_album = add_field(4, "Album:")
        self.entry_year = add_field(5, "Year:")
        
        tk.Label(form_card, text="Audio Path:", bg=CARD_COLOR, fg=FG_COLOR, font=BODY_FONT).grid(row=6, column=0, sticky="e", pady=5)
        self.entry_audio = tk.Entry(form_card, bg=BG_COLOR, fg=FG_COLOR, insertbackground="white")
        self.entry_audio.grid(row=6, column=1, pady=5)
        ttk.Button(form_card, text="...", width=3, command=self.browse_audio).grid(row=6, column=2, padx=5)
        
        tk.Label(form_card, text="Image Path:", bg=CARD_COLOR, fg=FG_COLOR, font=BODY_FONT).grid(row=7, column=0, sticky="e", pady=5)
        self.entry_image = tk.Entry(form_card, bg=BG_COLOR, fg=FG_COLOR, insertbackground="white")
        self.entry_image.grid(row=7, column=1, pady=5)
        ttk.Button(form_card, text="...", width=3, command=self.browse_image).grid(row=7, column=2, padx=5)

        btn_box = tk.Frame(form_card, bg=CARD_COLOR)
        btn_box.grid(row=8, column=0, columnspan=3, pady=20)
        ttk.Button(btn_box, text="Add", command=self.add_song).pack(side="left", padx=5)
        ttk.Button(btn_box, text="Update", command=self.update_song).pack(side="left", padx=5)
        ttk.Button(btn_box, text="Delete", command=self.delete_song).pack(side="left", padx=5)
        ttk.Button(btn_box, text="Clear", command=self.clear_form).pack(side="left", padx=5)

        # Right: List Card
        list_frame = tk.Frame(content_frame, bg=CARD_COLOR)
        list_frame.pack(side="right", fill="both", expand=True)

        cols = ("ID", "Title", "Artist", "Genre", "Album", "Year")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.refresh_list()

    def browse_audio(self):
        f = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        if f:
            self.entry_audio.delete(0, tk.END)
            self.entry_audio.insert(0, f)

    def browse_image(self):
        f = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if f:
            self.entry_image.delete(0, tk.END)
            self.entry_image.insert(0, f)

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        songs = self.controller.get_all_songs()
        for s in songs:
            self.tree.insert("", "end", values=(s.id, s.title, s.artist, s.genre, s.album, s.year))

    def clear_form(self):
        self.entry_id.delete(0, tk.END)
        self.entry_title.delete(0, tk.END)
        self.entry_artist.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_album.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_audio.delete(0, tk.END)
        self.entry_image.delete(0, tk.END)

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            id = values[0]
            node = self.controller.get_song(id)
            if node:
                s = node.data
                self.clear_form()
                self.entry_id.insert(0, s.id)
                self.entry_title.insert(0, s.title)
                self.entry_artist.insert(0, s.artist)
                self.entry_genre.insert(0, s.genre)
                self.entry_album.insert(0, s.album)
                self.entry_year.insert(0, s.year)
                self.entry_audio.insert(0, s.audio_path)
                self.entry_image.insert(0, s.image_path)

    def add_song(self):
        """Add song with comprehensive validation"""
        # Get all values
        id_str = self.entry_id.get().strip()
        title = self.entry_title.get().strip()
        artist = self.entry_artist.get().strip()
        genre = self.entry_genre.get().strip()
        album = self.entry_album.get().strip()
        year_str = self.entry_year.get().strip()
        audio_path = self.entry_audio.get().strip()
        image_path = self.entry_image.get().strip()
        
        # Validation 1: Check required fields are not empty
        if not all([id_str, title, artist, genre, album, year_str]):
            messagebox.showerror(
                "Validation Error",
                "Please fill in all required fields:\n• ID\n• Title\n• Artist\n• Genre\n• Album\n• Year\n\n(Audio and Image paths are optional)"
            )
            return
        
        # Validation 2: Check ID and Year are valid integers
        try:
            song_id = int(id_str)
            year = int(year_str)
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "ID and Year must be valid numbers.\n\nPlease check your input."
            )
            return
        
        # Validation 3: Check year is reasonable (optional but good practice)
        if year < 1900 or year > 2100:
            messagebox.showwarning(
                "Warning",
                f"Year {year} seems unusual. Are you sure?"
            )
        
        # Try to add song
        try:
            success, message = self.controller.add_song(
                song_id, title, artist, genre, album, year, audio_path, image_path
            )
            
            if success:
                self.refresh_list()
                self.clear_form()
                messagebox.showinfo("Success", message)
            else:
                # Duplicate or other error
                messagebox.showerror("Duplicate Song", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add song:\n{str(e)}")

    def update_song(self):
        try:
            from models import Song
            s = Song(
                int(self.entry_id.get()), self.entry_title.get(), self.entry_artist.get(),
                self.entry_genre.get(), self.entry_album.get(), int(self.entry_year.get()),
                self.entry_audio.get(), self.entry_image.get()
            )
            if self.controller.update_song(s.id, s):
                self.refresh_list()
                messagebox.showinfo("Success", "Song updated.")
            else:
                messagebox.showerror("Error", "Song ID not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def delete_song(self):
        try:
            id = int(self.entry_id.get())
            if self.controller.delete_song(id):
                self.refresh_list()
                self.clear_form()
                messagebox.showinfo("Success", "Song deleted.")
            else:
                messagebox.showerror("Error", "Song ID not found.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")
