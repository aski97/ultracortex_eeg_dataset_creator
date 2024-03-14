import tkinter as tk
from tkinter import simpledialog


class SettingsDialog(simpledialog.Dialog):

    def __init__(self, parent):
        self.samples_entry = None
        self.time_movement_entry = None
        self.time_record_movement_entry = None
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

        tk.Label(master, text="Number of samples:").grid(row=0)

        self.samples_entry = tk.Entry(master)
        self.samples_entry.grid(row=1, column=0)

        tk.Label(master, text="Movement time:").grid(row=2)

        self.time_movement_entry = tk.Entry(master)
        self.time_movement_entry.grid(row=3, column=0)

        tk.Label(master, text="Record movement time:").grid(row=4)

        self.time_movement_entry = tk.Entry(master)
        self.time_movement_entry.grid(row=5, column=0)

        return self.samples_entry  # Restituisce l'entry di default per il focus

    def validate(self):
        return 1

    def apply(self):
        first_value = self.entry1.get()
        second_value = self.entry2.get()
        # Puoi fare qualcosa con i valori qui, ad esempio stamparli
        print("Valore 1:", first_value)
        print("Valore 2:", second_value)
