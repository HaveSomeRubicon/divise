from divise.services.monitor import MonitorService
from divise.services.recorder import RecorderService


def main() -> None:
    recorder = RecorderService()
    monitor = MonitorService(recorder.record)
    monitor.start()


if __name__ == "__main__":
    main()
