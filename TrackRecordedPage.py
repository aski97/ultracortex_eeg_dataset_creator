import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from DataSystem import DataSystem


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

        self.menu_frame = tk.Frame(self.window)
        self.select_channel_label = tk.Label(self.menu_frame, text="Select Channel:")

        self.graph_frame = tk.Frame(self.window)

        # Pack elements
        self.menu_frame.pack(side="top", fill="x", ipady=5)
        self.select_channel_label.pack(side="left", padx=2)

        self.graph_frame.pack(side="top", fill="x", expand=True)

        # main_frame = tk.Frame(self.window)
        # main_frame.pack(fill=tk.BOTH, expand=1)
        #
        # # Create Frame for X Scrollbar
        # sec = tk.Frame(main_frame)
        # sec.pack(fill=tk.X, side=tk.BOTTOM)
        #
        # my_canvas = tk.Canvas(main_frame)
        # my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        #
        # # Add A Scrollbars to Canvas
        # x_scrollbar = ttk.Scrollbar(sec, orient=tk.HORIZONTAL, command=my_canvas.xview)
        # x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        #
        # y_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
        # y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        #
        # # Configure the canvas
        #
        # my_canvas.configure(xscrollcommand=x_scrollbar.set)
        #
        # my_canvas.configure(yscrollcommand=y_scrollbar.set)
        #
        # my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox(tk.ALL)))
        #
        # # Create Another Frame INSIDE the Canvas
        #
        # second_frame = tk.Frame(my_canvas)
        #
        # # Add that New Frame a Window In The Canvas
        #
        # my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

        # self.print()

        # channels = self.data.shape[1]
        channels = 2

        f = Figure(figsize=(10, 10), dpi=100)
        # ax = f.add_subplot(211)
        # ax.plot(self.data[:, 0])
        # ax.set_xlabel("time [s]")
        # ax.set_ylabel("Signal")

        # f, axs = plt.subplots(channels, 1, figsize=(1, 10))
        #
        for i in range(channels):
            ax = f.add_subplot(channels, 1, i+1)
            ax.plot(self.data[:, 0])
            ax.set_xlabel("time [s]")
            ax.set_ylabel("Signal")
            ax.set_title(f'Channel {i}')


        canvas = FigureCanvasTkAgg(f, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.window, pack_toolbar=False)
        toolbar.update()

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def print(self):
        channels = self.data.shape[1]

        f, axs = plt.subplots(channels, 1, figsize=(5, 5))

        for i in range(channels):
            axs[i].plot(self.data[:, i])
            axs[i].set_title(f'Channel {i}')
            axs[i].set_xlabel('Time')
            axs[i].set_ylabel('Signal Value')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(f, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.window)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
