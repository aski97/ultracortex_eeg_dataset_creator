from singleton_decorator import singleton


@singleton
class AppState:

    def __init__(self):
        self._settings = None
        self._number_records = None
        self._focus_duration = None  # Duration of the orange screen
        self._recording_duration = None  # Duration of the green screen
        self._iteration_duration = None  # Duration of the iteration (Focus + Record phase)
        self._status = None
        self._client_id = None
        self._session_name = None
        self._waiting_time = 5
        self._actual_iteration = 0

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @property
    def session_name(self):
        return self._session_name

    @session_name.setter
    def session_name(self, value):
        self._session_name = value

    @property
    def waiting_time(self):
        return self._waiting_time

    @waiting_time.setter
    def waiting_time(self, value):
        self._waiting_time = value

    @property
    def number_records(self):
        """ Total number of records (iterations) to record"""
        return self._number_records

    @number_records.setter
    def number_records(self, value):
        self._number_records = value

    @property
    def focus_duration(self):
        """
        Duration of the focus phase.
        This phase starts at the begging of an iteration to give time to focus to the user.
        """
        return self._focus_duration

    @focus_duration.setter
    def focus_duration(self, value):
        self._focus_duration = value

    @property
    def recording_duration(self):
        """
        Duration of the recording phase.
        After the focus phase starts the record phase where the signals are recorder.
        :return:
        """
        return self._recording_duration

    @recording_duration.setter
    def recording_duration(self, value):
        self._recording_duration = value

    @property
    def iteration_duration(self):
        """
        Duration of the iteration.
        An iteration consist of the focus phase + the recording phase
        :return:
        """
        return self._iteration_duration

    @iteration_duration.setter
    def iteration_duration(self, value):
        self._iteration_duration = value

    @property
    def actual_iteration(self):
        """ Time to wait before to start an iteration """
        return self._actual_iteration

    @actual_iteration.setter
    def actual_iteration(self, value):
        self._actual_iteration = value

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
