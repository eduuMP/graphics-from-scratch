import tkinter as tk

import customtkinter as ctk

from graphics_lab import actions as fc
from graphics_lab import constants as c
from graphics_lab.ui.theme import ACCENT, ACCENT_2, BORDER, CANVAS, TEXT, TEXT_2
from graphics_lab.ui.widgets import (Button, Card, DrawingCanvas, Dropdown,
                                     Field, Section)

ALGORITHM_OPTIONS = [
    "Slope Intercept",
    "DDA",
    "Bresenham (float)",
    "Bresenham (int)",
]

LINE_TYPE_OPTIONS = [text for text, _ in c.LINE_TYPES]
DIRECTION_OPTIONS = ["Antihorario", "Horario"]
REFLECTION_OPTIONS = [
    "Ninguna",
    "Eje X",
    "Eje Y",
    "Origen",
    "Recta y = mx + b",
]


def create_canvases(parent: ctk.CTkFrame) -> list[DrawingCanvas]:
    bar = ctk.CTkFrame(parent, fg_color="transparent")
    bar.pack(fill="x", padx=c.MARGIN, pady=(c.MARGIN, 10))

    frame = ctk.CTkFrame(parent, fg_color=BORDER, corner_radius=0)
    frame.pack(padx=c.MARGIN)

    canvases = [DrawingCanvas(frame), DrawingCanvas(frame)]

    undo_button = Button(bar, c.ICON_UNDO + "  Deshacer",
                         lambda: fc.undo(fc.active_canvas()), width=0)
    redo_button = Button(bar, c.ICON_REDO + "  Rehacer",
                         lambda: fc.redo(fc.active_canvas()), width=0)
    clear_button = Button(bar, c.ICON_CLEAR + "  Limpiar",
                          lambda: fc.clear_canvas(fc.active_canvas()),
                          width=0)
    eraser_button = Button(bar, c.ICON_ERASER + "  Goma",
                           lambda: fc.toggle_eraser(eraser_button), width=0)
    grid_button = Button(bar, c.ICON_GRID + "  Cuadrícula",
                         lambda: fc.toggle_grid(grid_button), width=0)

    undo_button.pack(side="left")
    redo_button.pack(side="left", padx=6)
    clear_button.pack(side="right")
    eraser_button.pack(side="right", padx=6)
    grid_button.pack(side="right")

    return canvases


def create_pixel_box(parent: ctk.CTkFrame) -> tk.Text:
    title = ctk.CTkLabel(parent, text="PÍXELES PINTADOS", height=18,
                         font=(c.FONT, 11, "bold"), text_color=TEXT_2)
    title.pack(anchor="w", padx=c.MARGIN, pady=(14, 4))

    frame = ctk.CTkFrame(parent, fg_color=CANVAS, corner_radius=8, height=110)
    frame.pack_propagate(False)
    frame.pack(fill="x", padx=c.MARGIN, pady=(0, c.MARGIN))

    scroll = ctk.CTkScrollbar(frame, button_color=BORDER,
                              button_hover_color=TEXT_2)
    scroll.pack(side="right", fill="y", padx=(0, 4), pady=4)

    box = tk.Text(frame, font=(c.MONO_FONT, c.TEXT_BOX_FONT_SIZE),
                  wrap="word", relief="flat", borderwidth=0,
                  highlightthickness=0, bg=CANVAS[0], fg=TEXT[0],
                  yscrollcommand=scroll.set, state="disabled")
    box.pack(side="left", fill="both", expand=True, padx=8, pady=8)
    scroll.configure(command=box.yview)

    return box


def create_empty_panel(parent: ctk.CTkFrame, title_text: str) -> Card:
    panel = Card(parent, width=280)
    panel.pack_propagate(False)
    title = ctk.CTkLabel(panel, text=title_text,
                         font=(c.FONT, 18, "bold"), text_color=TEXT)
    title.pack(anchor="w", padx=c.MARGIN, pady=(c.MARGIN, 16))
    return panel


def create_right_panel_1(parent: ctk.CTkFrame, root: ctk.CTk,
                         canvas: DrawingCanvas) -> tuple[Card, ctk.CTkFrame]:
    panel = create_empty_panel(parent, "Personalizar línea")

    # Algorithm
    Dropdown(Section(panel, "Algoritmo"), ALGORITHM_OPTIONS, "algorithm")

    # Thickness
    thickness_row = Section(panel, "Grosor")
    last = len(c.THICKNESS_OPTIONS) - 1

    thickness_value = ctk.CTkLabel(
        thickness_row, width=30, anchor="e",
        text=c.THICKNESS_OPTIONS[fc.config["thickness"]],
        font=(c.FONT, 14, "bold"), text_color=ACCENT)
    thickness_value.pack(side="right")

    slider = ctk.CTkSlider(thickness_row, from_=0, to=last,
                           number_of_steps=last,
                           command=lambda value: fc.change_thickness(
                               value, thickness_value),
                           fg_color=CANVAS, progress_color=ACCENT,
                           button_color=ACCENT, button_hover_color=ACCENT_2)
    slider.set(fc.config["thickness"])
    slider.pack(side="left", fill="x", expand=True)

    # Color
    swatch = ctk.CTkFrame(Section(panel, "Color"), height=30,
                          corner_radius=8, border_width=1,
                          border_color=BORDER, fg_color=fc.color,
                          cursor="hand2")
    swatch.pack(fill="x")
    swatch.bind("<Button-1>", lambda e: fc.choose_color(swatch))

    # Line type
    Dropdown(Section(panel, "Tipo de línea"), LINE_TYPE_OPTIONS, "style")

    # Actions (bottom of the panel)
    exit_button = Button(panel, "Salir",
                         lambda: fc.close_window(root=root), height=36)
    exit_button.pack(side="bottom", fill="x", padx=c.MARGIN,
                     pady=(8, c.MARGIN))

    random_button = Button(panel, "Línea aleatoria",
                           lambda: fc.create_random_line(canvas),
                           primary=True, height=36)
    random_button.pack(side="bottom", fill="x", padx=c.MARGIN)

    return panel, swatch


def create_row(section: Section, **kwargs) -> ctk.CTkFrame:
    row = ctk.CTkFrame(section, fg_color="transparent")
    row.pack(fill="x", **kwargs)
    return row


def create_right_panel_2(parent: ctk.CTkFrame, root: ctk.CTk) -> Card:
    panel = create_empty_panel(parent, "Transformaciones")
    fields = {}

    exit_button = Button(panel, "Salir",
                         lambda: fc.close_window(root=root), height=36)
    exit_button.pack(side="bottom", fill="x", padx=c.MARGIN,
                     pady=(8, c.MARGIN))

    apply_button = Button(panel, "Aplicar", fc.apply_transformations,
                          primary=True, height=36)
    apply_button.pack(side="bottom", fill="x", padx=c.MARGIN)

    # Translation
    row = create_row(Section(panel, "Traslación"))
    fields["translation_x"] = Field(row, "x")
    fields["translation_y"] = Field(row, "y")

    # Scaling
    row = create_row(Section(panel, "Escalado"))
    fields["scaling_x"] = Field(row, "x", default="1")
    fields["scaling_y"] = Field(row, "y", default="1")

    # Rotation
    row = create_row(Section(panel, "Rotación"))
    fields["rotation"] = Field(row, "α")
    gap = ctk.CTkFrame(row, fg_color="transparent")
    gap.pack(side="left", padx=(10, 0))
    Dropdown(gap, DIRECTION_OPTIONS, "direction")

    # Shearing
    row = create_row(Section(panel, "Shearing"))
    fields["shearing_x"] = Field(row, "x")
    fields["shearing_y"] = Field(row, "y")

    # Reflection
    section = Section(panel, "Reflexión")
    Dropdown(section, REFLECTION_OPTIONS, "reflection")
    row = create_row(section, pady=(6, 0))
    fields["reflection_m"] = Field(row, "m")
    fields["reflection_b"] = Field(row, "b")

    fc.fields = fields
 
    

    return panel
