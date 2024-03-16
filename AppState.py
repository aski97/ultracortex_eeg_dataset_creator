from singleton_decorator import singleton


@singleton
class AppState:

    def __init__(self):
        self._settings = None
        self._status = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def settings(self):
        """

        :return: {'records', 'movement_duration', 'waiting_time_before_recording'}
        """
        return self._settings

    @settings.setter
    def settings(self, value):
        self._settings = value
