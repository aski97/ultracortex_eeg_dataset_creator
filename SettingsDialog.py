import tkinter as tk
from tkinter import simpledialog

from AppState import AppState
from DataSystem import DataSystem
from tkinter import messagebox


class SettingsDialog(simpledialog.Dialog):

    def __init__(self, parent):
        self.app_state = AppState()

        self.number_records_label = None
        self.number_records_entry = None
        self.initial_duration_label = None
        self.initial_duration_scale = None
        self.focus_duration_label = None
        self.focus_duration_scale = None
        self.recording_duration_scale = None
        self.recording_duration_label = None
        self.break_duration_label = None
        self.break_duration_scale = None
        self.stream_name_label = None
        self.stream_name_entry = None
        self.sampling_rate_label = None
        self.sampling_rate_entry = None

        self.initial_duration_var = tk.DoubleVar(value=self.app_state.initial_duration)
        self.focus_duration_var = tk.DoubleVar(value=self.app_state.focus_duration)
        self.recording_duration_var = tk.DoubleVar(value=self.app_state.recording_duration)
        self.break_duration_var = tk.DoubleVar(value=self.app_state.break_duration)

        super().__init__(parent, "Settings")

    def buttonbox(self):
        box = tk.Frame(self)

        w = tk.Button(box, text="Save", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def body(self, master):
        self.number_records_label = tk.Label(master, text="Number of records:")
        self.number_records_entry = tk.Entry(master)
        self.initial_duration_label = tk.Label(master, text="PHASE 1: Initial (s)")
        self.initial_duration_scale = tk.Scale(master, from_=1, to=10, resolution=0.25, digits=4, variable=self.initial_duration_var, orient="horizontal")
        self.focus_duration_label = tk.Label(master, text="PHASE 2: Focus (s)")
        self.focus_duration_scale = tk.Scale(master, from_=1, to=10, resolution=0.25, digits=4, variable=self.focus_duration_var, orient="horizontal")
        self.recording_duration_label = tk.Label(master, text="PHASE 3: Recording (s)")
        self.recording_duration_scale = tk.Scale(master, from_=1, to=10, resolution=0.25, digits=4, variable=self.recording_duration_var, orient="horizontal")
        self.break_duration_label = tk.Label(master, text="PHASE 4: Break (s)")
        self.break_duration_scale = tk.Scale(master, from_=1, to=10, resolution=0.25, digits=4, variable=self.break_duration_var,
                                                 orient="horizontal")
        self.sampling_rate_label = tk.Label(master, text="Sampling rate (s)")
        self.sampling_rate_entry = tk.Entry(master)
        self.stream_name_label = tk.Label(master, text="Stream name")
        self.stream_name_entry = tk.Entry(master)

        self.number_records_label.grid(row=0)
        self.number_records_entry.grid(row=1, column=0)
        self.initial_duration_label.grid(row=2, column=0, pady=2)
        self.focus_duration_label.grid(row=2, column=1, pady=2)
        self.initial_duration_scale.grid(row=3, column=0, pady=1)
        self.focus_duration_scale.grid(row=3, column=1, pady=1)
        self.recording_duration_label.grid(row=4, column=0, pady=2)
        self.break_duration_label.grid(row=4, column=1, pady=2)
        self.recording_duration_scale.grid(row=5, column=0, pady=1)
        self.break_duration_scale.grid(row=5, column=1, pady=1)
        self.stream_name_label.grid(row=7, column=0, pady=1)
        self.sampling_rate_label.grid(row=7, column=1, pady=1)
        self.stream_name_entry.grid(row=8, column=0, pady=1)
        self.sampling_rate_entry.grid(row=8, column=1, pady=1)

        # Set values
        self.number_records_entry.insert(0, self.app_state.number_records)
        self.stream_name_entry.insert(0, self.app_state.stream_name)
        self.sampling_rate_entry.insert(0, self.app_state.sampling_rate)

        return self.number_records_entry  # Focus on the first entry

    def validate(self):
        number_records_string = self.number_records_entry.get()

        title = "Error"

        try:
            # Convert to int
            value = int(number_records_string)
            if value < 1:
                messagebox.showerror(title, "The number of records must be greater then 0")
                return False
        except ValueError:
            messagebox.showerror(title, "Invalid characters at the field 'number of records'. Put a positive number")
            return False

        return True

    def apply(self):
        # Get values
        number_records = int(self.number_records_entry.get())
        initial_duration = self.initial_duration_scale.get()
        focus_duration = self.focus_duration_scale.get()
        recording_duration = self.recording_duration_scale.get()
        break_duration = self.break_duration_scale.get()
        iteration_duration = initial_duration + focus_duration + recording_duration + break_duration

        stream_name = self.stream_name_entry.get()

        # Save on file
        DataSystem().save_settings_data(number_records,initial_duration, focus_duration, recording_duration, break_duration, stream_name)

        # update local state
        self.app_state.number_records = number_records
        self.app_state.initial_duration = initial_duration
        self.app_state.focus_duration = focus_duration
        self.app_state.recording_duration = recording_duration
        self.app_state.break_duration = break_duration
        self.app_state.iteration_duration = iteration_duration

        self.app_state.stream_name = stream_name
        self.app_state.sampling_rate = self.sampling_rate_entry.get()
