import threading
import tkinter as tk
from threading import Thread
import random
from enum import Enum

from AppState import AppState
from DataSystem import DataSystem
from Menubar import Menubar
from SettingsDialog import SettingsDialog
from singleton_decorator import singleton


class AppStatus(Enum):
    IDLE = 1
    SESSION_STARTED = 2
    SESSION_ENDED = 3


class RecordingThread(Thread):
    def __init__(self):
        super(RecordingThread, self).__init__()

        self.app_state = AppState()
        # self.client_id = self.app.get_client_id()
        # self.record_time = record_time
        # self.session_name = session_name
        self._stop_event = threading.Event()

    def run(self):
        while self.app_state.status == AppStatus.IDLE:
            continue
        print("è uscito")

    def stop(self):
        self._stop_event.set()


@singleton
class UEDatasetCreator:

    def __init__(self):
        root = tk.Tk()

        root.geometry("600x600")
        root.title("Ultracortex EEG Dataset Creator")
        root.configure(background="white")

        self.root = root

        # Init Systems
        self.data_system = DataSystem()
        self.state = AppState()

        # validations commands
        self.validate_positive_integer_entry_cmd = root.register(self.validate_client_id_input)

        # TK Variables
        self.client_id_var = tk.StringVar(value="0")
        self.client_id_var.trace('w', self.client_id_changed)

        # icons definition
        self.conf_session_icon = tk.PhotoImage(file="assets/img/settings.png")
        self.conf_session_icon = self.conf_session_icon.subsample(18)

        # GUI elements
        self.menubar = Menubar(self)

        self.top_frame = tk.Frame(root)
        self.c_id_label = tk.Label(self.top_frame, text="Client ID:")
        self.client_id_entry = tk.Entry(self.top_frame, textvariable=self.client_id_var, validate="key",
                                        validatecommand=(self.validate_positive_integer_entry_cmd, "%P"))
        self.start_session_btn = tk.Button(self.top_frame, text="Start Session", command=self.command_start_session)
        self.timer_label = tk.Label(self.top_frame, text="00:00")
        self.config_session_btn = tk.Button(self.top_frame, image=self.conf_session_icon, compound="center", width=25,
                                            height=25, command=self.command_open_settings)

        self.info_label = tk.Label(self.root, text="Info")
        self.recorded_movements_label = tk.Label(self.root, text="Records: 0/0")

        # Pack elements
        self.top_frame.pack(side="top", fill="x", ipady=5)
        self.c_id_label.pack(side="left", padx=2)
        self.client_id_entry.pack(side="left", padx=3)
        self.start_session_btn.pack(side="left", padx=10)
        self.timer_label.pack(side="left", padx=10)
        self.config_session_btn.pack(side="left", padx=10)

        # App variables
        number_records, focus_duration, recording_duration, iteration_duration = self.data_system.load_settings_data()

        self.state.status = AppStatus.IDLE
        self.state.number_records = number_records
        self.state.focus_duration = focus_duration
        self.state.recording_duration = recording_duration
        self.state.iteration_duration = iteration_duration
        self.state.client_id = 0
        self.state.session_name = "Session 1"
        self.state.waiting_time = 5  # Time to wait before to start an iteration
        self.state.actual_iteration = 0
        self.state.session_running_time = 0
        self.state.actual_selected_hand = 0  # 0 = Left hand, 1 = Right hand

        self.timer_running = False

    # Commands
    def command_start_session(self):
        # TODO: Change Start Button to Stop/Terminate Button

        # Variables changes
        self.state.actual_iteration = 0
        self.state.session_running_time = 0
        # UI changes
        self.start_session_btn.config(state="disabled")  # Disable button
        self.config_session_btn.config(state="disabled")  # Disable button
        self.client_id_entry.config(state="disabled")  # Disable entry
        # TODO: disable menu items (New Session/Settings)
        self.info_label.place(relx=0.5, rely=0.5, anchor="center")  # makes info label visible
        self.start_timer()  # Timer stars
        self.recorded_movements_label.config(text=f"Records: {self.state.actual_iteration}/{self.state.number_records}")
        self.recorded_movements_label.pack(side="top", pady=5)
        # Start recording threads
        recording_thread = RecordingThread()
        recording_thread.start()
        # Start iterations
        self.next_session_iteration()

    def command_open_settings(self):
        SettingsDialog(self.root)

    # Methods

    def next_session_iteration(self):
        # Check if there are records left
        self.recorded_movements_label.config(text=f"Records: {self.state.actual_iteration}/{self.state.number_records}")
        if self.state.actual_iteration < self.state.number_records:
            self.session_iteration(0)
        else:
            # Session end, no more records to record
            self.end_recording_session()

    def session_iteration(self, time_passed):
        if time_passed == (self.state.waiting_time + self.state.iteration_duration):
            # end of record, go to the next one
            self.state.actual_iteration += 1
            self.next_session_iteration()
        elif time_passed == 0:
            # trigger waiting time
            self.root.configure(bg="white")
            self.info_label.config(text=f"Starting in {self.state.waiting_time - time_passed} s")
        elif time_passed < self.state.waiting_time:
            self.info_label.config(text=f"Starting in {self.state.waiting_time - time_passed} s")
        elif time_passed == self.state.waiting_time:
            # trigger focus time

            self.state.actual_selected_hand = random.choice([0, 1])  # 0 = Left hand, 1 = Right hand
            self.info_label.config(text=f"{'Left' if self.state.actual_selected_hand == 0 else 'Right'} hand")
            self.root.configure(bg="orange")  # Change background
        elif time_passed == (self.state.waiting_time + self.state.focus_duration):
            # trigger start recording
            self.root.configure(bg="green")  # Change background
            self.record_movement()

        time_passed += 1
        self.root.after(1000, self.session_iteration, time_passed)

    def record_movement(self):
        pass
        # recording_thread_ts = RecordingThreadTS(record_time, filename_prefix)

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            minutes = self.state.session_running_time // 60
            seconds = self.state.session_running_time % 60
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.state.session_running_time += 1
            self.root.after(1000, self.update_timer)  # Call update_timer every 1000 ms

    def end_recording_session(self):
        self.state.status = AppStatus.SESSION_ENDED
        # UI Changes
        self.root.configure(bg="white")
        self.info_label.config(text=f"Session terminated, thank you!")
        # Variables changes
        self.timer_running = False

    def client_id_changed(self, *args):
        value = self.client_id_var.get()
        try:
            int_value = int(value)
            self.state.client_id = int_value
        except ValueError:
            pass

    def main_loop(self):
        self.root.mainloop()

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
    app = UEDatasetCreator()
    app.main_loop()
