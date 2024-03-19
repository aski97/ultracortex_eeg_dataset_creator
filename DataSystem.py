import numpy as np
import os
from datetime import datetime
from singleton_decorator import singleton


@singleton
class DataSystem:
    _path = "data/"
    _settings_filename = "settings.npy"

    @staticmethod
    def load(filename: str) -> np.ndarray | None:
        try:
            data = np.load(filename, allow_pickle=True)
            return data
        except FileNotFoundError:
            return None

    @staticmethod
    def save(file: np.ndarray, filename: str):
        directory = os.path.dirname(filename)

        if not os.path.exists(directory):
            os.makedirs(directory)

        np.save(filename, file)

    def load_settings_data(self) -> tuple:
        npy_settings = self.load(self.build_data_path(self._settings_filename))

        if npy_settings is None:
            # Create default settings
            settings = self.create_settings_dict(5, 3, 6)

            number_records = int(settings['number_records'])
            focus_duration = int(settings['focus_duration'])
            recording_duration = int(settings['recording_duration'])
            iteration_duration = focus_duration + recording_duration

            return number_records, focus_duration, recording_duration, iteration_duration

        # Convert npy array to dictionary
        setting_elements = dict(npy_settings.tolist())

        number_records = int(setting_elements['number_records'])
        focus_duration = int(setting_elements['focus_duration'])
        recording_duration = int(setting_elements['recording_duration'])
        iteration_duration = focus_duration + recording_duration

        return number_records, focus_duration, recording_duration, iteration_duration

    def save_timeseries_record(self, client_id, timeseries, record_time, hand, session_name):
        # Compute sampling rate
        sr = int(len(timeseries) / record_time)
        # store data into numpy array
        numpy_data_ts = np.array(timeseries)

        directory = self.build_data_path(f"recordings/{client_id}/{session_name}/{hand}/")
        filename = f"TS_{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}_{sr}Hz"

        path = directory + filename
        self.save(numpy_data_ts, path)
        print("Data Saved...")

    def save_settings_data(self, number_records, focus_duration, recording_duration) -> bool:
        # Convert to npy array
        dict_settings = self.create_settings_dict(number_records, focus_duration, recording_duration)
        npy_settings = np.array(list(dict_settings.items()), dtype=object)
        # Save data
        self.save(npy_settings, self.build_data_path(self._settings_filename))

        return True

    @staticmethod
    def create_settings_dict(number_records: int, focus_duration: int, recording_duration: int):
        return {'number_records': number_records, 'focus_duration': focus_duration,
                'recording_duration': recording_duration}

    def build_data_path(self, filename: str) -> str:
        return self._path + filename
