import tkinter as tk
from tkinter import messagebox


class Menubar:

    def __init__(self, parent):
        font_specs = ("ubuntu", 14)

        # Definition of menubar
        menubar = tk.Menu(parent.root, font=font_specs)
        parent.root.config(menu=menubar)

        # Dropdown Items
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)

        menubar.add_cascade(label="File", menu=file_dropdown)
        menubar.add_cascade(label="Info", menu=about_dropdown)

        # Command Items
        file_dropdown.add_command(label="Start Session", command=parent.command_start_session)
        file_dropdown.add_command(label="Settings", command=parent.command_open_settings)
        about_dropdown.add_command(label="Copyright", command=self.command_show_copyright_message)

    def command_show_copyright_message(self):
        box_title = "Riguardo PyText"
        box_message = "Un semplice Editor Testuale creato con Python e TkInter!"
        messagebox.showinfo(box_title, box_message)
