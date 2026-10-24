import os

import customtkinter as ctk

from graphics_lab import actions as fc
from graphics_lab import constants as c
from graphics_lab.ui.layout import (create_canvases, create_pixel_box,
                                    create_right_panel_1, create_right_panel_2)
from graphics_lab.ui.fractals_view import open_fractals_window
from graphics_lab.ui.theme import BACKGROUND, TEXT
from graphics_lab.ui.widgets import Button, Card


def main() -> None:
    # the cursor paths in constants are relative to this folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    ctk.set_appearance_mode("light")

    root = ctk.CTk(fg_color=BACKGROUND)
    root.title("Creador de líneas")
    root.resizable(True, True)

    header = ctk.CTkFrame(root, fg_color="transparent")
    header.pack(fill="x", padx=24, pady=(18, 12))

    title = ctk.CTkLabel(header, text="Creador de líneas",
                         font=(c.FONT, 24, "bold"), text_color=TEXT)
    title.pack(side="left", padx=(12, 0))

    theme_button = Button(header, c.ICON_DARK_MODE, lambda:
                          fc.toggle_theme(theme_button, swatch), width=40)
    theme_button.pack(side="right")

    practice_button = Button(header, "", lambda:
                             fc.toggle_practice(panel_1, panel_2,
                                                practice_button), width=190)
    practice_button.pack(side="right")

    fractals_button = Button(header, c.ICON_FRACTAL + "  Fractales",
                             lambda: open_fractals_window(root), width=0)
    fractals_button.pack(side="right", padx=6)

    body = ctk.CTkFrame(root, fg_color="transparent")
    body.pack(padx=24, pady=(0, 24))

    left_area = Card(body)
    left_area.pack(side="left", fill="y")

    fc.canvases = create_canvases(left_area)
    fc.pixel_box = create_pixel_box(left_area)
    panel_1, swatch = create_right_panel_1(body, root, fc.canvases[0])
    panel_2 = create_right_panel_2(body, root)
    fc.show_practice(panel_1, panel_2, practice_button)

    root.mainloop()


if __name__ == "__main__":
    main()
