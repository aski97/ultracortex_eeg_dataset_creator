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
        self.validate_positive_integer_entry_cmd = root.register(self.validate_client_id_input)

        # icons definition
        self.conf_session_icon = tk.PhotoImage(file="assets/img/settings.png")
        self.conf_session_icon = self.conf_session_icon.subsample(18)

        # GUI elements
        self.menubar = Menubar(self)

        self.top_frame = tk.Frame(root)
        self.c_id_label = tk.Label(self.top_frame, text="Client ID:")
        self.client_id_entry = tk.Entry(self.top_frame, validate="key",
                                        validatecommand=(self.validate_positive_integer_entry_cmd, "%P"))
        self.start_session_btn = tk.Button(self.top_frame, text="Start Session", command=self.command_start_session)
        self.timer_label = tk.Label(self.top_frame, text="00:00")
        self.config_session_btn = tk.Button(self.top_frame, image=self.conf_session_icon, compound="center", width=25,
                                            height=25, command=self.command_open_settings)

        self.info_label = tk.Label(self.root, text="Info")


        # Pack elements
        self.top_frame.pack(side="top", fill="x", ipady=5)
        self.c_id_label.pack(side="left", padx=2)
        self.client_id_entry.pack(side="left", padx=3)
        self.start_session_btn.pack(side="left", padx=10)
        self.timer_label.pack(side="left", padx=10)
        self.config_session_btn.pack(side="left", padx=10)

        # label is invisible at the beginning

        # App variables
        self.client_id_entry.insert(0, "0")
        self.timer_running = False
        self.timer_value = 0

        self.time_before_to_start = 5
        self.actual_iteration = 0

    # Commands
    def command_start_session(self):
        # TODO: From Start to Stop/Terminate
        # Disable button
        self.start_session_btn.config(state="disabled")
        # Timer stars
        self.start_timer()
        # Countdown starts
        self.info_label.place(relx=0.5, rely=0.5, anchor="center")  # makes info label visible
        self.countdown(0)  # starts from 0

    def command_open_settings(self):
        SettingsDialog(self.root)

    # Methods

    def countdown(self, time_passed):
        if time_passed <= self.time_before_to_start:
            self.info_label.config(text=f"Starting in {self.time_before_to_start - time_passed} s")
            time_passed += 1
            self.root.after(1000, self.countdown, time_passed)  # Call update_timer every 1000 ms
        else:
            # Session iterations start
            self.next_imagination_movement()

    def next_imagination_movement(self):
        # Check if there are records left
        records = self.data_system.settings.get('records')
        focus_duration = self.data_system.settings.get('waiting_time_before_recording')
        imagination_duration = self.data_system.settings.get('movement_duration')
        if self.actual_iteration < records:
            self.session_iteration(0, focus_duration, imagination_duration)
        else:
            # Session end, no more records to record
            self.end_recording_session()

    def session_iteration(self, time_passed, focus_duration, imagination_duration):
        if time_passed == imagination_duration:
            # end record go to the next
            self.actual_iteration += 1
            self.next_imagination_movement()
        elif time_passed == 0:
            # trigger focus time
            # TODO: MAKE THE DECISION RANDOM
            self.info_label.config(text=f"Left hand")
            self.root.configure(bg="orange")  # Change background
        elif time_passed == (imagination_duration - focus_duration):
            # trigger start recording
            self.root.configure(bg="green")  # Change background
            self.record_movement()

        time_passed += 1
        self.root.after(1000, self.session_iteration, time_passed, focus_duration, imagination_duration)

    def record_movement(self):
        pass

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

    def end_recording_session(self):
        self.timer_running = False
        self.root.configure(bg="white")
        self.info_label.config(text=f"Session terminated, thank you!")

    # Validations
    @staticmethod
    def validate_client_id_input(new_value):
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
