from __future__ import annotations

import math
import queue
import threading
from datetime import datetime
import tkinter as tk

import customtkinter as ctk

from core.assistant import process_text, process_voice
from core.app_config import AppConfig
from core import file_manager
from core.history import HistoryManager
from core.logger import get_logger

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

logger = get_logger(__name__)


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self._ui_queue = queue.Queue()
        self._is_busy = False
        self._orb_state = "idle"
        self._orb_phase = 0.0
        self.config_manager = AppConfig()
        self.history_manager = HistoryManager()
        self._settings_open = False

        self.title("ART AI")
        self.geometry("1280x760")
        self.minsize(1100, 680)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_panel()
        self._bind_events()

        self.after(80, self._animate_orb)
        self.after(100, self._process_ui_queue)
        self._render_welcome_message()
        self._refresh_history_panel()

    def _build_sidebar(self) -> None:

        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        title = ctk.CTkLabel(
            self.sidebar,
            text="ART AI",
            font=("Segoe UI", 26, "bold"),
        )
        title.grid(row=0, column=0, padx=24, pady=(28, 6), sticky="w")

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Voice file assistant",
            font=("Segoe UI", 13),
            text_color="#8ea0b8",
        )
        subtitle.grid(row=1, column=0, padx=24, pady=(0, 18), sticky="w")

        self.current_directory_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Current: {file_manager.current_directory}",
            wraplength=228,
            justify="left",
        )
        self.current_directory_label.grid(row=2, column=0, padx=24, pady=(0, 18), sticky="w")

        self.sidebar_actions = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_actions.grid(row=3, column=0, padx=18, pady=(0, 10), sticky="ew")

        self.voice_button = ctk.CTkButton(
            self.sidebar_actions,
            text="🎤 Speak",
            height=44,
            command=self.start_voice_command,
        )
        self.voice_button.pack(fill="x", pady=(0, 10))

        self.send_button = ctk.CTkButton(
            self.sidebar_actions,
            text="Send Text",
            height=44,
            command=self.submit_text_command,
        )
        self.send_button.pack(fill="x", pady=(0, 10))

        self.refresh_button = ctk.CTkButton(
            self.sidebar_actions,
            text="Refresh History",
            height=40,
            fg_color="#31415a",
            hover_color="#425472",
            command=self._refresh_history_panel,
        )
        self.refresh_button.pack(fill="x")

        self.settings_button = ctk.CTkButton(
            self.sidebar_actions,
            text="Settings",
            height=40,
            fg_color="#31415a",
            hover_color="#425472",
            command=self.toggle_settings_panel,
        )
        self.settings_button.pack(fill="x", pady=(10, 0))

        history_title = ctk.CTkLabel(
            self.sidebar,
            text="Recent Commands",
            font=("Segoe UI", 16, "bold"),
        )
        history_title.grid(row=4, column=0, padx=24, pady=(12, 8), sticky="nw")

        self.history_panel = ctk.CTkScrollableFrame(self.sidebar, width=240, height=300)
        self.history_panel.grid(row=5, column=0, padx=18, pady=(0, 20), sticky="nsew")

        self.settings_panel = ctk.CTkFrame(self.sidebar)
        self.settings_panel.grid(row=6, column=0, padx=18, pady=(0, 18), sticky="nsew")
        self.settings_panel.grid_remove()

        settings_title = ctk.CTkLabel(
            self.settings_panel,
            text="Settings",
            font=("Segoe UI", 16, "bold"),
        )
        settings_title.pack(anchor="w", padx=12, pady=(12, 6))

        self.theme_option = ctk.CTkOptionMenu(
            self.settings_panel,
            values=["dark", "light"],
            command=self._on_theme_change,
        )
        self.theme_option.pack(fill="x", padx=12, pady=6)

        self.speed_entry = ctk.CTkEntry(self.settings_panel, placeholder_text="Speech speed")
        self.speed_entry.pack(fill="x", padx=12, pady=6)

        self.microphone_entry = ctk.CTkEntry(self.settings_panel, placeholder_text="Microphone index")
        self.microphone_entry.pack(fill="x", padx=12, pady=6)

        self.search_roots_entry = ctk.CTkEntry(
            self.settings_panel,
            placeholder_text="Search roots separated by ;",
        )
        self.search_roots_entry.pack(fill="x", padx=12, pady=6)

        self.save_settings_button = ctk.CTkButton(
            self.settings_panel,
            text="Save Settings",
            command=self.save_settings,
        )
        self.save_settings_button.pack(fill="x", padx=12, pady=(8, 12))

    def _build_main_panel(self) -> None:

        self.main = ctk.CTkFrame(self, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self.main, fg_color="transparent")
        header.grid(row=0, column=0, padx=24, pady=(20, 8), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        heading = ctk.CTkLabel(
            header,
            text="ART AI Assistant",
            font=("Segoe UI", 30, "bold"),
        )
        heading.grid(row=0, column=0, sticky="w")

        self.status = ctk.CTkLabel(
            header,
            text="Status: Ready",
            font=("Segoe UI", 14),
            text_color="#8ea0b8",
        )
        self.status.grid(row=1, column=0, sticky="w", pady=(2, 0))

        self.orb_host = ctk.CTkFrame(self.main, height=220)
        self.orb_host.grid(row=1, column=0, padx=24, pady=(8, 6), sticky="ew")
        self.orb_host.grid_columnconfigure(0, weight=1)

        self.orb_canvas = tk.Canvas(
            self.orb_host,
            width=240,
            height=180,
            highlightthickness=0,
            bg="#111827",
        )
        self.orb_canvas.pack(expand=True, pady=14)

        self.chat_area = ctk.CTkScrollableFrame(self.main)
        self.chat_area.grid(row=2, column=0, padx=24, pady=(6, 12), sticky="nsew")

        self.input_panel = ctk.CTkFrame(self.main, fg_color="transparent")
        self.input_panel.grid(row=3, column=0, padx=24, pady=(0, 12), sticky="ew")
        self.input_panel.grid_columnconfigure(0, weight=1)

        self.command_entry = ctk.CTkEntry(
            self.input_panel,
            placeholder_text="Type a command like 'search downloads invoice' or 'open chrome'",
            height=44,
        )
        self.command_entry.grid(row=0, column=0, padx=(0, 12), sticky="ew")

        self.entry_send_button = ctk.CTkButton(
            self.input_panel,
            text="Send",
            width=120,
            height=44,
            command=self.submit_text_command,
        )
        self.entry_send_button.grid(row=0, column=1, padx=(0, 12))

        self.entry_voice_button = ctk.CTkButton(
            self.input_panel,
            text="Voice",
            width=120,
            height=44,
            command=self.start_voice_command,
        )
        self.entry_voice_button.grid(row=0, column=2)

        self.status_bar = ctk.CTkLabel(
            self.main,
            text="Ready",
            anchor="w",
            text_color="#8ea0b8",
        )
        self.status_bar.grid(row=4, column=0, padx=24, pady=(0, 18), sticky="ew")

        self._load_settings_into_ui()

    def _bind_events(self) -> None:

        self.command_entry.bind("<Return>", self._submit_text_event)

    def _render_welcome_message(self) -> None:

        self._add_bubble(
            sender="assistant",
            message="Welcome to ART AI. Use voice or type a command to manage files, search folders, or launch apps.",
        )

    def _refresh_history_panel(self) -> None:

        for child in self.history_panel.winfo_children():
            child.destroy()

        entries = self.history_manager.latest(12)

        if not entries:
            empty_label = ctk.CTkLabel(self.history_panel, text="No history yet.", text_color="#8ea0b8")
            empty_label.pack(anchor="w", padx=8, pady=8)
            return

        for entry in entries:
            item = ctk.CTkFrame(self.history_panel)
            item.pack(fill="x", padx=6, pady=6)

            top_line = f"{entry.timestamp} • {entry.intent}"
            status_color = "#7ddc8a" if entry.success else "#ff8d8d"

            ctk.CTkLabel(item, text=top_line, anchor="w", justify="left").pack(fill="x", padx=10, pady=(8, 2))
            ctk.CTkLabel(
                item,
                text=entry.command,
                anchor="w",
                justify="left",
                wraplength=210,
            ).pack(fill="x", padx=10)
            ctk.CTkLabel(
                item,
                text="Success" if entry.success else "Failed",
                text_color=status_color,
            ).pack(anchor="w", padx=10, pady=(0, 8))

        clear_button = ctk.CTkButton(
            self.history_panel,
            text="Clear History",
            fg_color="#5c2f2f",
            hover_color="#793c3c",
            command=self.clear_history,
        )
        clear_button.pack(fill="x", padx=6, pady=(8, 4))

    def _submit_text_event(self, event) -> str:

        self.submit_text_command()
        return "break"

    def submit_text_command(self) -> None:

        if self._is_busy:
            return

        command = self.command_entry.get().strip()
        if not command:
            return

        self.command_entry.delete(0, "end")
        self._add_bubble("user", command)
        self._set_busy(True, "Thinking...")
        self._set_orb_state("thinking")

        worker = threading.Thread(target=self._process_text_worker, args=(command,), daemon=True)
        worker.start()

    def start_voice_command(self) -> None:

        if self._is_busy:
            return

        self._set_busy(True, "Listening...")
        self._set_orb_state("listening")

        worker = threading.Thread(target=self._process_voice_worker, daemon=True)
        worker.start()

    def _process_text_worker(self, command: str) -> None:

        try:
            result_command, result = process_text(command)
        except Exception as exc:  # pragma: no cover - thread safety fallback
            logger.exception("Text command worker failed")
            result_command, result = command, f"Error: {exc}"

        self._ui_queue.put({"source": "text", "command": result_command, "result": result})

    def _process_voice_worker(self) -> None:

        try:
            result_command, result = process_voice()
        except Exception as exc:  # pragma: no cover - thread safety fallback
            logger.exception("Voice command worker failed")
            result_command, result = "", f"Error: {exc}"

        self._ui_queue.put({"source": "voice", "command": result_command, "result": result})

    def _process_ui_queue(self) -> None:

        while not self._ui_queue.empty():
            payload = self._ui_queue.get()
            self._handle_result(payload["command"], payload["result"])

        self.after(100, self._process_ui_queue)

    def _handle_result(self, command: str, result: str) -> None:

        if command:
            self._add_bubble("assistant", result)

        self._set_busy(False, "Ready")
        self._set_orb_state("speaking" if command else "idle")
        self._refresh_history_panel()
        self.after(350, lambda: self._set_orb_state("idle"))

        if result.startswith("Current Directory:"):
            self.current_directory_label.configure(text=result.replace("Current Directory:", "Current:").strip())

        self._sync_directory_label()

    def _set_busy(self, is_busy: bool, status_text: str) -> None:

        self._is_busy = is_busy
        state = "disabled" if is_busy else "normal"

        for widget in (
            self.voice_button,
            self.send_button,
            self.entry_send_button,
            self.entry_voice_button,
        ):
            widget.configure(state=state)

        self.status.configure(text=f"Status: {status_text}")
        self.status_bar.configure(text=status_text)

    def _set_orb_state(self, state: str) -> None:

        self._orb_state = state
        logger.info("Orb state changed to %s", state)

    def _load_settings_into_ui(self) -> None:

        self.theme_option.set(self.config_manager.get("theme", "dark"))
        self.speed_entry.insert(0, str(self.config_manager.get("speech_speed", 170)))
        self.microphone_entry.insert(0, str(self.config_manager.get("microphone", 0)))
        search_roots = self.config_manager.get("search_roots", [])
        self.search_roots_entry.insert(0, ";".join(search_roots))

    def _on_theme_change(self, theme: str) -> None:

        self.config_manager.set("theme", theme)
        ctk.set_appearance_mode(theme.capitalize())

    def toggle_settings_panel(self) -> None:

        self._settings_open = not self._settings_open
        if self._settings_open:
            self.settings_panel.grid()
        else:
            self.settings_panel.grid_remove()

    def save_settings(self) -> None:

        try:
            speed = int(self.speed_entry.get().strip())
            microphone = int(self.microphone_entry.get().strip())
        except ValueError:
            self.status_bar.configure(text="Invalid numeric settings.")
            return

        search_roots = [item.strip() for item in self.search_roots_entry.get().split(";") if item.strip()]

        self.config_manager.set("speech_speed", speed)
        self.config_manager.set("microphone", microphone)
        self.config_manager.set("search_roots", search_roots)

        self.status_bar.configure(text="Settings saved.")

    def clear_history(self) -> None:

        self.history_manager.clear()
        self._refresh_history_panel()
        self.status_bar.configure(text="History cleared.")

    def _sync_directory_label(self) -> None:

        self.current_directory_label.configure(text=f"Current: {file_manager.current_directory}")

    def _animate_orb(self) -> None:

        self._orb_phase += 0.18
        self.orb_canvas.delete("all")

        palette = {
            "idle": ("#2f80ed", "#5dade2"),
            "listening": ("#8e44ad", "#c39bd3"),
            "thinking": ("#1abc9c", "#76d7c4"),
            "speaking": ("#f39c12", "#f7dc6f"),
            "breathing": ("#3498db", "#85c1e9"),
        }
        primary, secondary = palette.get(self._orb_state, palette["idle"])

        center_x = 120
        center_y = 90
        base_radius = 42
        pulse = 8 + 10 * (0.5 + 0.5 * math.sin(self._orb_phase))

        for ring_index, ring_radius in enumerate((78, 58, 38)):
            outline = secondary if ring_index == 0 else primary
            self.orb_canvas.create_oval(
                center_x - ring_radius - pulse / 2,
                center_y - ring_radius - pulse / 2,
                center_x + ring_radius + pulse / 2,
                center_y + ring_radius + pulse / 2,
                outline=outline,
                width=2,
            )

        self.orb_canvas.create_oval(
            center_x - base_radius - pulse,
            center_y - base_radius - pulse,
            center_x + base_radius + pulse,
            center_y + base_radius + pulse,
            fill=primary,
            outline=secondary,
            width=3,
        )

        self.orb_canvas.create_oval(
            center_x - 16,
            center_y - 16,
            center_x + 16,
            center_y + 16,
            fill="#f4f8ff",
            outline="",
        )

        self.after(70, self._animate_orb)

    def _add_bubble(self, sender: str, message: str) -> None:

        bubble_row = ctk.CTkFrame(self.chat_area, fg_color="transparent")
        bubble_row.pack(fill="x", padx=12, pady=8)

        is_user = sender == "user"
        bubble_color = "#2e86ff" if is_user else "#232c3d"
        text_color = "#ffffff"
        alignment = "e" if is_user else "w"

        bubble = ctk.CTkFrame(bubble_row, fg_color=bubble_color, corner_radius=18)
        bubble.pack(anchor=alignment, padx=(80 if is_user else 0, 0 if is_user else 80))

        ctk.CTkLabel(
            bubble,
            text=message,
            wraplength=620,
            justify="left",
            text_color=text_color,
        ).pack(anchor="w", padx=14, pady=(10, 2))

        ctk.CTkLabel(
            bubble,
            text=datetime.now().strftime("%H:%M"),
            text_color="#a8b3c7",
            font=("Segoe UI", 11),
        ).pack(anchor="e", padx=14, pady=(0, 10))

        self.chat_area.after(30, self._scroll_chat_to_bottom)

    def _scroll_chat_to_bottom(self) -> None:

        try:
            self.chat_area._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass