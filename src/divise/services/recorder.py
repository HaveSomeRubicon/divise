import time

from divise import db
from divise.core.models import Window


class RecorderService:
    def __init__(self):
        db.init_db()

    def record(self, window: Window, start_time: float, end_time: float | None = None):
        # No end_time provided - assume it's ending now
        if not end_time:
            end_time = time.time()

        duration = end_time - start_time
        app_id = db.get_app_id(window.name, window.path)

        db.save_session(app_id, start_time, end_time)

        print(f"Program: {window.name}, Duration: {round(duration * 10) / 10}")
