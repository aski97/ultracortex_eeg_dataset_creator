import threading
import tkinter as tk
import random
from tkinter import messagebox

from AppState import AppState
from DataSystem import DataSystem
from LifecycleStatus import Status, StreamStatus
from Menubar import Menubar
from RecordingThread import RecordingThread
from SettingsDialog import SettingsDialog
from singleton_decorator import singleton


@singleton
class UEDatasetCreator:

    def __init__(self):
        root = tk.Tk()

        root.geometry("600x600")
        root.title("Ultracortex EEG Dataset Creator")
        root.configure(background="black")
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root = root

        # Init Systems
        self.data_system = DataSystem()
        self.state = AppState()

        # validations commands
        self.validate_positive_integer_entry_cmd = root.register(self.validate_client_id_input)

        # TK Variables
        self.client_id_var = tk.StringVar(value="0")
        self.client_id_var.trace('w', self.client_id_changed)
        self.session_name_var = tk.StringVar(value="Session 1")
        self.session_name_var.trace('w', self.session_name_changed)

        # icons definition
        self.conf_session_icon = tk.PhotoImage(file="assets/img/settings.png")
        self.conf_session_icon = self.conf_session_icon.subsample(18)

        # GUI elements
        self.menubar = Menubar(self)

        self.top_frame = tk.Frame(root)
        self.c_id_label = tk.Label(self.top_frame, text="Client ID:")
        self.client_id_entry = tk.Entry(self.top_frame, textvariable=self.client_id_var, validate="key",
                                        validatecommand=(self.validate_positive_integer_entry_cmd, "%P"))
        self.session_name_label = tk.Label(self.top_frame, text="Session name:")
        self.session_name_entry = tk.Entry(self.top_frame, textvariable=self.session_name_var)
        self.start_session_btn = tk.Button(self.top_frame, text="Start Session", command=self.command_start_session)
        self.timer_label = tk.Label(self.top_frame, text="00:00")
        self.config_session_btn = tk.Button(self.top_frame, image=self.conf_session_icon, compound="center", width=25,
                                            height=25, command=self.command_open_settings)

        self.cross_label = tk.Label(self.root, text="+", font=("Helvetica", 48), fg="white", bg="black")
        self.info_label = tk.Label(self.root, text="+", font=("Helvetica", 48), fg="white", bg="black")
        self.recorded_movements_label = tk.Label(self.root, text="Records: 0/0")

        # Pack elements
        self.top_frame.pack(side="top", fill="x", ipady=5)
        self.c_id_label.pack(side="left", padx=2)
        self.client_id_entry.pack(side="left", padx=3)
        self.session_name_label.pack(side="left", padx=2)
        self.session_name_entry.pack(side="left", padx=3)
        self.start_session_btn.pack(side="left", padx=10)
        self.timer_label.pack(side="left", padx=10)
        self.config_session_btn.pack(side="left", padx=10)
        self.cross_label.place(relx=0.5, rely=0.5, anchor="center")  # makes info label visible

        # App variables
        number_records, initial_duration, focus_duration, recording_duration, break_duration, iteration_duration, stream_name = self.data_system.load_settings_data()
        self.recording_thread = None
        self.state.app_status = Status.IDLE
        self.state.iteration_status = Status.IDLE
        self.state.stream_status = StreamStatus.IDLE
        self.state.stream_name = stream_name
        self.state.number_records = number_records
        self.state.initial_duration = 2  # PHASE 1 DURATION
        self.state.focus_duration = focus_duration  # PHASE 2 DURATION
        self.state.recording_duration = recording_duration  # PHASE 3 DURATION
        self.state.break_duration = 2   # PHASE 4 DURATION
        self.state.iteration_duration = iteration_duration
        self.state.client_id = 0
        self.state.session_name = self.session_name_var.get()

        self.state.actual_iteration = 0
        self.state.session_running_time = 0
        self.state.actual_selected_hand = 0  # 0 = Left hand, 1 = Right hand, 2 = None
        self.state.sampling_rate = 0.01  # 250Hz

    # Commands
    def on_closing(self):
        self.state.app_status = Status.IDLE
        self.state.iteration_status = Status.IDLE
        self.root.destroy()

    def command_start_session(self):
        # TODO: Change Start Button to Stop/Terminate Button
        # Variables changes
        self.state.actual_iteration = 0
        self.state.session_running_time = 0
        self.state.app_status = Status.SESSION_STARTED
        self.state.iteration_status = Status.IDLE
        # UI changes
        self.start_session_btn.config(state="disabled")  # Disable button
        self.config_session_btn.config(state="disabled")  # Disable button
        self.client_id_entry.config(state="disabled")  # Disable entry
        self.session_name_entry.config(state="disabled")  # Disable entry
        # Start recording threads
        self.recording_thread = RecordingThread()
        self.recording_thread.start()
        # Continue if a stream is found
        # with self.state.on_stream_status_change:
        #     while True:
        #         self.state.on_stream_status_change.wait()
        #         if self.state.stream_status == StreamStatus.NOT_FOUND:
        #             messagebox.showerror("Stream not found", "No EEG Stream found, please make sure lsl streaming is enabled on OpenBCI GUI.")
        #             self.reset_session()
        #             return
        #         elif self.state.stream_status == StreamStatus.SEARCHING:
        #             print("looking for an EEG stream...")
        #         elif self.state.stream_status == StreamStatus.FOUND:
        #             print("Stream found")
        #             break

        self.info_label.place(relx=0.5, rely=0.2, anchor="center")  # makes info label visible
        self.start_timer()  # Timer stars
        self.recorded_movements_label.config(text=f"Records: {self.state.actual_iteration}/{self.state.number_records}")
        self.recorded_movements_label.pack(side="top", pady=5)

        # Start iterations
        self.next_session_iteration()

    def command_open_settings(self):
        SettingsDialog(self.root)

    # Methods

    def reset_session(self):
        self.state.app_status = Status.IDLE
        self.state.iteration_status = Status.IDLE
        # refresh UI
        self.reset_ui_session()

    def reset_ui_session(self):
        self.start_session_btn.config(state="active")
        self.config_session_btn.config(state="active")
        self.client_id_entry.config(state="normal")
        self.session_name_entry.config(state="normal")

    def next_session_iteration(self):
        # Check if there are records left
        self.recorded_movements_label.config(text=f"Records: {self.state.actual_iteration}/{self.state.number_records}")
        if self.state.actual_iteration < self.state.number_records:
            self.session_iteration(0)
        else:
            # Session end, no more records to record
            self.end_recording_session()

    def session_iteration(self, time_passed):
        if time_passed == (self.state.initial_duration + self.state.iteration_duration):
            # BREAK TIME, pause before start the next iteration (PHASE 4)
            # TODO: questo è il fine del break e non la fase 4, da inserire il trigger della fase di break
            self.state.iteration_status = Status.WAITING_PHASE
            self.state.actual_iteration += 1
            # TODO: change background colour
            self.cross_label.config(bg="black")
            self.next_session_iteration()
        elif time_passed == 0:
            print("WAITING PHASE (1)")
            # WAITING TIME, fixation cross (PHASE 1)
            # TODO: suono acustico per tot secondi (0.4s)
            self.state.iteration_status = Status.WAITING_PHASE
            self.root.configure(bg="black")
            self.cross_label.place(relx=0.5, rely=0.5, anchor="center")  # makes info label visible
            # self.info_label.config(text=f"Starting in {self.state.waiting_time - time_passed} s")
        elif time_passed < self.state.initial_duration:
            pass
            # self.info_label.config(text=f"Starting in {self.state.waiting_time - time_passed} s")
        elif time_passed == self.state.initial_duration:
            print("FOCUS PHASE (2)")
            # FOCUS TIME, show the movement to focus on (PHASE 2)
            # TODO: freccia che indica il movimento (sinistra, destra, cerchio)
            # TODO: durata 1.25s
            self.state.iteration_status = Status.FOCUS_PHASE
            self.state.actual_selected_hand = random.choice([0, 1])  # 0 = Left hand, 1 = Right hand, 2 = None
            self.cross_label.config(bg="orange")
            self.info_label.config(text=f"{'Left' if self.state.actual_selected_hand == 0 else 'Right'} hand")
            self.root.configure(bg="orange")  # Change background
        elif time_passed == (self.state.initial_duration + (self.state.focus_duration - 0.75)):
            # starts recording phase (PHASE 3)
            print("Start recording")
            self.state.iteration_status = Status.RECORDING_PHASE
        elif time_passed == (self.state.initial_duration + self.state.focus_duration):
            # end of focus phase, GUI changes
            print("END FOCUS PHASE")
            self.cross_label.config(state="disabled")  # Disable cross
            self.root.configure(bg="green")  # Change background

        time_passed += 1
        self.root.after(1000, self.session_iteration, time_passed)

    def start_timer(self):
        if self.state.app_status == Status.SESSION_STARTED:
            self.update_timer()

    def update_timer(self):
        if self.state.app_status == Status.SESSION_STARTED:
            minutes = self.state.session_running_time // 60
            seconds = self.state.session_running_time % 60
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.state.session_running_time += 1
            self.root.after(1000, self.update_timer)  # Call update_timer every 1000 ms

    def end_recording_session(self):
        # UI Changes
        self.root.configure(bg="black")
        self.info_label.config(text=f"Session terminated, thank you!")
        self.state.app_status = Status.SESSION_ENDED

    def client_id_changed(self, *args):
        value = self.client_id_var.get()
        try:
            int_value = int(value)
            self.state.client_id = int_value
        except ValueError:
            pass

    def session_name_changed(self, *args):
        value = self.session_name_entry.get()
        self.state.session_name = value

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
