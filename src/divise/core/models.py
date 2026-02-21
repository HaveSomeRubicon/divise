from dataclasses import dataclass


@dataclass(frozen=True)
class Window:
    hwnd: int
    path: str
    name: str
    title: str
