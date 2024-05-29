import threading

from singleton_decorator import singleton


@singleton
class AppState:

    def __init__(self):
        self._number_records = None
        self._initial_duration = None  # Duration of phase 1
        self._focus_duration = None  # Duration of phase 2
        self._recording_duration = None  # Duration of the phase 3
        self._break_duration = None  # Duration of the phase 4
        self._iteration_duration = None  # Duration of the iteration (PHASE 1 + PHASE 2 + PHASE 3 + PHASE 4)
        self._iteration_status = None
        self._app_status = None
        self._client_id = None
        self._session_number = None
        self._run_number = None
        self._actual_iteration = 0
        self._session_running_time = 0
        self._actual_selected_hand = 0  # 0 = Left hand, 1 = Right hand
        self._sampling_rate = 0.004  # 250Hz
        self._stream_name = None
        self._stream_status = None
        self._on_stream_status_change = threading.Condition()

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self._client_id = value

    @property
    def session_number(self):
        return self._session_number

    @session_number.setter
    def session_number(self, value):
        self._session_number = value

    @property
    def run_number(self):
        return self._run_number

    @run_number.setter
    def run_number(self, value):
        self._run_number = value

    @property
    def number_records(self):
        """ Total number of records (iterations) to record"""
        return self._number_records

    @number_records.setter
    def number_records(self, value):
        self._number_records = value

    @property
    def initial_duration(self):
        """
        Duration of the initial phase.
        :return:
        """
        return self._initial_duration

    @initial_duration.setter
    def initial_duration(self, value):
        self._initial_duration = value

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
    def break_duration(self):
        """
        Duration of the break phase, after the recording.
        :return:
        """
        return self._break_duration

    @break_duration.setter
    def break_duration(self, value):
        self._break_duration = value

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
    def actual_selected_hand(self):
        """
        The selected hand for the actual iteration.
        It could be 0 for the left hand,
        or 1 for the right hand.
        """
        return self._actual_selected_hand

    @actual_selected_hand.setter
    def actual_selected_hand(self, value):
        self._actual_selected_hand = value

    @property
    def session_running_time(self):
        return self._session_running_time

    @session_running_time.setter
    def session_running_time(self, value):
        self._session_running_time = value

    @property
    def app_status(self):
        return self._app_status

    @app_status.setter
    def app_status(self, value):
        self._app_status = value

    @property
    def iteration_status(self):
        return self._iteration_status

    @iteration_status.setter
    def iteration_status(self, value):
        self._iteration_status = value

    @property
    def sampling_rate(self):
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, value):
        self._sampling_rate = value

    @property
    def stream_name(self):
        return self._stream_name

    @stream_name.setter
    def stream_name(self, value):
        self._stream_name = value

    @property
    def stream_status(self):
        return self._stream_status

    @stream_status.setter
    def stream_status(self, value):
        self._stream_status = value

    @property
    def on_stream_status_change(self):
        return self._on_stream_status_change


