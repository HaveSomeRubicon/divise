import ctypes
import os
from ctypes import wintypes

import psutil

from divise.core.models import Window

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

HWND = wintypes.HWND
DWORD = wintypes.DWORD

GetForegroundWindow = user32.GetForegroundWindow
GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextW = user32.GetWindowTextW
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.restype = DWORD
GetWindowThreadProcessId.argtypes = [HWND, ctypes.POINTER(DWORD)]


GetLastError = kernel32.GetLastError


def get_active_window() -> Window | None:
    # Get HWND
    hwnd = GetForegroundWindow()
    if hwnd == 0:
        error_code = GetLastError()
        print(f"Windows error code: {error_code}")
        return None

    # Get path
    try:
        pid = DWORD()
        GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        proc = psutil.Process(pid.value)
        path = proc.exe()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        path = None

    # Get name
    name = os.path.basename(path) if path else None

    # Get title
    length = GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowTextW(hwnd, buff, length + 1)
    title = buff.value

    return Window(hwnd, path, name, title)
