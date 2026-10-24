import tkinter as tk
from typing import Callable

import customtkinter as ctk

from graphics_lab import actions as fc
from graphics_lab import constants as c
from graphics_lab.ui.theme import (ACCENT, ACCENT_2, BORDER, CANVAS, PANEL,
                                   TEXT, TEXT_2)


class DrawingCanvas(tk.Canvas):

    def __init__(self, parent: ctk.CTkFrame) -> None:
        super().__init__(parent, width=480, height=400, bg=CANVAS[0],
                         highlightthickness=0, cursor=fc.cursor("brush"))
        self.lines = []
        self.vertices = []
        self.deleted_lines = []
        self.first_point = None

        fc.draw_axes(self)
        self.bind("<Button-1>", lambda event: fc.on_press(event, self))


class Card(ctk.CTkFrame):

    def __init__(self, parent: ctk.CTkFrame, **kwargs) -> None:
        super().__init__(parent, fg_color=PANEL, corner_radius=14,
                         border_width=5, border_color=BORDER, **kwargs)


class Button(ctk.CTkButton):

    def __init__(self, parent: ctk.CTkFrame, text: str,
                 command: Callable[[], None], primary: bool = False,
                 **kwargs) -> None:
        super().__init__(parent, text=text, command=command,
                         corner_radius=8, border_width=1,
                         font=(c.FONT, 13), **kwargs)
        self.highlight(primary)

    def highlight(self, highlighted: bool) -> None:
        if highlighted:
            self.configure(fg_color=ACCENT, hover_color=ACCENT_2,
                           border_color=ACCENT, text_color=c.WHITE)
        else:
            self.configure(fg_color="transparent", hover_color=CANVAS,
                           border_color=BORDER, text_color=TEXT)


class Section(ctk.CTkFrame):

    def __init__(self, parent: ctk.CTkFrame, text: str) -> None:
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="x", padx=c.MARGIN, pady=(0, 14))

        title = ctk.CTkLabel(self, text=text.upper(), height=18,
                             font=(c.FONT, 11, "bold"), text_color=TEXT_2)
        title.pack(anchor="w", pady=(0, 4))


class Field(ctk.CTkEntry):

    def __init__(self, parent: ctk.CTkFrame, text: str,
                 default: str = "0") -> None:
        label = ctk.CTkLabel(parent, text=text, font=(c.FONT, 13),
                             text_color=TEXT_2)
        label.pack(side="left", padx=(9, 6))

        super().__init__(parent, width=50, height=28, justify="center",
                         placeholder_text=default, font=(c.FONT, 13),
                         corner_radius=8, border_width=1,
                         fg_color=CANVAS, border_color=BORDER,
                         text_color=TEXT, placeholder_text_color=TEXT_2)
        # CTkEntry starts with _is_focused=True, so delete() would not bring
        # the placeholder back on a field the user never clicked
        self._is_focused = False
        self.pack(side="left", fill="x", expand=True)


class Dropdown(ctk.CTkOptionMenu):
    def __init__(self, parent: ctk.CTkFrame, options: list[str],
                 key: str) -> None:
        super().__init__(parent, values=options, command=self.save,
                         font=(c.FONT, 13), corner_radius=8,
                         fg_color=CANVAS, text_color=TEXT,
                         button_color=ACCENT, button_hover_color=ACCENT_2,
                         dropdown_fg_color=PANEL, dropdown_text_color=TEXT,
                         dropdown_hover_color=CANVAS)

        self.options = options
        self.key = key
        self.set(options[fc.config[key]])
        self.pack(fill="x")

    def save(self, value: str) -> None:
        fc.config[self.key] = self.options.index(value)
