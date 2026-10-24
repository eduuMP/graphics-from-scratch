TRANSFORMATIONS_1BY1= False

BLACK = "#000000"
WHITE = "#ffffff"

# Light mode
WINDOW_BG_LIGHT      = "#f0f4f8"
PANEL_BG_LIGHT       = "#ffffff"
CANVAS_BG_LIGHT      = "#e8eef5"
ACCENT_LIGHT         = "#1912a3"
ACCENT_HOVER_LIGHT   = "#4338ca"
SECONDARY_TEXT_LIGHT = "#64748b"
BORDER_LIGHT         = "#d8e0ea"
GRID_LIGHT           = "#c3ccd8"

# Dark mode
WINDOW_BG_DARK      = "#0f172a"
PANEL_BG_DARK       = "#1e293b"
CANVAS_BG_DARK      = "#1a2233"
ACCENT_DARK         = "#6366f1"
ACCENT_HOVER_DARK   = "#818cf8"
TEXT_DARK           = "#ffffff"
SECONDARY_TEXT_DARK = "#94a3b8"
BORDER_DARK         = "#334155"
GRID_DARK           = "#2b3648"

# Icons
ICON_UNDO       = "↶"
ICON_REDO       = "↷"
ICON_LIGHT_MODE = "⚪"
ICON_DARK_MODE  = "⚫"
ICON_CLEAR      = "🗑"
ICON_ERASER     = "🧽"
ICON_GRID       = "▦"
ICON_FRACTAL    = "❄"

FONT = "Times New Roman"
MONO_FONT = "Consolas"
TEXT_BOX_FONT_SIZE = 10
MARGIN = 18

PRACTICE_1 = True

THICKNESS_OPTIONS = ["1", "5", "10", "20"]

MAX_FRACTAL_LEVEL = 8

# One color per recursion depth, from black (base) to bright red (deepest)
FRACTAL_PALETTE = [
    "#000000", "#1f0000", "#3d0000", "#5c0000", "#7a0000",
    "#990000", "#b80000", "#d60000", "#ff1a1a",
]
FRACTAL_OUTLINE = "#8b0000"
FRACTAL_BG = "#000000"
FRACTAL_DELAY = 15   # ms between animation ticks
FRACTAL_FRAMES = 300 # roughly how many ticks a full drawing takes

LINE_TYPES = [
    ("_____", [1]),
    ("----",  [1, 1, 1, 1, 0, 0]),
    ("-.-.-", [1, 1, 1, 1, 0, 0, 1, 0, 0]),
    ("-..-..-", [1, 1, 1, 1, 0, 1, 0, 1, 0]),
]

# paths relative to the package folder, app.main() moves there on start
CURSORS = {
    "eraser": {
        True: "@assets/dark_eraser.cur",
        False: "@assets/eraser.cur"},
    "brush": {
        True: "@assets/dark_brush.cur",
        False: "@assets/brush.cur"},
}
