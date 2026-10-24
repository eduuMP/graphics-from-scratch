from __future__ import annotations

import random
import tkinter as tk
from tkinter import colorchooser
from typing import TYPE_CHECKING

import customtkinter as ctk

from graphics_lab import constants as c
from graphics_lab.algorithms import transformations as tf
from graphics_lab.algorithms.lines import (bresenham_float, bresenham_int,
                                           dda, slope_intercept)

if TYPE_CHECKING:
    from graphics_lab.ui.widgets import Button, DrawingCanvas, Field

Point = tuple[int, int]

ALGORITHMS = [slope_intercept, dda, bresenham_float, bresenham_int]
ERASER_RADIUS = 5

config = {"algorithm": 0, "thickness": 1, "style": 0,
          "direction": 0, "reflection": 0, "fractal": 0}
color = c.BLACK
erase_mode = False
grid_visible = False
dark_mode = False
practice_1 = c.PRACTICE_1
pixel_box = None
fields: dict[str, Field] = {}

canvases = []

fractal_window = None
fractal_canvases: list[tk.Canvas] = []
fractal_fields: dict[str, Field] = {}
fractal_job = None


# Coords

def delta() -> int:
    return int(c.THICKNESS_OPTIONS[config["thickness"]])


def screen_to_logical(x: int, y: int, canvas: DrawingCanvas) -> Point:
    x = x - canvas.winfo_width() // 2
    y = canvas.winfo_height() // 2 - y
    return x // delta(), y // delta()


def logical_to_screen(x: float, y: float, canvas: tk.Canvas,
                      scale: int | None = None) -> Point:
    # Fractal canvases pass scale=1, they do not depend on the thickness
    scale = delta() if scale is None else scale
    x = round(x * scale + canvas.winfo_width() // 2)
    y = round(canvas.winfo_height() // 2 - y * scale)
    return x, y


# Paint

def choose_color(swatch: ctk.CTkFrame) -> None:
    global color
    new_color = colorchooser.askcolor(color)[1]
    if new_color is None:
        return
    color = new_color
    swatch.configure(fg_color=color)


def draw_axes(canvas: DrawingCanvas) -> None:
    width = int(canvas.cget("width"))
    height = int(canvas.cget("height"))
    cx = width // 2
    cy = height // 2

    gray = c.SECONDARY_TEXT_LIGHT
    canvas.create_line(0, cy, width, cy, fill=gray, arrow="last",
                       tags="axes")
    canvas.create_line(cx, height, cx, 0, fill=gray, arrow="last",
                       tags="axes")
    canvas.create_text(width - 8, cy + 10, text="X", fill=gray,
                       tags="axes")
    canvas.create_text(cx + 10, 8, text="Y", fill=gray, tags="axes")


def draw_grid(canvas: DrawingCanvas) -> None:
    canvas.delete("grid")
    # with thickness 1 the grid would cover the whole canvas
    if not grid_visible or delta() == 1:
        return

    width = int(canvas.cget("width"))
    height = int(canvas.cget("height"))
    # lines go through the origin so they match the pixel borders
    start_x = (width // 2) % delta()
    start_y = (height // 2) % delta()

    gray = c.GRID_DARK if dark_mode else c.GRID_LIGHT
    for x in range(start_x, width, delta()):
        canvas.create_line(x, 0, x, height, fill=gray, tags="grid")
    for y in range(start_y, height, delta()):
        canvas.create_line(0, y, width, y, fill=gray, tags="grid")
    canvas.tag_lower("grid")


def border_color(fill_color: str) -> str:
    r = int(fill_color[1:3], 16)
    g = int(fill_color[3:5], 16)
    b = int(fill_color[5:7], 16)
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    if brightness > 128:
        return c.BLACK
    return c.WHITE


def paint_pixel(canvas: DrawingCanvas, x: int, y: int, fill: str,
                border: str) -> int:
    nx, ny = logical_to_screen(x, y, canvas)
    return canvas.create_rectangle(nx, ny, nx + delta(), ny - delta(),
                                   fill=fill, outline=border)


def paint_real_line(canvas: DrawingCanvas, start: Point, end: Point,
                    line_color: str) -> int:
    half = delta() / 2
    x0, y0 = logical_to_screen(*start, canvas)
    x1, y1 = logical_to_screen(*end, canvas)
    return canvas.create_line(x0 + half, y0 - half, x1 + half, y1 - half,
                              fill=line_color)


def paint_line(canvas: DrawingCanvas, pixels: list[Point], start: Point,
               end: Point, fill: str) -> list[int]:
    pattern = c.LINE_TYPES[config["style"]][1]
    border = border_color(fill)

    items = []
    for i, (x, y) in enumerate(pixels):
        if pattern[i % len(pattern)]:
            items.append(paint_pixel(canvas, x, y, fill, border))
    if practice_1:
        items.append(paint_real_line(canvas, start, end, border))
    return items


def text_tag(items: list[int]) -> str:
    # text box tag that groups the coords written for one line
    return f"line{id(items)}"


def write_coords(start: Point, end: Point, pixels: list[Point],
                 tag: str) -> None:
    pixels_text = ", ".join(f"({x},{y})" for x, y in pixels)

    pixel_box.config(state="normal")
    pixel_box.tag_delete(tag)
    pixel_box.insert("end", f"Punto inicial: ({start[0]},{start[1]})"
                            f"| Punto final: ({end[0]},{end[1]})\n", tag)
    pixel_box.insert("end", pixels_text + "\n\n", tag)
    pixel_box.see("end")
    pixel_box.config(state="disabled")


def plot_line(canvas: DrawingCanvas, start: Point, end: Point,
              fill: str) -> None:
    algorithm = ALGORITHMS[config["algorithm"]]
    pixels = algorithm(*start, *end)

    items = paint_line(canvas, pixels, start, end, fill)
    write_coords(start, end, pixels, text_tag(items))
    canvas.lines.append(items)
    # endpoints in logical coords, so the line can be transformed later
    canvas.vertices.append((start, end, fill, items))
    clear_deleted(canvas)


# Canvas

def active_canvas() -> DrawingCanvas:
    if practice_1:
        return canvases[0]
    return canvases[1]


def on_press(event: tk.Event, canvas: DrawingCanvas) -> None:
    if not erase_mode:
        on_click(event, canvas)
    else:
        erase(event, canvas)


def on_click(event: tk.Event, canvas: DrawingCanvas) -> None:
    point = screen_to_logical(event.x, event.y, canvas)

    if canvas.first_point is None:
        canvas.first_point = point
        return

    plot_line(canvas, canvas.first_point, point, color)
    canvas.first_point = None


def create_random_line(canvas: DrawingCanvas) -> None:
    width = canvas.winfo_width()
    height = canvas.winfo_height()

    start = screen_to_logical(random.randint(0, width),
                              random.randint(0, height), canvas)
    end = screen_to_logical(random.randint(0, width),
                            random.randint(0, height), canvas)
    random_color = f"#{random.randint(0, 0xFFFFFF):06x}"

    plot_line(canvas, start, end, random_color)
    canvas.first_point = None


def set_state(canvas: DrawingCanvas, items: list[int], state: str) -> None:
    for item in items:
        canvas.itemconfigure(item, state=state)


def clear_deleted(canvas: DrawingCanvas) -> None:
    pixel_box.config(state="normal")
    for items in canvas.deleted_lines:
        canvas.delete(*items)
        tag = text_tag(items)
        ranges = pixel_box.tag_ranges(tag)
        if ranges:
            pixel_box.delete(*ranges)
        pixel_box.tag_delete(tag)
    pixel_box.config(state="disabled")
    canvas.deleted_lines.clear()


def undo(canvas: DrawingCanvas) -> None:
    if not canvas.lines:
        return
    items = canvas.lines.pop()
    set_state(canvas, items, "hidden")
    pixel_box.tag_configure(text_tag(items), elide=True)
    canvas.deleted_lines.append(items)


def redo(canvas: DrawingCanvas) -> None:
    if not canvas.deleted_lines:
        return
    items = canvas.deleted_lines.pop()
    set_state(canvas, items, "normal")
    pixel_box.tag_configure(text_tag(items), elide=False)
    canvas.lines.append(items)


def erase(event: tk.Event, canvas: DrawingCanvas) -> None:
    area = (event.x - ERASER_RADIUS, event.y - ERASER_RADIUS,
            event.x + ERASER_RADIUS, event.y + ERASER_RADIUS)

    erased = []
    for item in canvas.find_overlapping(*area):
        tags = canvas.gettags(item)
        if "axes" in tags or "grid" in tags:
            continue
        if canvas.itemcget(item, "state") == "hidden":
            continue
        erased.append(item)

    if erased:
        set_state(canvas, erased, "hidden")
        canvas.deleted_lines.append(erased)


def clear_pixel_box() -> None:
    pixel_box.config(state="normal")
    pixel_box.delete("1.0", "end")
    pixel_box.config(state="disabled")


def clear_canvas(canvas: DrawingCanvas) -> None:
    canvas.delete("all")
    draw_axes(canvas)
    draw_grid(canvas)
    canvas.lines.clear()
    canvas.vertices.clear()
    canvas.deleted_lines.clear()
    canvas.first_point = None
    clear_pixel_box()


# Transformations
 
def read_field(key: str, default: float,
               source: dict[str, Field] | None = None) -> float:
    #If none --> called from transformations else fractals
    source = fields if source is None else source
    text = source[key].get().strip()
    if text == "":
        return default
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return default


def total_matrix() -> tf.Matrix:
    t = tf.translation(read_field("translation_x", 0),
                       read_field("translation_y", 0))
    s = tf.scaling(read_field("scaling_x", 1), read_field("scaling_y", 1))
    r = tf.rotation(read_field("rotation", 0), config["direction"] == 1)
    h = tf.shearing(read_field("shearing_x", 0), read_field("shearing_y", 0))
    f = tf.reflection(config["reflection"], read_field("reflection_m", 0),
                      read_field("reflection_b", 0))

    return t @ f @ h @ r @ s


def apply_transformations() -> None:
    canvas = active_canvas()
    matrix = total_matrix()

    # only visible lines: undone ones are no longer in canvas.lines
    old = [v for v in canvas.vertices if v[3] in canvas.lines]

    # delete everything drawn, plot_line fills lines and vertices again
    for items in canvas.lines:
        canvas.delete(*items)
    canvas.lines.clear()
    canvas.vertices = []
    clear_pixel_box()

    for start, end, line_color, _ in old:
        new_start, new_end = tf.transform_line(matrix, start, end)
        plot_line(canvas, new_start, new_end, line_color)

    if c.TRANSFORMATIONS_1BY1:
        for field in fields.values():
            field.delete(0, "end")


# Eraser and theme

def cursor(key: str) -> str:
    return c.CURSORS[key][dark_mode]


def canvas_cursor() -> str:
    if erase_mode:
        return cursor("eraser")
    return cursor("brush")


def toggle_eraser(eraser_button: Button) -> None:
    global erase_mode
    erase_mode = not erase_mode
    eraser_button.highlight(erase_mode)

    for canvas in canvases:
        canvas.configure(cursor=canvas_cursor())


def toggle_grid(grid_button: Button) -> None:
    global grid_visible
    grid_visible = not grid_visible
    grid_button.highlight(grid_visible)

    for canvas in canvases:
        draw_grid(canvas)


def toggle_theme(button: Button, swatch: ctk.CTkFrame) -> None:
    global dark_mode, color
    dark_mode = not dark_mode

    if dark_mode:
        canvas_bg, text = c.CANVAS_BG_DARK, c.TEXT_DARK
        ctk.set_appearance_mode("dark")
        button.configure(text=c.ICON_LIGHT_MODE)
    else:
        canvas_bg, text = c.CANVAS_BG_LIGHT, c.BLACK
        ctk.set_appearance_mode("light")
        button.configure(text=c.ICON_DARK_MODE)

    for canvas in canvases:
        canvas.configure(bg=canvas_bg, cursor=canvas_cursor())
        draw_grid(canvas)
    pixel_box.configure(bg=canvas_bg, fg=text)

    if color in (c.BLACK, c.TEXT_DARK):
        color = text
        swatch.configure(fg_color=color)


def show_practice(panel_1: ctk.CTkFrame, panel_2: ctk.CTkFrame,
                  button: Button) -> None:
    if practice_1:
        visible, hidden = panel_1, panel_2
        button.configure(text="Acceder a Transformaciones")
    else:
        visible, hidden = panel_2, panel_1
        button.configure(text="Acceder a Algoritmos de línea")

    hidden.pack_forget()
    visible.pack(side="left", fill="y", padx=(c.MARGIN, 0))

    for canvas in canvases:
        canvas.pack_forget()
    active_canvas().pack(padx=1, pady=1)


def toggle_practice(panel_1: ctk.CTkFrame, panel_2: ctk.CTkFrame,
                    button: Button) -> None:
    global practice_1
    practice_1 = not practice_1
    clear_pixel_box()
    show_practice(panel_1, panel_2, button)


def change_thickness(value: float, label: ctk.CTkLabel) -> None:
    index = round(value)
    config["thickness"] = index
    label.configure(text=c.THICKNESS_OPTIONS[index])
    for canvas in canvases:
        draw_grid(canvas)


def close_window(root: ctk.CTk) -> None:
    root.destroy()


# Fractals

def close_fractals_window() -> None:
    global fractal_window
    for canvas in fractal_canvases:
        stop_fractal_animation(canvas)
    fractal_canvases.clear()
    fractal_fields.clear()
    fractal_window.destroy()
    fractal_window = None


def fill_triangle(canvas: tk.Canvas, vertices: list[tuple[float, float]],
                  fill: str) -> None:
    pass



def sierpinski(a: tuple[float, float], b: tuple[float, float],
               top: tuple[float, float], level: int, depth: int = 1):
    pass

def stop_fractal_animation(canvas: tk.Canvas) -> None:
    pass


def animate_triangles(canvas: tk.Canvas, triangles: list, start: int = 0,
                      step: int = 1) -> None:
    pass

def draw_recursive(canvas: tk.Canvas) -> None:
    pass


def draw_julia(canvas: tk.Canvas) -> None:
    pass


def draw_mandelbrot(canvas: tk.Canvas) -> None:
    pass


# If m is less than 0 another change is needed. It can be solved, but it gets
# more complex; the fastest way is to reflect it with a transformation,
# flipping some signs?

# if y1 == y2, we already have the points

# if x1 == x2, the division gives infinity, so draw that line separately

