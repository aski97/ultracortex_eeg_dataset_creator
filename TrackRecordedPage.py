import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from DataSystem import DataSystem


class TrackRecordedPage():

    def __init__(self, parent, filename):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Track {filename}")
        self.window.geometry("800x800")

        data = DataSystem().load(filename)

        if data is None:
            return
        f, axs = plt.subplots(3, 1, figsize=(5, 5))

        if len(data.shape) == 2:
            for i in range(3):
                axs[i].plot(data[:, i])
                # a[i].set_title(f'EEG Signal Over Time for Channel {i}')
                # a.xlabel('Time')
                # a.ylabel('Signal Value')
        else:
            print("Il file numpy deve essere 2D.")

        canvas = FigureCanvasTkAgg(f, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self.window)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
