import tkinter as tk
from threading import Thread
import time

from DataSystem import DataSystem
from Menubar import Menubar
from SettingsDialog import SettingsDialog


class UEDatasetCreator:

    def __init__(self, root):
        root.geometry("600x600")
        root.title("Ultracortex EEG Dataset Creator")
        root.configure(background="white")

        self.root = root

        # Init Systems
        self.data_system = DataSystem()

        # validations commands
        validate_client_id_cmd = root.register(self.validate_client_id_input)

        # icons definition
        self.conf_session_icon = tk.PhotoImage(file="assets/img/settings.png")
        self.conf_session_icon = self.conf_session_icon.subsample(18)

        # GUI elements
        self.menubar = Menubar(self)

        self.top_frame = tk.Frame(root)
        self.c_id_label = tk.Label(self.top_frame, text="Client ID:")
        self.client_id_entry = tk.Entry(self.top_frame, validate="key", validatecommand=(validate_client_id_cmd, "%P"))
        self.start_session_btn = tk.Button(self.top_frame, text="Start Session", command=self.command_start_session)
        self.timer_label = tk.Label(self.top_frame, text="00:00")
        self.config_session_btn = tk.Button(self.top_frame, image=self.conf_session_icon, compound="center", width=25, height=25,
                                       command=lambda: print("Hai cliccato!"))

        # Pack elements
        self.top_frame.pack(side="top", fill="x", ipady=5)
        self.c_id_label.pack(side="left", padx=2)
        self.client_id_entry.pack(side="left", padx=3)
        self.start_session_btn.pack(side="left", padx=10)
        self.timer_label.pack(side="left", padx=10)
        self.config_session_btn.pack(side="left", padx=10)

        # App variables
        self.client_id_entry.insert(0, "0")
        self.timer_running = False
        self.timer_value = 0

    # Commands
    def command_start_session(self):
        print("Inizio sessione")
        self.start_timer()

    def command_open_settings(self):
        SettingsDialog(self.root)

    # Methods
    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            minutes = self.timer_value // 60
            seconds = self.timer_value % 60
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.timer_value += 1
            self.root.after(1000, self.update_timer)  # Call update_timer every 1000 ms

    # Validations
    def validate_client_id_input(self, new_value):
        if new_value == "":
            return True  # Permetti l'input vuoto
        try:
            # Controlla se il valore inserito può essere convertito in un intero
            value = int(new_value)
            # Controlla se il valore è un intero positivo
            if value >= 0:
                return True
            else:
                return False
        except ValueError:
            return False


if __name__ == '__main__':
    window = tk.Tk()
    app = UEDatasetCreator(window)
    window.mainloop()
