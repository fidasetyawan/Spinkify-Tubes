import tkinter as tk
from tkinter import ttk
from .styles import BG_COLOR, ACCENT_COLOR, ACCENT_SOFT, FG_COLOR

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.parent = parent
        
        # Main container for centering
        main_container = tk.Frame(self, bg=BG_COLOR)
        main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo with shadow effect (simulated with darker pink layer)
        logo_container = tk.Frame(main_container, bg=BG_COLOR)
        logo_container.pack(pady=(0, 8))
        
        # Shadow layer (darker pink for glow effect)
        shadow_label = tk.Label(
            logo_container, 
            text="SPINKIFY", 
            font=("Helvetica", 38, "bold"), 
            bg=BG_COLOR, 
            fg="#8b4566"  # Darker pink for shadow
        )
        shadow_label.place(relx=0.5, rely=0.5, anchor="center", x=2, y=2)
        
        # Main logo text
        tk.Label(
            logo_container, 
            text="SPINKIFY", 
            font=("Helvetica", 38, "bold"), 
            bg=BG_COLOR, 
            fg=ACCENT_COLOR
        ).pack()
        
        # Tagline - More concise
        tk.Label(
            main_container, 
            text="A modern music player built with Python & Tkinter", 
            font=("Helvetica", 10), 
            bg=BG_COLOR, 
            fg="#dcdcdc"
        ).pack(pady=(0, 35))
        
        # Divider line
        divider = tk.Frame(main_container, bg="#333333", height=1, width=300)
        divider.pack(pady=(0, 25))
        
        # Role selection label
        tk.Label(
            main_container, 
            text="Select Role", 
            font=("Helvetica", 13, "bold"), 
            bg=BG_COLOR, 
            fg=FG_COLOR
        ).pack(pady=(0, 20))
        
        # Buttons container
        btn_container = tk.Frame(main_container, bg=BG_COLOR)
        btn_container.pack()
        
        # Admin Button with icon and rounded style
        admin_frame = tk.Frame(btn_container, bg=ACCENT_COLOR, cursor="hand2")
        admin_frame.pack(side="left", padx=15)
        
        admin_inner = tk.Frame(admin_frame, bg=ACCENT_COLOR)
        admin_inner.pack(padx=2, pady=2)
        
        admin_content = tk.Frame(admin_inner, bg=ACCENT_COLOR)
        admin_content.pack(padx=28, pady=12)
        
        tk.Label(admin_content, text="👑", font=("Segoe UI Emoji", 16), bg=ACCENT_COLOR).pack(side="left", padx=(0, 8))
        tk.Label(admin_content, text="Admin", font=("Helvetica", 11, "bold"), bg=ACCENT_COLOR, fg=FG_COLOR).pack(side="left")
        
        # Admin button bindings
        def on_admin_enter(e):
            admin_frame.config(bg=ACCENT_SOFT)
            admin_inner.config(bg=ACCENT_SOFT)
            admin_content.config(bg=ACCENT_SOFT)
            for child in admin_content.winfo_children():
                child.config(bg=ACCENT_SOFT)
        
        def on_admin_leave(e):
            admin_frame.config(bg=ACCENT_COLOR)
            admin_inner.config(bg=ACCENT_COLOR)
            admin_content.config(bg=ACCENT_COLOR)
            for child in admin_content.winfo_children():
                child.config(bg=ACCENT_COLOR)
        
        for widget in [admin_frame, admin_inner, admin_content]:
            widget.bind("<Button-1>", lambda e: parent.show_admin())
            widget.bind("<Enter>", on_admin_enter)
            widget.bind("<Leave>", on_admin_leave)
        
        for child in admin_content.winfo_children():
            child.bind("<Button-1>", lambda e: parent.show_admin())
            child.bind("<Enter>", on_admin_enter)
            child.bind("<Leave>", on_admin_leave)
        
        # User Button with icon and rounded style
        user_frame = tk.Frame(btn_container, bg="#2a2a2a", highlightbackground=ACCENT_COLOR, highlightthickness=2, cursor="hand2")
        user_frame.pack(side="left", padx=15)
        
        user_content = tk.Frame(user_frame, bg="#2a2a2a")
        user_content.pack(padx=28, pady=12)
        
        tk.Label(user_content, text="🎧", font=("Segoe UI Emoji", 16), bg="#2a2a2a").pack(side="left", padx=(0, 8))
        tk.Label(user_content, text="User", font=("Helvetica", 11, "bold"), bg="#2a2a2a", fg=FG_COLOR).pack(side="left")
        
        # User button bindings
        def on_user_enter(e):
            user_frame.config(bg="#3a3a3a", highlightbackground=ACCENT_SOFT)
            user_content.config(bg="#3a3a3a")
            for child in user_content.winfo_children():
                child.config(bg="#3a3a3a")
        
        def on_user_leave(e):
            user_frame.config(bg="#2a2a2a", highlightbackground=ACCENT_COLOR)
            user_content.config(bg="#2a2a2a")
            for child in user_content.winfo_children():
                child.config(bg="#2a2a2a")
        
        for widget in [user_frame, user_content]:
            widget.bind("<Button-1>", lambda e: parent.show_user())
            widget.bind("<Enter>", on_user_enter)
            widget.bind("<Leave>", on_user_leave)
        
        for child in user_content.winfo_children():
            child.bind("<Button-1>", lambda e: parent.show_user())
            child.bind("<Enter>", on_user_enter)
            child.bind("<Leave>", on_user_leave)
