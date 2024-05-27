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
            settings = self.create_settings_dict(5, 2, 1.3, 3, 1.5, "EEG")

            return self.extrapolate_settings_from_dic(settings)

        # Convert npy array to dictionary
        setting_elements = dict(npy_settings.tolist())

        return self.extrapolate_settings_from_dic(setting_elements)

    @staticmethod
    def extrapolate_settings_from_dic(settings: dict) -> tuple:
        number_records = int(settings['number_records'])
        initial_duration = float(settings['initial_duration'])
        focus_duration = float(settings['focus_duration'])
        recording_duration = float(settings['recording_duration'])
        break_duration = float(settings['break_duration'])
        stream_name = settings['stream_name']
        iteration_duration = initial_duration + focus_duration + recording_duration + break_duration

        return number_records, initial_duration, focus_duration, recording_duration, break_duration, iteration_duration, stream_name

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

    def save_settings_data(self, number_records: int, initial_duration: float, focus_duration: float, recording_duration: float, break_duration: float, stream_name: str) -> bool:
        # Convert to npy array
        dict_settings = self.create_settings_dict(number_records,initial_duration, focus_duration, recording_duration, break_duration, stream_name)
        npy_settings = np.array(list(dict_settings.items()), dtype=object)
        # Save data
        self.save(npy_settings, self.build_data_path(self._settings_filename))

        return True

    @staticmethod
    def create_settings_dict(number_records: int, initial_duration: float, focus_duration: float,
                             recording_duration: float, break_duration: float, stream_name: str) -> dict:
        return {'number_records': number_records,
                'initial_duration': initial_duration,
                'focus_duration': focus_duration,
                'recording_duration': recording_duration,
                'break_duration': break_duration,
                'stream_name': stream_name}

    def build_data_path(self, filename: str) -> str:
        return self._path + filename
