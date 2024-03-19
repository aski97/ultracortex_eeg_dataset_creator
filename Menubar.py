import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
from TrackRecordedPage import TrackRecordedPage


class Menubar:

    def __init__(self, parent):
        # Definition of menubar
        menubar = tk.Menu(parent.root)
        parent.root.config(menu=menubar)

        self.app = parent

        # Dropdown Items
        file_dropdown = tk.Menu(menubar, tearoff=0)
        about_dropdown = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="File", menu=file_dropdown)
        menubar.add_cascade(label="Info", menu=about_dropdown)

        # Command Items
        file_dropdown.add_command(label="Open track", command=self.open_recorded_track)
        about_dropdown.add_command(label="Copyright", command=self.command_show_copyright_message)

    def command_show_copyright_message(self):
        box_title = "Ultra Cortex Eeg Dataset Creator"
        box_message = "TODO"
        messagebox.showinfo(box_title, box_message)

    def open_recorded_track(self):
        filetypes = [('numpy files', '*.npy')]

        filename = fd.askopenfilename(
            title='Open a Recorded track',
            initialdir='data/recordings',
            filetypes=filetypes)

        TrackRecordedPage(self.app.root, filename)

