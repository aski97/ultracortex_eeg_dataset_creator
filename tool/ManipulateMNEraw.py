import numpy as np
import mne
from sklearn.preprocessing import StandardScaler


def plot_data(x, y, title):
    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(y, x[:, 1])

    plt.title(title)
    plt.xlabel("time")
    plt.ylabel("Signal")

    plt.show()


raw = mne.io.read_raw_fif("../data/recordings/0/1/0/ts_run_2_03-06-2024-15-56-09_456Hz_raw.fif", preload=True)

n_samples = raw.n_times
print(f"Numero di campioni: {n_samples}")

data = raw.get_data()
y = raw.times

# 1 RAW
plot_data(raw.get_data().T, raw.times, "1) Raw EEG Data")

# # Remove the DC component
# raw.filter(l_freq=0.5, h_freq=None, filter_length='auto')
#
# plot_data(raw.get_data().T, raw.times, "1.1) REMOVING DC component")
#
# # Removes power line artifacts
# freqs = [50]
# raw.notch_filter(freqs=freqs, filter_length='auto')
#
# plot_data(raw.get_data().T, raw.times, "1.2) REMOVING ARTIFACTS")

# 2. Resampling
raw.resample(250)
plot_data(raw.get_data().T, raw.times, "2) RESAMPLING 250Hz")

# 3 BAND-PASS FILTER
# ci concentriamo solo su alcune frequenze di studio
# Delta (0.5 - 4 Hz):
#
# Caratteristiche: onde lente, presenti durante il sonno profondo.
# Utilizzo: filtraggio di segnali di sonno o studi su stati di incoscienza.
# Theta (4 - 8 Hz):
#
# Caratteristiche: associata a stati di sonnolenza, rilassamento e meditazione.
# Utilizzo: studi su rilassamento, meditazione o sonno leggero.
# Alpha (8 - 13 Hz):
#
# Caratteristiche: onde associate a rilassamento, occhi chiusi, ma vigile.
# Utilizzo: studi sulla vigilanza, meditazione, rilassamento e attenzione passiva.
# Beta (13 - 30 Hz):
#
# Caratteristiche: onde più veloci associate a stati di veglia, attività mentale e concentrazione.
# Utilizzo: studi su concentrazione, ansia, stati di veglia attiva.
# Gamma (30 - 100 Hz):
#
# Caratteristiche: onde ad alta frequenza associate a processi cognitivi complessi, attenzione e percezione.
# Utilizzo: studi su funzioni cognitive, attenzione e percezione.
raw.filter(l_freq=4, h_freq=100.0, filter_length="auto")

plot_data(raw.get_data().T, raw.times, "3) Added Filter")

# 4. Riferimento comune
raw.set_eeg_reference('average')

plot_data(raw.get_data().T, raw.times, "4) Added Reference")

# # 5. Rimozione degli artefatti oculari e muscolari (ICA)
# ica = mne.preprocessing.ICA(n_components=16, random_state=97)
# ica.fit(raw)
# ica.exclude = ica.find_bads_eog(raw)
# raw = ica.apply(raw)
#
# plot_data(raw.get_data().T, raw.times, "5) ICA")

# 6. Normalizzazione
# Ottieni i dati delle epoche in formato array
data = raw.get_data()

# Applica la normalizzazione
scaler = StandardScaler()
data_normalized = scaler.fit_transform(data)

# Aggiorna le epoche con i dati normalizzati
raw._data = data_normalized

plot_data(raw.get_data().T, raw.times, "5) NORMALIZED DATA")
