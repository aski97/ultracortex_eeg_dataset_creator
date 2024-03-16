import threading
from main import UEDatasetCreator

# Variabile globale per il debug:
debug_mode = False
timestamps_debug = []
# funzioni di debug
# def print_debug_timestamps():  #non attivare su entrambi i thread in contemporanea
#     print("\nTimestamps Debug:")
#     print("Inizio Registrazione - Fine Registrazione - Durata - Intervallo Successivo")
#     for i in range(len(timestamps_debug) - 1):
#         start, end = timestamps_debug[i]
#         next_start, _ = timestamps_debug[i + 1]
#         duration = end - start
#         interval = next_start - end
#         print(f"{start} - {end} - {duration:.2f} secondi - {interval:.2f} secondi")
#     start, end = timestamps_debug[-1]
#     print(f"{start} - {end} - {end - start:.2f} secondi")
# # =======================================================================================================================
# # uso il primo timestamp in arrivo dallo stream e conto record_time secondi in avanti su di esso
# def buffer_receive(record_time,stop_event):
#     # Cerca lo stream:
#     streams = resolve_stream('type', 'TS')
#     # Crea un nuovo StreamInlet:
#     inlet = StreamInlet(streams[0])
#     #print("Stream trovato...")
#     # Inizializza il timestamp di inizio:
#     start_timestamp = None
#     # Estrai i campioni accumulati nel buffer:
#     record_data_ts = []
#     #print("Inizio registrazione...")
#     while True:
#         if stop_event.is_set():
#             break
#         sample, timestamp = inlet.pull_sample()
#         if start_timestamp is None:
#             start_timestamp = timestamp
#         end_timestamp = timestamp  # aggiorno ogni iterazione per avere quello finale
#         record_data_ts.append(sample)
#         # Controlla se è passato il tempo desiderato:
#         if timestamp - start_timestamp >= record_time:
#             break
#     # Chiudi lo stream, terminando la ricezione dei dati:
#     inlet.close_stream()
#     #print("Ricezione dati terminata e stream chiuso.")
#     timestamps_debug.append((start_timestamp, end_timestamp))
#     return record_data_ts
# #=======================================================================================================================
#

class RecordingThread(threading.Thread):
    def __init__(self):
        super(RecordingThread, self).__init__()
        self.app = UEDatasetCreator()
        self.client_id = self.app.get_client_id()
        # self.data_system = DataSystem()

        # self.record_time = record_time
        # self.session_name = session_name
        self._stop_event = threading.Event()

    def run(self):
        print("Ce l'abbiamo fatta")
        # # TODO: put a while and conditions
        # record_data_ts = buffer_receive(self.record_time,self._stop_event)
        # # TODO: make placeholders dynamic
        # self.app.data_system.save_timeseries_record(self.client_id,record_data_ts, self.record_time, "Left", self.session_name)
        #
        # if debug_mode:
        #     print_debug_timestamps()
    def stop(self):
        self._stop_event.set()