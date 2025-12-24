from itertools import cycle
import sys
import threading
import time

class Spinner:
    """Simple terminal spinner shown while work is in progress."""

    def __init__(self, message: str = "Generating") -> None:
        self._message = message
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        def run() -> None:
            symbols = cycle(["|", "/", "-", "\\"])
            while not self._stop.is_set():
                ch = next(symbols)
                sys.stdout.write(f"\r{self._message} {ch}")
                sys.stdout.flush()
                time.sleep(0.1)
            # Clear line when stopping
            sys.stdout.write("\r" + " " * (len(self._message) + 4) + "\r")
            sys.stdout.flush()

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join()