import tkinter as tk


# Commands
def command_start_session():
    print("Inizio sessione")


# window configurations
window = tk.Tk()
window.geometry("600x600")
window.title("Ultracortex EEG Dataset Creator")
window.configure(background="black")

# icons definition
conf_session_icon = tk.PhotoImage(file="assets/img/settings.png")
conf_session_icon = conf_session_icon.subsample(18)  # Ridimensiona l'immagine

# GUI definition
frame = tk.Frame(window)
c_id_label = tk.Label(frame, text="Client ID:")
client_id_entry = tk.Entry(frame)
start_session_btn = tk.Button(frame, text="Start Session", command=command_start_session)
config_session_btn = tk.Button(frame, image=conf_session_icon, compound="center", width=25, height=25, command=lambda: print("Hai cliccato!"))
label = tk.Label(frame, text="00:00")

# Layout injection
frame.pack(side="top", fill="x", ipady=5)
c_id_label.pack(side="left", padx=2)
client_id_entry.pack(side="left", padx=3)
start_session_btn.pack(side="left", padx=10)
config_session_btn.pack(side="left", padx=10)
label.pack(side="left", padx=10)

if __name__ == '__main__':
    window.mainloop()
