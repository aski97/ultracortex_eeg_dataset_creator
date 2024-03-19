import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import pandas as pd

# Configurazione:
plot_graphs = True  # Scegli se desideri visualizzare i grafici o meno
selected_channel = 1 # Seleziona il canale che vuoi visualizzare (parte da 0, il canale 0 è il primo elettrodo)
file_number = 1 # Seleziona il numero del file che vuoi leggere (1, 2, 3, ...)
directory_name = "../recordings/0/Session 1/0/"  # Seleziona il nome della cartella dove sono salvati i file numpy

plot_all_channels = True  # Scegli se desideri visualizzare tutti i 16 canali


selected_channel -= 1 # Si sottrae 1 perché gli indici in Python iniziano da 0 ma io voglio inserire il numero del canale
def load_and_print(filename):
    # Stampa il nome del file che si sta leggendo
    file_name_only = os.path.basename(filename)
    print(f"Nome file: {file_name_only}\n")
    # Carica il file numpy
    data = np.load(filename)

    # Stampa le informazioni sulla dimensione dell'array
    print(f"Dimensione dell'array: {data.shape}\n")

    # Se l'array è 2D, converti direttamente in DataFrame e stampa
    if len(data.shape) == 2:
        df = pd.DataFrame(data)
        print(df)

        if plot_graphs:
            # Grafico del canale selezionato
            plt.plot(data[:, selected_channel])
            plt.title(f'EEG Signal Over Time for Channel {selected_channel + 1}')
            plt.xlabel('Time')
            plt.ylabel('Signal Value')
            plt.show()

            if plot_all_channels:
                # Grafico di tutti i 16 canali
                for i in range(16):
                    plt.subplot(4, 4, i+1) # 4 righe e 4 colonne
                    plt.plot(data[:, i])
                    plt.title(f'Channel {i + 1}')
                plt.tight_layout() # Per evitare sovrapposizioni
                plt.show()
    else:
        print("Il file numpy deve essere 2D.")

if __name__ == "__main__":
    load_and_print("TS_19-03-2024-14-46-57_95Hz.npy")
    # numpy_files = sorted(glob.glob(os.path.join("../recordings/0/Session 1/0/", '*.npy')))
    # if numpy_files and file_number <= len(numpy_files):
    #     filename = numpy_files[file_number - 1]  # Si sottrae 1 perché gli indici in Python iniziano da 0
    #     load_and_print(filename)
    # elif file_number > len(numpy_files):
    #     print(f"Il numero del file selezionato ({file_number}) è maggiore del numero di file disponibili ({len(numpy_files)}).")
    # else:
    #     print("Non sono stati trovati file numpy nella directory specificata.")
