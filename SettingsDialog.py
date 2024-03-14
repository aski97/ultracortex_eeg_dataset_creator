import tkinter as tk
from tkinter import simpledialog

from DataSystem import DataSystem
from tkinter import messagebox


class SettingsDialog(simpledialog.Dialog):

    def __init__(self, parent):
        self.records_entry = None
        self.movement_duration_scale = None
        self.waiting_time_before_recording_scale = None
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

        tk.Label(master, text="Number of records:").grid(row=0)

        settings = DataSystem().settings

        self.records_entry = tk.Entry(master)
        self.records_entry.grid(row=1, column=0)

        tk.Label(master, text="Movement duration (s)").grid(row=2, pady=2)

        self.movement_duration_scale = tk.Scale(master, from_=1, to=60, orient="horizontal")
        self.movement_duration_scale.grid(row=3, column=0, pady=1)

        tk.Label(master, text="Waiting time before recording the movement (s)").grid(row=4, pady=2)

        self.waiting_time_before_recording_scale = tk.Scale(master, from_=1, to=60, orient="horizontal")
        self.waiting_time_before_recording_scale.grid(row=5, column=0, pady=1)

        record_duration = settings['movement_duration'] - settings['waiting_time_before_recording']
        # TODO: UPDATE THE VALUE RUNTIME
        tk.Label(master, text=f"Record duration: {record_duration} s").grid(row=6, pady=5)

        # Set values
        self.records_entry.insert(0, settings['records'])
        self.movement_duration_scale.set(settings['movement_duration'])
        self.waiting_time_before_recording_scale.set(settings['waiting_time_before_recording'])

        return self.records_entry  # Restituisce l'entry di default per il focus

    def validate(self):
        wt = self.waiting_time_before_recording_scale.get()
        md = self.movement_duration_scale.get()
        records = self.records_entry.get()
        title = "Error"

        try:
            # Convert to int
            value = int(records)
            if value < 1:
                messagebox.showerror(title, "The number of records must be greater then 0")
                return False
        except ValueError:
            messagebox.showerror(title, "Invalid characters at the field 'number of records'. Put a positive number")
            return False

        if wt >= md:
            messagebox.showerror(title, "Movement duration must be greater then waiting time before recording")
            return False

        return True

    def apply(self):
        # Save values
        records = int(self.records_entry.get())
        md = self.movement_duration_scale.get()
        wt = self.waiting_time_before_recording_scale.get()

        settings = DataSystem.create_settings_dict(records,md,wt)
        DataSystem().save_settings_data(settings)