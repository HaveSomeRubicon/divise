import time
from typing import Callable

from divise.core.models import Window
from divise.os.win32_provider import get_active_window


class MonitorService:
    def __init__(self, record_callback: Callable[[Window, float, float], None]):
        self.running = True
        self.last_window: Window | None = None
        self.start_time: float = time.time()
        self.record_callback = record_callback

    def start(self):
        while self.running:
            active_window = get_active_window()

            # Handle focus loss
            if active_window is None:
                if self.last_window is None:
                    continue
                self._trigger_record()
                self._handle_window_change(None)
                continue

            # Handle first window
            if self.last_window is None:
                self._handle_window_change(active_window)
                continue

            # Handle window change
            if active_window.path != self.last_window.path:
                self._trigger_record()
                self._handle_window_change(active_window)

            time.sleep(1)

    def stop(self):
        if self.running and self.last_window:
            self._trigger_record()
        self.running = False

    def _trigger_record(self):
        self.record_callback(self.last_window, self.start_time)

    def _handle_window_change(self, active_window: Window | None):
        self.start_time = time.time()
        self.last_window = active_window
