import numpy as np
import os
from datetime import datetime
from singleton_decorator import singleton


@singleton
class DataSystem:
    _path = "data/"
    _settings_filename = "settings.npy"

    def load(self, filename: str) -> np.ndarray | None:
        full_path = self._path + filename
        try:
            data = np.load(full_path, allow_pickle=True)
            return data
        except FileNotFoundError:
            return None

    def save(self, file: np.ndarray, filename: str):
        full_path = self._path + filename
        directory = os.path.dirname(full_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        np.save(full_path, file)

    def load_settings_data(self) -> dict:
        npy_settings = self.load(self._settings_filename)

        if npy_settings is None:
            # Create default settings
            return self.create_settings_dict(10, 10, 6)

        # Convert npy array to dictionary
        tuple_list = npy_settings.tolist()
        return dict(tuple_list)

    def save_timeseries_record(self, client_id, timeseries, record_time, hand, session_name):
        # Compute sampling rate
        sr = int(len(timeseries) / record_time)
        # store data into numpy array
        numpy_data_ts = np.array(timeseries)

        directory = f"recordings/{client_id}/{session_name}/{hand}"
        filename = f"TS_{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}_{sr}Hz"

        path = directory + filename
        self.save(numpy_data_ts, path)
        print("Data Saved...")

    def save_settings_data(self, value: dict) -> bool:
        # Check we have all the parameters
        if 'records' not in value or 'movement_duration' not in value or 'waiting_time_before_recording' not in value:
            return False

        # Convert to npy array
        npy_settings = np.array(list(value.items()), dtype=object)
        # Save data
        self.save(npy_settings, self._settings_filename)

        return True

    @staticmethod
    def create_settings_dict(records: int, movement_duration: int, waiting_time_before_recording: int):
        return {'records': records, 'movement_duration': movement_duration,
                'waiting_time_before_recording': waiting_time_before_recording}
