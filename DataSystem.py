import numpy as np


class DataSystem:
    _instance = None
    _path = "data/"
    _settings_filename = "settings.npy"

    settings = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.load_settings_data()

    def load(self, filename: str) -> np.ndarray | None:
        full_path = self._path + filename
        try:
            data = np.load(full_path, allow_pickle=True)
            return data
        except FileNotFoundError:
            return None

    def save(self, file: np.ndarray, filename: str):
        full_path = self._path + filename
        np.save(full_path, file)

    def load_settings_data(self):
        npy_settings = self.load(self._settings_filename)

        if npy_settings is None:
            # Create default settings
            self.settings = self.create_settings_dict(10, 10, 6)
            return

        # Convert npy array to dictionary
        tuple_list = npy_settings.tolist()
        self.settings = dict(tuple_list)

    def save_settings_data(self, value: dict) -> bool:
        # Check we have all the parameters
        if 'records' not in value or 'movement_duration' not in value or 'waiting_time_before_recording' not in value:
            return False

        # Update local value
        self.settings = value
        # Convert to npy array
        npy_settings = np.array(list(self.settings.items()), dtype=object)
        # Save data
        self.save(npy_settings, self._settings_filename)

        return True

    @staticmethod
    def create_settings_dict(records: int, movement_duration: int, waiting_time_before_recording: int):
        return {'records': records, 'movement_duration': movement_duration,
                'waiting_time_before_recording': waiting_time_before_recording}
