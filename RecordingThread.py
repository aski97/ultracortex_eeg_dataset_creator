import threading
import time
from AppState import AppState
from DataSystem import DataSystem
from LifecycleStatus import Status
from pylsl import StreamInlet, resolve_stream


class RecordingThread(threading.Thread):
    def __init__(self):
        super(RecordingThread, self).__init__()

        self.app_state = AppState()
        self.data_system = DataSystem()

        self._stop_event = threading.Event()

    def run(self):
        # Searching the stream
        print("looking for an EEG stream...")
        streams = resolve_stream('type', 'EEG')
        if len(streams) > 1:
            print('Number of EEG streams is > 0, picking the first one.')
        else:
            print(f"Stream found")
        # Creating a Streaminlet
        inlet = StreamInlet(streams[0])
        info = inlet.info()
        # print(info.nominal_srate())
        record_data_ts = []
        while True:
            if self.app_state.iteration_status == Status.RECORDING_PHASE:
                sample, timestamps = inlet.pull_sample()
                record_data_ts.append(sample)
                # Waiting time to simulate sampling rate
                time.sleep(self.app_state.sampling_rate)
            elif self.app_state.iteration_status == Status.WAITING_PHASE:
                if record_data_ts:
                    # Save data and empty the list
                    self.save_iteration(record_data_ts)
                    record_data_ts = []
            elif self.app_state.app_status == Status.SESSION_ENDED:
                break

        inlet.close_stream()

    def save_iteration(self, samples):
        print(f"Got {len(samples)} samples")
        self.data_system.save_timeseries_record(self.app_state.client_id,
                                                samples,
                                                self.app_state.recording_duration,
                                                self.app_state.actual_selected_hand,
                                                self.app_state.session_name)

