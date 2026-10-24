import tkinter as tk

import customtkinter as ctk

from graphics_lab import actions as fc
from graphics_lab import constants as c
from graphics_lab.ui.theme import (ACCENT, ACCENT_2, BACKGROUND, BORDER, TEXT,
                                   TEXT_2)
from graphics_lab.ui.widgets import Button, Card, Dropdown, Field, Section

RECURSIVE_OPTIONS = [
    "Triángulo de Sierpinski",
    "Alfombra de Sierpinski",
    "Curva de Koch",
    "Copo de nieve de Koch",
    "Árbol binario",
    "Curva de Hilbert",
]


def create_fractal_canvas(parent: ctk.CTkFrame) -> tk.Canvas:
    frame = ctk.CTkFrame(parent, fg_color=BORDER, corner_radius=0)
    frame.pack(side="left", fill="both", expand=True, padx=c.MARGIN,
               pady=c.MARGIN)

    canvas = tk.Canvas(frame, bg=c.FRACTAL_BG, highlightthickness=0)
    canvas.pack(fill="both", expand=True, padx=1, pady=1)
    fc.fractal_canvases.append(canvas)
    return canvas


def create_fractal_panel(parent: ctk.CTkFrame, title_text: str) -> Card:
    panel = Card(parent, width=280)
    panel.pack_propagate(False)
    panel.pack(side="right", fill="y")
    title = ctk.CTkLabel(panel, text=title_text,
                         font=(c.FONT, 18, "bold"), text_color=TEXT)
    title.pack(anchor="w", padx=c.MARGIN, pady=(c.MARGIN, 16))
    return panel


def create_tab(tabview: ctk.CTkTabview, name: str,
               title_text: str) -> tuple[tk.Canvas, Card]:
    tab = tabview.add(name)

    panel = create_fractal_panel(tab, title_text)
    left_area = Card(tab)
    left_area.pack(side="left", fill="both", expand=True, padx=(0, c.MARGIN))
    canvas = create_fractal_canvas(left_area)
    return canvas, panel


def create_row(section: Section) -> ctk.CTkFrame:
    row = ctk.CTkFrame(section, fg_color="transparent")
    row.pack(fill="x", pady=(0, 6))
    return row


def add_draw_button(panel: Card, command) -> None:
    draw_button = Button(panel, "Dibujar", command, primary=True, height=36)
    draw_button.pack(side="bottom", fill="x", padx=c.MARGIN,
                     pady=(8, c.MARGIN))


def create_recursive_tab(tabview: ctk.CTkTabview) -> None:
    canvas, panel = create_tab(tabview, "Recursivos", "Fractales recursivos")
    add_draw_button(panel, lambda: fc.draw_recursive(canvas))

    Dropdown(Section(panel, "Fractal"), RECURSIVE_OPTIONS, "fractal")

    row = create_row(Section(panel, f"Nivel (1 - {c.MAX_FRACTAL_LEVEL})"))
    fc.fractal_fields["level"] = Field(row, "n", default="5")


def create_julia_tab(tabview: ctk.CTkTabview) -> None:
    canvas, panel = create_tab(tabview, "Julia", "Conjunto de Julia")
    add_draw_button(panel, lambda: fc.draw_julia(canvas))
    fields = fc.fractal_fields

    section = Section(panel, "Ventana")
    row = create_row(section)
    fields["julia_xmin"] = Field(row, "xmin", default="-1.5")
    fields["julia_xmax"] = Field(row, "xmax", default="1.5")
    row = create_row(section)
    fields["julia_ymin"] = Field(row, "ymin", default="-1.5")
    fields["julia_ymax"] = Field(row, "ymax", default="1.5")

    row = create_row(Section(panel, "Constante c"))
    fields["julia_re"] = Field(row, "Re", default="-0.7")
    fields["julia_im"] = Field(row, "Im", default="0.27015")

    row = create_row(Section(panel, "Iteraciones y colores"))
    fields["julia_n"] = Field(row, "n", default="30")
    fields["julia_colors"] = Field(row, "colors", default="16")


def create_mandelbrot_tab(tabview: ctk.CTkTabview) -> None:
    canvas, panel = create_tab(tabview, "Mandelbrot",
                               "Conjunto de Mandelbrot")
    add_draw_button(panel, lambda: fc.draw_mandelbrot(canvas))
    fields = fc.fractal_fields

    row = create_row(Section(panel, "Iteraciones y colores"))
    fields["mandelbrot_n"] = Field(row, "n", default="30")
    fields["mandelbrot_colors"] = Field(row, "colors", default="16")

    info = ctk.CTkLabel(panel, justify="left", font=(c.FONT, 13),
                        text_color=TEXT_2,
                        text="x ∈ [-2.5, 2.5]\ny ∈ [-1.5, 1.5]\n"
                             "Z₀ = 0,  Zₙ₊₁ = Zₙ² + c")
    info.pack(anchor="w", padx=c.MARGIN)


def open_fractals_window(root: ctk.CTk) -> None:
    if fc.fractal_window is not None and fc.fractal_window.winfo_exists():
        fc.fractal_window.focus()
        return

    window = ctk.CTkToplevel(root, fg_color=BACKGROUND)
    window.title("Fractales")
    window.protocol("WM_DELETE_WINDOW", fc.close_fractals_window)
    fc.fractal_window = window

    tabview = ctk.CTkTabview(window, fg_color="transparent",
                             segmented_button_selected_color=ACCENT,
                             segmented_button_selected_hover_color=ACCENT_2,
                             segmented_button_fg_color=TEXT_2,
                             segmented_button_unselected_color=TEXT_2,
                             segmented_button_unselected_hover_color=ACCENT_2,
                             text_color=c.WHITE)
    tabview.pack(fill="both", expand=True, padx=24, pady=(6, 24))
    tabview._segmented_button.configure(font=(c.FONT, 14, "bold"))

    create_recursive_tab(tabview)
    create_mandelbrot_tab(tabview)
    create_julia_tab(tabview)
    
    # CTkToplevel resets its state on open, so maximize after it settles
    window.after(100, lambda: window.state("zoomed"))

    window.after(200, window.lift)
    window.after(200, window.focus)
