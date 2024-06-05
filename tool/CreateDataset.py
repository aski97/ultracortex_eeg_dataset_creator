import mne
import numpy as np


mne.set_log_level('WARNING')


def to_categorical(y, num_classes):
    """
    Convert a class vector (integers) to binary class matrix.

    Args:
        y (numpy array): Array of integers representing classes.
        num_classes (int): Total number of classes.

    Returns:
        numpy array: Binary matrix representation of the input.
    """
    y = np.asarray(y, dtype='int32')
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes))
    categorical[np.arange(n), y] = 1
    return categorical


def preprocessing(raw):
    from sklearn.preprocessing import StandardScaler

    # # Rimuove artefatti di rete elettrica
    # freqs = [50]
    # raw.notch_filter(freqs=freqs, filter_length='auto')

    # 1. RESAMPLING -> 250 Hz
    raw.resample(250)
    # 1.1 REDUCE TO 750 SAMPLINGS (some records have 751)
    n_samples = raw.n_times
    if n_samples > 750:
        start_sample = 0
        end_sample = 749
        sfreq = raw.info['sfreq']
        raw = raw.crop(tmin=start_sample / sfreq, tmax=end_sample / sfreq)
    # 2. FILTERING (also 0.5 - 100Hz)
    raw.filter(l_freq=4.0, h_freq=100.0, filter_length="auto")
    # 3. REFERENCING
    raw.set_eeg_reference('average')
    # 4. NORMALIZATION
    scaler = StandardScaler()
    data_normalized = scaler.fit_transform(raw.get_data())
    raw._data = data_normalized

    return raw


def load_preprocessed_raws(client, session):
    import os

    x, y = [], []
    main_dir = os.getcwd()
    path = os.path.join(main_dir, "..", "data", "recordings", client, session)

    for label, action in enumerate(['0', '1', '2']):
        action_dir = os.path.join(path, action)
        for file in os.listdir(action_dir):
            file_path = os.path.join(action_dir, file)
            raw = mne.io.read_raw_fif(file_path, preload=True)
            eeg_preprocessed = preprocessing(raw)
            x.append(eeg_preprocessed.get_data())
            y.append(label)

    x_np = np.array(x)
    y_np = np.array(y)
    y_one_hot = to_categorical(y_np, 3)
    # Ridimensionamento dei dati per adattarli alla CNN 2D.
    return x_np, y_one_hot
    pass


def save_dataset(x_train, x_test, y_train, y_test, path):
    np.save(f"{path}/x_train_4_100Hz_n.npy", x_train)
    # np.save(f"{path}/y_train.npy", y_train)
    np.save(f"{path}/x_test_4_100Hz_n.npy", x_test)
    # np.save(f"{path}/y_test.npy", y_test)


# Create Training set
x_train, y_train = load_preprocessed_raws("0", "1")

# Create Test set
x_test, y_test = load_preprocessed_raws("0", "2")

save_dataset(x_train, x_test, y_train, y_test, "../data/dataset/0")

