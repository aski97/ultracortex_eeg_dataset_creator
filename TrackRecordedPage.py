import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from DataSystem import DataSystem


class ScrollablePlotFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class TrackRecordedPage:

    def __init__(self, parent, filename):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Track {filename}")
        self.window.geometry("800x800")

        self.data = DataSystem().load(filename)

        if self.data is None:
            return

        if len(self.data.shape) != 2:
            print("Numpy file must be 2D.")
            return

        self.channels = self.data.shape[1]

        self.checkboxes_vars = []
        self.plots = []

        self.menu_frame = tk.Frame(self.window)
        self.menu_frame.pack(side="top", fill="x", ipady=5)

        self.select_channel_label = tk.Label(self.menu_frame, text="Select Channel:")
        self.select_channel_label.pack(side="left", padx=2)
        for _ in range(self.channels):
            value = tk.BooleanVar()
            value.set(True)
            value.trace_add("write", lambda name, index, mode, var=value: self.on_channel_selection(name, index, mode))
            c = tk.Checkbutton(self.menu_frame, text=f'{_}', variable=value, onvalue=True, offvalue=False)
            c.pack(side="left")

            self.checkboxes_vars.append(value)

        self.select_all_button = tk.Button(self.menu_frame, text="Select all", command=self.select_all_channels)
        self.select_all_button.pack(side="left", padx=5)

        self.deselect_all_button = tk.Button(self.menu_frame, text="Deselect all", command=self.deselect_all_channels)
        self.deselect_all_button.pack(side="left")

        self.scrollable_frame = ScrollablePlotFrame(self.window)
        self.scrollable_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)

        for _ in range(self.channels):
            plot = self.add_plot(self.scrollable_frame.scrollable_frame, _, plot_height=500)
            self.plots.append(plot)

    def on_channel_selection(self,name, index, mode):
        i = int(name.replace('PY_VAR', '')) - 1
        value = self.checkboxes_vars[i].get()

        if value:
            # show plot channel i
            self.plots[i].grid(column=1, row=i)
            pass
        else:
            # disable plot channel i
            self.plots[i].grid_forget()
            pass

    def select_all_channels(self):
        for _ in range(self.channels):
            self.checkboxes_vars[_].set(True)

    def deselect_all_channels(self):
        for _ in range(self.channels):
            self.checkboxes_vars[_].set(False)

    def add_plot(self, frame, channel, plot_height):
        fig = Figure(figsize=(10, 1))

        ax = fig.add_subplot(111)
        ax.plot(self.data[:, channel])
        ax.set_xlabel("time [s]")
        ax.set_ylabel("Signal")
        ax.set_title(f'Channel {channel}')

        container = tk.Frame(frame)
        container.grid(column=1, row=channel)

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.config(height=plot_height)  # Adjust height as needed
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        toolbar_frame = tk.Frame(container)
        toolbar_frame.pack(fill=tk.X, expand=True, pady=[0,30])

        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()

        return container
        # canvas_widget.pack(fill=tk.BOTH, expand=True, pady=[0, 30])
        # canvas_widget.bind('<Configure>', lambda event, canvas_widget : self.frame_width(event, canvas_widget))

    # def frame_width(self, event, canvas_widget):
    #     canvas_width = event.width
    #     canvas_widget.itemconfig(self.scrollable_frame, width=canvas_width)
