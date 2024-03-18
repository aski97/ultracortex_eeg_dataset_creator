import tkinter as tk
from tkinter import simpledialog

from AppState import AppState
from DataSystem import DataSystem
from tkinter import messagebox


class SettingsDialog(simpledialog.Dialog):

    def __init__(self, parent):
        self.number_records_label = None
        self.number_records_entry = None
        self.focus_duration_label = None
        self.focus_duration_scale = None
        self.recording_duration_scale = None
        self.recording_duration_label = None
        self.iteration_duration_label = None
        self.app_state = AppState()
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
        self.focus_duration_label = tk.Label(master, text="Focus duration (s)")
        self.focus_duration_scale = tk.Scale(master, from_=1, to=60, orient="horizontal")
        self.recording_duration_label = tk.Label(master, text="Recording duration (s)")
        self.recording_duration_scale = tk.Scale(master, from_=1, to=60, orient="horizontal")
        # TODO: UPDATE THE VALUE RUNTIME
        self.iteration_duration_label = tk.Label(master, text=f"Iteration duration: {self.app_state.iteration_duration}")

        self.number_records_label.grid(row=0)
        self.number_records_entry.grid(row=1, column=0)
        self.focus_duration_label.grid(row=2, pady=2)
        self.focus_duration_scale.grid(row=3, column=0, pady=1)
        self.recording_duration_label.grid(row=4, pady=2)
        self.recording_duration_scale.grid(row=5, column=0, pady=1)
        self.iteration_duration_label.grid(row=6, pady=5)

        # Set values
        self.number_records_entry.insert(0, self.app_state.number_records)
        self.focus_duration_scale.set(self.app_state.focus_duration)
        self.recording_duration_scale.set(self.app_state.recording_duration)

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
        focus_duration = self.focus_duration_scale.get()
        recording_duration = self.recording_duration_scale.get()
        iteration_duration = focus_duration + recording_duration

        # Save on file
        DataSystem().save_settings_data(number_records, focus_duration, recording_duration)

        # update local state
        self.app_state.number_records = number_records
        self.app_state.focus_duration = focus_duration
        self.app_state.recording_duration = recording_duration
        self.app_state.iteration_duration = iteration_duration
