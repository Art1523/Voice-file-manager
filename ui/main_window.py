import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("ART AI")
        self.geometry("1200x700")
        self.minsize(1000, 650)

        # ---------------- Left Sidebar ---------------- #

        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.pack(side="left", fill="y")

        title = ctk.CTkLabel(
            self.sidebar,
            text="🤖 ART AI",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=30)

        buttons = [
            "🏠 Home",
            "💬 Chat",
            "📂 Files",
            "⚙ Settings",
            "📜 History"
        ]

        for text in buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                height=45
            )
            btn.pack(fill="x", padx=20, pady=10)

        # ---------------- Main Area ---------------- #

        self.main = ctk.CTkFrame(self)
        self.main.pack(side="left", fill="both", expand=True)

        heading = ctk.CTkLabel(
            self.main,
            text="ART AI",
            font=("Arial", 34, "bold")
        )
        heading.pack(pady=20)

        self.status = ctk.CTkLabel(
            self.main,
            text="Status : Ready",
            font=("Arial", 18)
        )

        self.status.pack()

        self.orb = ctk.CTkLabel(
            self.main,
            text="🔵",
            font=("Arial", 120)
        )

        self.orb.pack(pady=40)

        self.chat = ctk.CTkTextbox(
            self.main,
            width=700,
            height=220
        )

        self.chat.pack(padx=30, pady=20)

        self.chat.insert("end", "AI : Welcome Atharva!\n\n")

        self.mic = ctk.CTkButton(
            self.main,
            text="🎤 Speak",
            width=220,
            height=55
        )

        self.mic.pack(pady=20)