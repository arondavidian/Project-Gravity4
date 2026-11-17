from __future__ import annotations

import json
import math
import os
import sys
import threading
import time
from array import array
from collections import OrderedDict
from typing import Iterable

import pygame



ROWS = 6
COLUMNS = 7
EMPTY = 0
PLAYER = 1
AI = 2
WINDOW_LENGTH = 4
DEFAULT_DEPTH = 6
FPS = 60
CELL_SIZE = 100
TOKEN_SIZE = int(CELL_SIZE * 0.75)
HOLE_RADIUS = int(CELL_SIZE * 0.42)
SIDE_MARGIN = 40
TOP_BAR_HEIGHT = CELL_SIZE
BOTTOM_MARGIN = 80
BOARD_PADDING = 12
BOARD_WIDTH = COLUMNS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE
WIDTH = BOARD_WIDTH + 2 * SIDE_MARGIN
HEIGHT = TOP_BAR_HEIGHT + BOARD_HEIGHT + BOTTOM_MARGIN
BOARD_LEFT = (WIDTH - BOARD_WIDTH) // 2
BOARD_TOP = TOP_BAR_HEIGHT
RADIUS = int(CELL_SIZE * 0.38)
AI_DELAY_MS = 300
DROP_GRAVITY = 1800.0
DROP_START_VELOCITY = 0.0
DROP_MAX_VELOCITY = 900.0
DROP_BOUNCE_DAMPING = 0.22
DROP_MIN_BOUNCE_SPEED = 120.0

MODE_AI_FIRST = 1
MODE_AI_SECOND = 2
MODE_PVP = 3
ACTION_PLAY = "play"
ACTION_SETTINGS = "settings"
ACTION_BACK = "back"

STATE_START = "start"
STATE_MENU = "menu"
STATE_PLAY_MENU = "play_menu"
STATE_AI_MENU = "ai_menu"
STATE_DIFFICULTY = "difficulty"
STATE_GAME = "game"
STATE_WIN_ANIMATION = "win_animation"
STATE_WIN_PAUSE = "win_pause"
STATE_GAME_OVER = "game_over"
STATE_SETTINGS = "settings"
STATE_PAUSED = "paused"

EASY = 1
MEDIUM = 2
HARD = 3
AI_SEARCH_DEPTHS = {EASY: 3, MEDIUM: 5, HARD: 7}
AI_SEARCH_TIME_LIMITS = {EASY: 0.7, MEDIUM: 1.8, HARD: 4.0}

BACKGROUND_COLOR = (12, 18, 28)
BOARD_COLOR = (30, 90, 200)
HOLE_COLOR = (8, 12, 20)
RUBY_RED = (215, 38, 76, 150)
CYAN_BLUE = (55, 225, 255, 150)
TEXT_COLOR = (220, 230, 255)
BUTTON_COLOR = (240, 240, 240)
BUTTON_HOVER_COLOR = (255, 255, 255)
BUTTON_TEXT_COLOR = (20, 24, 34)
SUBTEXT_COLOR = (180, 190, 205)
BUTTON_GREEN = (80, 200, 120)
WIN_HIGHLIGHT_COLOR = (60, 255, 120)
ACCENT_COLOR = (99, 188, 255)
BOARD_TOP_COLOR = (67, 140, 255)
BOARD_BOTTOM_COLOR = (21, 74, 184)
PANEL_COLOR = (19, 26, 40)
PANEL_SHADOW = (5, 8, 14)
HOLE_INNER_COLOR = (16, 23, 37)
BUTTON_SHADOW_COLOR = (8, 12, 20)
HOVER_GLOW_COLOR = (255, 255, 255)
BUTTON_WIDTH = 280
BUTTON_HEIGHT = 80
SLIDER_WIDTH = 320
SLIDER_HEIGHT = 10
SETTINGS_PANEL_WIDTH = 420
SETTINGS_BUTTON_HEIGHT = 58
TITLE_GRADIENT_TOP = (0, 200, 255)
TITLE_GRADIENT_BOTTOM = (0, 100, 255)
TITLE_GLOW_COLOR = (110, 220, 255)
TITLE_GLOW_ALPHA = 90
MIN_UI_FONT_SIZE = 14
PADDING = 16
TEXT_PADDING = 16
SPACING = 40
LINE_SPACING = 10
TEXT_BLOCK_SPACING = 18
TEXT_LINE_GAP = 14
TOP_TEXT_PADDING = 80
TEXT_LIST_SPACING = 60
SAVE_FILE = "connect4_save.json"
MENU_TITLE_Y = 78
MENU_SUBTITLE_Y = 168
MENU_FIRST_BUTTON_Y = 292
MENU_BUTTON_SPACING = 88
MENU_BACK_BUTTON_Y = 568
BUTTON_PADDING_X = 28
BUTTON_PADDING_Y = 18
START_MENU_TITLE_Y = 54
START_MENU_SUBTITLE_Y = START_MENU_TITLE_Y + 140
START_MENU_INFO_Y = START_MENU_SUBTITLE_Y + 94
START_MENU_PLAY_BUTTON_Y = START_MENU_INFO_Y + 118
START_MENU_SECONDARY_BUTTON_Y = HEIGHT - 100
START_MENU_BUTTON_GAP = SPACING
START_MENU_PLAY_BUTTON_WIDTH = 360
START_MENU_PLAY_BUTTON_HEIGHT = 96
START_MENU_SECONDARY_BUTTON_WIDTH = 210
START_MENU_SECONDARY_BUTTON_HEIGHT = 72
START_MENU_SIDE_MARGIN = 42
UI_HEADER_LEFT = 28
UI_HEADER_WIDTH = WIDTH - 56
UI_SUBTITLE_LEFT = 76
UI_SUBTITLE_WIDTH = WIDTH - 152
UI_INFO_LEFT = 102
UI_INFO_WIDTH = WIDTH - 204
UI_TITLE_HEIGHT = 128
UI_SUBTITLE_HEIGHT = 94
UI_INFO_HEIGHT = 62
UI_PANEL_TOP = 290
UI_PANEL_BOTTOM_MARGIN = 170
UI_PANEL_SIDE_MARGIN = 90
CONTENT_TITLE_Y = 130
CONTENT_SUBTITLE_Y = CONTENT_TITLE_Y + 96
CONTENT_INFO_Y = CONTENT_SUBTITLE_Y + 72
BOTTOM_NAV_Y = HEIGHT - 92
BOTTOM_SIDE_NAV_Y = HEIGHT - 96
SELECTION_OPTION_WIDTH = 360
SELECTION_OPTION_HEIGHT = 84
SELECTION_OPTION_GAP = 34
SELECTION_BLOCK_START_Y = HEIGHT // 2 - 32
PAUSE_PANEL_WIDTH = 430
PAUSE_PANEL_HEIGHT = 360
PAUSE_STACK_GAP = 82
PAUSE_STACK_START_OFFSET = -44
PLAY_MENU_Y = {
    "title": MENU_TITLE_Y,
    "subtitle": MENU_SUBTITLE_Y,
    "ai_mode": MENU_FIRST_BUTTON_Y,
    "pvp": MENU_FIRST_BUTTON_Y + MENU_BUTTON_SPACING,
    "back": MENU_BACK_BUTTON_Y,
}
AI_MENU_Y = {
    "title": MENU_TITLE_Y,
    "subtitle": MENU_SUBTITLE_Y,
    "ai_start": MENU_FIRST_BUTTON_Y,
    "you_start": MENU_FIRST_BUTTON_Y + MENU_BUTTON_SPACING,
    "back": MENU_BACK_BUTTON_Y,
}
AI_DIFFICULTY_Y = {
    "title": MENU_TITLE_Y,
    "subtitle": MENU_SUBTITLE_Y,
    "easy": MENU_FIRST_BUTTON_Y,
    "medium": MENU_FIRST_BUTTON_Y + MENU_BUTTON_SPACING,
    "hard": MENU_FIRST_BUTTON_Y + MENU_BUTTON_SPACING * 2,
    "back": MENU_BACK_BUTTON_Y,
}

WIN_FLASH_INTERVAL = 0.18
WIN_FLASH_TOGGLES = 12
END_SCREEN_DELAY_MS = 2500
FADE_SPEED = 520.0
MINIMAX_CACHE_LIMIT = 80_000
MINIMAX_CACHE_TRIM_TO = 60_000


Board = list[list[int]]
RED_TOKEN: pygame.Surface | None = None
BLUE_TOKEN: pygame.Surface | None = None
TOKEN_VARIANTS: dict[tuple[str, int, int], pygame.Surface] = {}
TOKEN_SHADOWS: dict[int, pygame.Surface] = {}
TOKEN_GLOWS: dict[tuple[str, int, int], pygame.Surface] = {}
BACKGROUND_SURFACE: pygame.Surface | None = None
BOARD_PANEL_SURFACE: pygame.Surface | None = None
HOLE_SURFACE: pygame.Surface | None = None
WIN_GLOW_SURFACE: pygame.Surface | None = None
FADE_SURFACES: dict[int, pygame.Surface] = {}
FONT_CACHE: dict[tuple[object, int, bool, str], pygame.font.Font] = {}
MINIMAX_CACHE: OrderedDict[
    tuple[tuple[tuple[int, ...], ...], int, bool],
    tuple[int | None, int, str],
] = OrderedDict()
SETTINGS: dict[str, object] = {
    "volume": 0.5,
    "effects_volume": 0.7,
    "music_volume": 0.32,
    "sound_enabled": True,
    "music_enabled": True,
}
EXTRA_SAVE_SETTINGS: dict[str, object] = {}
EXTRA_PLAYER_DATA: dict[str, object] = {}
PLAYER_DATA: dict[str, object] = {"tokens": 250, "ai_score": 0}
SOUND_OK = False

DEFAULT_SETTINGS: dict[str, object] = dict(SETTINGS)
DEFAULT_PLAYER_DATA: dict[str, object] = {"tokens": 250, "ai_score": 0}




def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def save_file_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_FILE)


def serialized_player_data() -> dict[str, object]:
    return {
        "tokens": int(PLAYER_DATA.get("tokens", DEFAULT_PLAYER_DATA["tokens"])),
        "ai_score": int(PLAYER_DATA.get("ai_score", DEFAULT_PLAYER_DATA["ai_score"])),
    }


def safe_int(value: object, default: int = 0) -> int:
    """Convert arbitrary input to int without crashing on corrupted save data."""
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return default


def safe_float(value: object, default: float = 0.0) -> float:
    """Convert arbitrary input to float without crashing on corrupted save data."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def save_progress() -> None:
    music_volume = max(0.0, min(1.0, safe_float(SETTINGS.get("music_volume", DEFAULT_SETTINGS["music_volume"]), float(DEFAULT_SETTINGS["music_volume"]))))
    payload = {
        "settings": {
            **EXTRA_SAVE_SETTINGS,
            "volume": max(0.0, min(1.0, float(SETTINGS.get("volume", DEFAULT_SETTINGS["volume"])))),
            "effects_volume": max(0.0, min(1.0, float(SETTINGS.get("effects_volume", SETTINGS.get("volume", 0.5))))),
            "music_volume": music_volume,
            "sound_enabled": bool(SETTINGS.get("sound_enabled", DEFAULT_SETTINGS["sound_enabled"])),
            "music_enabled": bool(SETTINGS.get("music_enabled", True)),
        },
        "player_data": {**EXTRA_PLAYER_DATA, **serialized_player_data()},
    }
    target_path = save_file_path()
    temporary_path = target_path + ".tmp"
    try:
        with open(temporary_path, "w", encoding="utf-8") as save_handle:
            json.dump(payload, save_handle, indent=2)
            save_handle.flush()
            os.fsync(save_handle.fileno())
        os.replace(temporary_path, target_path)
    except OSError:
        try:
            os.remove(temporary_path)
        except OSError:
            pass
        return


def load_progress() -> None:
    EXTRA_SAVE_SETTINGS.clear()
    EXTRA_PLAYER_DATA.clear()
    SETTINGS.update(DEFAULT_SETTINGS)
    PLAYER_DATA.update(DEFAULT_PLAYER_DATA)

    try:
        with open(save_file_path(), "r", encoding="utf-8") as save_handle:
            payload = json.load(save_handle)
    except (OSError, ValueError, TypeError):
        return
    if not isinstance(payload, dict):
        return

    settings_data = payload.get("settings", {})
    if isinstance(settings_data, dict):
        EXTRA_SAVE_SETTINGS.update({key: value for key, value in settings_data.items() if key not in {"volume", "effects_volume", "music_volume", "sound_enabled", "music_enabled"}})
        SETTINGS["volume"] = max(0.0, min(1.0, safe_float(settings_data.get("volume", DEFAULT_SETTINGS["volume"]), float(DEFAULT_SETTINGS["volume"]))))
        SETTINGS["effects_volume"] = max(0.0, min(1.0, safe_float(settings_data.get("effects_volume", SETTINGS["volume"]), float(SETTINGS["volume"]))))
        default_music_volume = float(DEFAULT_SETTINGS["music_volume"])
        SETTINGS["music_volume"] = max(0.0, min(1.0, safe_float(settings_data.get("music_volume", default_music_volume), default_music_volume)))
        SETTINGS["sound_enabled"] = bool(settings_data.get("sound_enabled", DEFAULT_SETTINGS["sound_enabled"]))
        SETTINGS["music_enabled"] = bool(settings_data.get("music_enabled", True))

    player_data = payload.get("player_data", {})
    if not isinstance(player_data, dict):
        return
    EXTRA_PLAYER_DATA.update({key: value for key, value in player_data.items() if key not in {"tokens", "ai_score"}})

    PLAYER_DATA["tokens"] = max(0, safe_int(player_data.get("tokens", DEFAULT_PLAYER_DATA["tokens"]), int(DEFAULT_PLAYER_DATA["tokens"])))
    PLAYER_DATA["ai_score"] = max(0, safe_int(player_data.get("ai_score", DEFAULT_PLAYER_DATA["ai_score"]), int(DEFAULT_PLAYER_DATA["ai_score"])))


def reward_for_difficulty(difficulty: int | None) -> int:
    if difficulty == EASY:
        return 50
    if difficulty == MEDIUM:
        return 100
    if difficulty == HARD:
        return 500
    return 0


def draw_reward_for_difficulty(difficulty: int | None) -> int:
    return reward_for_difficulty(difficulty) // 2


def reward_preview_lines() -> list[str]:
    return [
        f"Easy -> {reward_for_difficulty(EASY)} points",
        f"Medium -> {reward_for_difficulty(MEDIUM)} points",
        f"Hard -> {reward_for_difficulty(HARD)} points",
    ]


def ai_match_points(result: str) -> int:
    if result == "win":
        return 3
    if result == "draw":
        return 1
    return 0














def token_color_for_piece(piece: int) -> tuple[int, int, int]:
    if piece == PLAYER:
        return selected_player_color()
    if piece == AI:
        return selected_ai_color()
    return (0, 200, 255)


def token_color_for_piece(piece: int) -> tuple[int, int, int]:
    return (0, 200, 255) if piece == PLAYER else (230, 52, 76) if piece == AI else (0, 200, 255)


def color_cache_key(color: tuple[int, int, int]) -> str:
    return f"{color[0]}_{color[1]}_{color[2]}"


def remember_minimax_result(
    cache_key: tuple[tuple[tuple[int, ...], ...], int, bool],
    result: tuple[int | None, int, str],
) -> None:
    """Store a transposition-table entry and trim the cache opportunistically."""
    if cache_key in MINIMAX_CACHE:
        MINIMAX_CACHE.move_to_end(cache_key)
    MINIMAX_CACHE[cache_key] = result
    while len(MINIMAX_CACHE) > MINIMAX_CACHE_LIMIT:
        MINIMAX_CACHE.popitem(last=False)


def build_token_palette(color: tuple[int, int, int]) -> dict[str, tuple[int, int, int]]:
    r, g, b = color
    outer = (max(0, int(r * 0.48)), max(0, int(g * 0.48)), max(0, int(b * 0.48)))
    rim = (max(0, int(r * 0.9)), max(0, int(g * 0.9)), max(0, int(b * 0.9)))
    center = (
        min(255, int(r * 0.7 + 76)),
        min(255, int(g * 0.7 + 76)),
        min(255, int(b * 0.7 + 76)),
    )
    highlight = (
        min(255, int(r * 0.18 + 210)),
        min(255, int(g * 0.18 + 210)),
        min(255, int(b * 0.18 + 210)),
    )
    return {
        "outer": outer,
        "rim": rim,
        "center": center,
        "highlight": highlight,
    }


def set_volume_for_sounds(sounds: dict[str, pygame.mixer.Sound | None]) -> None:
    volume = float(SETTINGS.get("effects_volume", SETTINGS.get("volume", 0.5))) if bool(SETTINGS.get("sound_enabled", True)) else 0.0
    for sound in sounds.values():
        if sound is not None:
            sound.set_volume(volume)


def update_volume_from_mouse(slider_rect: pygame.Rect, mouse_x: int) -> None:
    ratio = (mouse_x - slider_rect.left) / max(slider_rect.width, 1)
    SETTINGS["volume"] = max(0.0, min(1.0, ratio))
    save_progress()


def update_setting_volume_from_mouse(slider_rect: pygame.Rect, mouse_x: int, setting_key: str, *, persist: bool = True) -> None:
    ratio = (mouse_x - slider_rect.left) / max(slider_rect.width, 1)
    SETTINGS[setting_key] = max(0.0, min(1.0, ratio))
    if setting_key == "effects_volume":
        SETTINGS["volume"] = SETTINGS[setting_key]
    if persist:
        save_progress()




def get_next_y(start_y: int, index: int, spacing: int) -> int:
    return start_y + index * spacing


def get_centered_y(start_y: int, spacing: int, index: int) -> int:
    return start_y + index * spacing


def menu_text_positions(
    *,
    title_y: int = MENU_TITLE_Y,
    subtitle_y: int = MENU_SUBTITLE_Y,
) -> tuple[int, int]:
    return title_y, subtitle_y


def get_font(font_name: str = "default", size: int = 28, bold: bool = False) -> pygame.font.Font:
    resolved_size = max(MIN_UI_FONT_SIZE, int(size))

    if not hasattr(get_font, "_custom_font_path"):
        get_font._custom_font_path = None
        for candidate in (
            resource_path("SegoeUI.ttf"),
            resource_path("Calibri.ttf"),
            resource_path("Arial.ttf"),
            resource_path("Roboto-Regular.ttf"),
            resource_path("SegoeUI.ttf"),
            resource_path("assets/fonts/SegoeUI.ttf"),
            resource_path("assets/fonts/Calibri.ttf"),
            resource_path("assets/fonts/Arial.ttf"),
            resource_path("assets/fonts/Roboto-Regular.ttf"),
            resource_path("fonts/SegoeUI.ttf"),
            resource_path("fonts/Calibri.ttf"),
            resource_path("fonts/Arial.ttf"),
            resource_path("fonts/Roboto-Regular.ttf"),
        ):
            if os.path.exists(candidate):
                get_font._custom_font_path = candidate
                break

    preferred_name: str | list[str] = font_name
    if font_name == "default":
        preferred_name = ["segoeui", "calibri", "arial"]

    resolved_bold = bool(bold)
    cache_font_name = tuple(preferred_name) if isinstance(preferred_name, list) else preferred_name
    cache_key = (cache_font_name, resolved_size, resolved_bold, str(get_font._custom_font_path))
    if cache_key not in FONT_CACHE:
        if font_name == "default" and get_font._custom_font_path is not None:
            font_obj = pygame.font.Font(get_font._custom_font_path, resolved_size)
            font_obj.set_bold(resolved_bold)
            FONT_CACHE[cache_key] = font_obj
        else:
            FONT_CACHE[cache_key] = pygame.font.SysFont(preferred_name, resolved_size, bold=resolved_bold)
    return FONT_CACHE[cache_key]


def truncate_text(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def apply_word_spacing(text: str, extra_spaces: int = 1) -> str:
    if extra_spaces <= 0 or " " not in text:
        return text
    spacer = " " * (extra_spaces + 1)
    return "\n".join(spacer.join(line.split(" ")) for line in text.splitlines())


def _split_long_word(word: str, font: pygame.font.Font, max_width: int) -> list[str]:
    if not word:
        return [""]
    pieces: list[str] = []
    current = ""
    for char in word:
        candidate = current + char
        if current and font.size(candidate)[0] > max_width:
            pieces.append(current)
            current = char
        else:
            current = candidate
    if current:
        pieces.append(current)
    return pieces


def _wrap_text_to_width(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    max_width = max(1, int(max_width))
    wrapped_lines: list[str] = []
    for paragraph in text.splitlines() or [text]:
        words = paragraph.split()
        if not words:
            wrapped_lines.append("")
            continue

        current_line = ""
        for word in words:
            if font.size(word)[0] > max_width:
                if current_line:
                    wrapped_lines.append(current_line)
                    current_line = ""
                wrapped_lines.extend(_split_long_word(word, font, max_width))
                continue

            candidate = f"{current_line} {word}".strip()
            if not current_line or font.size(candidate)[0] <= max_width:
                current_line = candidate
            else:
                wrapped_lines.append(current_line)
                current_line = word

        if current_line:
            wrapped_lines.append(current_line)

    return wrapped_lines or [""]


def _ellipsize_text_to_width(text: str, font: pygame.font.Font, max_width: int) -> str:
    if font.size(text)[0] <= max_width:
        return text

    ellipsis = "..."
    if font.size(ellipsis)[0] > max_width:
        return ""

    trimmed = text.rstrip()
    while trimmed:
        candidate = trimmed + ellipsis
        if font.size(candidate)[0] <= max_width:
            return candidate
        trimmed = trimmed[:-1].rstrip()
    return ellipsis


def _fit_text_lines(
    text: str,
    inner_rect: pygame.Rect,
    *,
    max_size: int,
    min_size: int,
    bold: bool,
    allow_wrap: bool,
    line_spacing: int,
) -> tuple[pygame.font.Font, list[str]]:
    fitted_font = get_font("default", min_size, bold=bold)
    fitted_lines = _wrap_text_to_width(text, fitted_font, inner_rect.width) if allow_wrap else [text]

    for size in range(max_size, min_size - 1, -1):
        candidate_font = get_font("default", size, bold=bold)
        candidate_lines = _wrap_text_to_width(text, candidate_font, inner_rect.width) if allow_wrap else [text]
        if any(candidate_font.size(line)[0] > inner_rect.width for line in candidate_lines):
            continue

        line_height = candidate_font.get_linesize()
        total_height = len(candidate_lines) * line_height + max(0, len(candidate_lines) - 1) * line_spacing
        fitted_font = candidate_font
        fitted_lines = candidate_lines
        if total_height <= inner_rect.height:
            return fitted_font, fitted_lines

    if not allow_wrap:
        return fitted_font, [_ellipsize_text_to_width(text, fitted_font, inner_rect.width)]

    fitted_lines = _wrap_text_to_width(text, fitted_font, inner_rect.width)
    line_height = fitted_font.get_linesize()
    max_lines = max(1, (inner_rect.height + line_spacing) // max(1, line_height + line_spacing))
    if len(fitted_lines) <= max_lines:
        return fitted_font, fitted_lines

    visible_lines = fitted_lines[:max_lines]
    if visible_lines:
        visible_lines[-1] = _ellipsize_text_to_width(visible_lines[-1], fitted_font, inner_rect.width)
    return fitted_font, visible_lines


def draw_text_box(
    screen: pygame.Surface,
    text: str,
    rect: pygame.Rect,
    color: tuple[int, int, int] = TEXT_COLOR,
    *,
    max_size: int = 40,
    min_size: int = 16,
    bold: bool = False,
    allow_wrap: bool = True,
    padding: int = 16,
    line_spacing: int = LINE_SPACING,
    shadow_offset: tuple[int, int] = (2, 2),
    shadow_color: tuple[int, int, int] = (0, 0, 0),
    gradient: tuple[tuple[int, int, int], tuple[int, int, int]] | None = None,
    outline_color: tuple[int, int, int] = (0, 0, 0),
    is_title: bool = False,
    word_spacing: int = 0,
    align: str = "center",
    vertical_align: str = "center",
) -> pygame.Rect:
    if not hasattr(draw_text_box, "_surface_cache"):
        draw_text_box._font_cache = {}
        draw_text_box._surface_cache = {}
    surface_cache: dict[tuple[object, ...], pygame.Surface] = draw_text_box._surface_cache

    inner_rect = pygame.Rect(
        rect.left + padding,
        rect.top + padding,
        max(10, rect.width - padding * 2),
        max(10, rect.height - padding * 2),
    )

    min_size = max(MIN_UI_FONT_SIZE, min_size)
    display_text = apply_word_spacing(text, word_spacing)
    resolved_bold = bool(bold) and is_title
    fitted_font, lines = _fit_text_lines(
        display_text,
        inner_rect,
        max_size=max_size,
        min_size=min_size,
        bold=resolved_bold,
        allow_wrap=allow_wrap,
        line_spacing=line_spacing,
    )

    line_height = fitted_font.get_linesize()
    total_height = len(lines) * line_height + max(0, len(lines) - 1) * line_spacing
    if vertical_align == "top":
        start_y = inner_rect.top
    elif vertical_align == "bottom":
        start_y = inner_rect.bottom - total_height
    else:
        start_y = inner_rect.centery - total_height // 2
    start_y = max(inner_rect.top, min(start_y, inner_rect.bottom - total_height))
    union_rect: pygame.Rect | None = None
    title_scale = 2 if is_title and max_size >= 72 else 1 if is_title else 0
    outline_width = 2 if title_scale == 2 else 1 if is_title else 1
    glow_alpha = 52 if title_scale == 2 else 26 if is_title else 0
    glow_padding = 10 if title_scale == 2 else 6 if is_title else 3
    glow_color = TITLE_GLOW_COLOR if gradient is not None else color
    shadow_rgba = (*shadow_color, 72 if title_scale == 2 else 58 if is_title else 48)
    outline_rgb = outline_color

    for index, line in enumerate(lines):
        text_width, text_height = fitted_font.size(line)
        base_key = (
            line,
            fitted_font.get_height(),
            resolved_bold,
            color,
            gradient,
            outline_rgb,
            glow_color,
            outline_width,
            glow_alpha,
            glow_padding,
        )
        if base_key in surface_cache:
            composed_surface = surface_cache[base_key]
        else:
            if gradient is None:
                text_surface = fitted_font.render(line, True, color).convert_alpha()
            else:
                text_surface = fitted_font.render(line, True, (255, 255, 255)).convert_alpha()
                width, height = text_surface.get_size()
                gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                for y in range(height):
                    ratio = y / max(height - 1, 1)
                    r = int(gradient[0][0] * (1 - ratio) + gradient[1][0] * ratio)
                    g = int(gradient[0][1] * (1 - ratio) + gradient[1][1] * ratio)
                    b = int(gradient[0][2] * (1 - ratio) + gradient[1][2] * ratio)
                    pygame.draw.line(gradient_surface, (r, g, b), (0, y), (width, y))
                text_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_MULT)

            width, height = text_surface.get_size()
            composed_surface = pygame.Surface(
                (width + (glow_padding + outline_width) * 2, height + (glow_padding + outline_width) * 2),
                pygame.SRCALPHA,
            )
            center_offset = glow_padding + outline_width

            if glow_alpha > 0:
                glow_surface = fitted_font.render(line, True, glow_color).convert_alpha()
                glow_range = 2 if title_scale == 2 else 1
                glow_distance_limit = 5 if title_scale == 2 else 2
                for dx in range(-glow_range, glow_range + 1):
                    for dy in range(-glow_range, glow_range + 1):
                        if dx == 0 and dy == 0:
                            continue
                        if dx * dx + dy * dy > glow_distance_limit:
                            continue
                        glow_copy = glow_surface.copy()
                        glow_copy.fill((255, 255, 255, glow_alpha), special_flags=pygame.BLEND_RGBA_MULT)
                        composed_surface.blit(glow_copy, (center_offset + dx, center_offset + dy))

            outline_surface = fitted_font.render(line, True, outline_rgb).convert_alpha()
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx == 0 and dy == 0:
                        continue
                    if dx * dx + dy * dy > outline_width * outline_width + 1:
                        continue
                    composed_surface.blit(outline_surface, (center_offset + dx, center_offset + dy))

            composed_surface.blit(text_surface, (center_offset, center_offset))
            if is_title:
                composed_surface.blit(text_surface, (center_offset + 1, center_offset))
            if len(surface_cache) > 256:
                surface_cache.clear()
            surface_cache[base_key] = composed_surface

        shadow_surface = fitted_font.render(line, True, shadow_color).convert_alpha()
        shadow_surface.fill(shadow_rgba, special_flags=pygame.BLEND_RGBA_MULT)
        line_rect = pygame.Rect(0, 0, text_width, text_height)
        if align == "left":
            line_rect.midleft = (
                inner_rect.left,
                start_y + line_height // 2 + index * (line_height + line_spacing),
            )
        elif align == "right":
            line_rect.midright = (
                inner_rect.right,
                start_y + line_height // 2 + index * (line_height + line_spacing),
            )
        else:
            line_rect.center = (
                inner_rect.centerx,
                start_y + line_height // 2 + index * (line_height + line_spacing),
            )
        line_rect.clamp_ip(inner_rect)
        shadow_rect = line_rect.move(*shadow_offset)
        screen.blit(shadow_surface, shadow_rect)
        composed_rect = composed_surface.get_rect(center=line_rect.center)
        screen.blit(composed_surface, composed_rect)
        union_rect = line_rect if union_rect is None else union_rect.union(line_rect)

    return union_rect if union_rect is not None else inner_rect.copy()


def draw_text(
    screen: pygame.Surface,
    text: str,
    x: int,
    y: int,
    size: int,
    *,
    is_title: bool = False,
    color: tuple[int, int, int] = TEXT_COLOR,
    gradient: tuple[tuple[int, int, int], tuple[int, int, int]] | None = None,
    width: int | None = None,
    center: bool = True,
    align: str = "center",
) -> pygame.Rect:
    text_width = width if width is not None else min(WIDTH - 80, max(220, int(WIDTH * 0.72)))
    rect_height = max(size + (50 if is_title else 30), int(size * (2.2 if is_title else 1.7)))
    rect = pygame.Rect(0, 0, text_width, rect_height)
    rect.midtop = (x, y) if center else (x + rect.width // 2, y)
    return draw_text_box(
        screen,
        text,
        rect,
        color=color,
        max_size=size,
        min_size=max(MIN_UI_FONT_SIZE, size - (18 if is_title else 6)),
        padding=16 if is_title else 12,
        line_spacing=TEXT_LINE_GAP if is_title else LINE_SPACING + 4,
        shadow_offset=(2, 3) if is_title else (1, 2),
        gradient=gradient,
        is_title=is_title,
        allow_wrap=True,
        word_spacing=1,
        align=align,
        vertical_align="top",
    )


def draw_text_list(
    screen: pygame.Surface,
    texts: list[dict[str, object]],
    start_y: int,
    *,
    spacing: int = TEXT_LIST_SPACING,
    center_x: int | None = None,
) -> list[pygame.Rect]:
    resolved_center_x = WIDTH // 2 if center_x is None else center_x
    rects: list[pygame.Rect] = []
    for index, entry in enumerate(texts):
        rects.append(
            draw_text(
                screen,
                str(entry["text"]),
                resolved_center_x,
                start_y + index * spacing,
                int(entry["size"]),
                is_title=bool(entry.get("is_title", False)),
                color=entry.get("color", TEXT_COLOR),
                gradient=entry.get("gradient"),
                width=entry.get("width"),
            )
        )
    return rects


def board_rect() -> pygame.Rect:
    return pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT)


def column_from_x(x: int) -> int | None:
    relative_x = x - BOARD_LEFT
    if relative_x < 0:
        return None
    col = relative_x // CELL_SIZE
    if col < 0 or col >= COLUMNS:
        return None
    return int(col)


def board_key(board: Board) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(row) for row in board)


def create_board() -> Board:
    return [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board: Board) -> None:
    print()
    for row in board:
        print("| " + " ".join(symbol(cell) for cell in row) + " |")
    print("  " + " ".join(str(col) for col in range(COLUMNS)))
    print()


def symbol(piece: int) -> str:
    if piece == PLAYER:
        return "X"
    if piece == AI:
        return "O"
    return "."


def is_valid_location(board: Board, col: int) -> bool:
    return 0 <= col < COLUMNS and board[0][col] == EMPTY


def get_valid_locations(board: Board) -> list[int]:
    return [col for col in range(COLUMNS) if is_valid_location(board, col)]


def get_next_open_row(board: Board, col: int) -> int | None:
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None


def drop_piece(board: Board, row: int, col: int, piece: int) -> None:
    board[row][col] = piece


def board_pixel_position(row: int, col: int) -> tuple[int, int]:
    x = BOARD_LEFT + col * CELL_SIZE + CELL_SIZE // 2
    y = BOARD_TOP + row * CELL_SIZE + CELL_SIZE // 2
    return x, y


def winning_move(board: Board, piece: int) -> bool:
    return get_winning_cells(board, piece) is not None


def is_winning_drop(board: Board, row: int, col: int, piece: int) -> bool:
    """Check only lines through the newly placed token (constant-size work)."""
    for row_step, col_step in ((0, 1), (1, 0), (1, 1), (1, -1)):
        count = 1
        for sign in (-1, 1):
            r = row + row_step * sign
            c = col + col_step * sign
            while 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == piece:
                count += 1
                r += row_step * sign
                c += col_step * sign
        if count >= WINDOW_LENGTH:
            return True
    return False


def get_winning_cells(board: Board, piece: int) -> list[tuple[int, int]] | None:
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            cells = [(row, col + offset) for offset in range(WINDOW_LENGTH)]
            if all(board[r][c] == piece for r, c in cells):
                return cells

    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            cells = [(row + offset, col) for offset in range(WINDOW_LENGTH)]
            if all(board[r][c] == piece for r, c in cells):
                return cells

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            cells = [(row + offset, col + offset) for offset in range(WINDOW_LENGTH)]
            if all(board[r][c] == piece for r, c in cells):
                return cells

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            cells = [(row - offset, col + offset) for offset in range(WINDOW_LENGTH)]
            if all(board[r][c] == piece for r, c in cells):
                return cells

    return None


def is_terminal_node(board: Board) -> bool:
    return (
        winning_move(board, PLAYER)
        or winning_move(board, AI)
        or not get_valid_locations(board)
    )


def evaluate_window(window: Iterable[int], piece: int) -> int:
    values = list(window)
    opponent = PLAYER if piece == AI else AI

    piece_count = values.count(piece)
    empty_count = values.count(EMPTY)
    opponent_count = values.count(opponent)

    score = 0

    if piece_count == 4:
        score += 100_000
    elif piece_count == 3 and empty_count == 1:
        score += 120
    elif piece_count == 2 and empty_count == 2:
        score += 12

    if opponent_count == 3 and empty_count == 1:
        score -= 140
    elif opponent_count == 2 and empty_count == 2:
        score -= 10

    return score


def score_position(board: Board, piece: int) -> int:
    opponent = PLAYER if piece == AI else AI
    score = 0

    position_weights = (
        (3, 4, 5, 7, 5, 4, 3),
        (4, 6, 8, 10, 8, 6, 4),
        (5, 8, 11, 13, 11, 8, 5),
        (5, 8, 11, 13, 11, 8, 5),
        (4, 6, 8, 10, 8, 6, 4),
        (3, 4, 5, 7, 5, 4, 3),
    )

    def evaluate_window_strong(window: list[int]) -> int:
        piece_count = window.count(piece)
        opponent_count = window.count(opponent)
        empty_count = window.count(EMPTY)

        if piece_count > 0 and opponent_count > 0:
            return 0

        window_score = 0

        if piece_count == 4:
            window_score += 1_000_000
        elif piece_count == 3 and empty_count == 1:
            window_score += 900
        elif piece_count == 2 and empty_count == 2:
            window_score += 90
        elif piece_count == 1 and empty_count == 3:
            window_score += 8

        if opponent_count == 4:
            window_score -= 1_000_000
        elif opponent_count == 3 and empty_count == 1:
            window_score -= 1_200
        elif opponent_count == 2 and empty_count == 2:
            window_score -= 110
        elif opponent_count == 1 and empty_count == 3:
            window_score -= 6

        return window_score

    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == piece:
                score += position_weights[row][col]
            elif board[row][col] == opponent:
                score -= position_weights[row][col]

    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            score += evaluate_window_strong(board[row][col:col + WINDOW_LENGTH])

    for row in range(ROWS - 3):
        for col in range(COLUMNS):
            window = [board[row + offset][col] for offset in range(WINDOW_LENGTH)]
            score += evaluate_window_strong(window)

    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            window = [board[row + offset][col + offset] for offset in range(WINDOW_LENGTH)]
            score += evaluate_window_strong(window)

    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            window = [board[row - offset][col + offset] for offset in range(WINDOW_LENGTH)]
            score += evaluate_window_strong(window)

    # Reward positions that create multiple immediate winning threats without
    # copying the board or rescanning every four-cell window for each column.
    immediate_wins = 0
    opponent_immediate_wins = 0
    for col in get_valid_locations(board):
        row = get_next_open_row(board, col)
        if row is None:
            continue
        board[row][col] = piece
        if is_winning_drop(board, row, col, piece):
            immediate_wins += 1
        board[row][col] = opponent
        if is_winning_drop(board, row, col, opponent):
            opponent_immediate_wins += 1
        board[row][col] = EMPTY

    if immediate_wins >= 2:
        score += 25_000
    elif immediate_wins == 1:
        score += 3_000

    if opponent_immediate_wins >= 2:
        score -= 30_000
    elif opponent_immediate_wins == 1:
        score -= 4_000

    return score


def copy_board(board: Board) -> Board:
    return [row[:] for row in board]


def order_moves(board: Board, valid_locations: list[int], piece: int) -> list[int]:
    """Order immediate wins, forced blocks, then central moves for alpha-beta."""
    center = COLUMNS // 2
    opponent = PLAYER if piece == AI else AI
    opponent_threats: set[int] = set()
    for col in valid_locations:
        row = get_next_open_row(board, col)
        if row is None:
            continue
        board[row][col] = opponent
        if is_winning_drop(board, row, col, opponent):
            opponent_threats.add(col)
        board[row][col] = EMPTY

    ranked_moves: list[tuple[int, int, int, int]] = []

    for col in valid_locations:
        row = get_next_open_row(board, col)
        if row is None:
            continue

        board[row][col] = piece
        is_win = is_winning_drop(board, row, col, piece)
        board[row][col] = EMPTY
        blocks_threat = col in opponent_threats
        priority = 1_000_000 if is_win else 10_000 if blocks_threat else 0
        ranked_moves.append((priority, -abs(col - center), -row, col))

    ranked_moves.sort(reverse=True)
    ordered = [col for _, _, _, col in ranked_moves]
    return ordered if ordered else valid_locations[:]


class _SearchTimeout(Exception):
    """Abort an incomplete iterative-deepening pass without using its result."""


def minimax(
    board: Board,
    depth: int,
    alpha: float,
    beta: float,
    maximizing_player: bool,
    deadline: float | None = None,
    last_move: tuple[int, int, int] | None = None,
) -> tuple[int | None, int]:
    if deadline is not None and time.perf_counter() >= deadline:
        raise _SearchTimeout

    alpha_original = alpha
    beta_original = beta
    winner = 0
    if last_move is not None:
        last_row, last_col, last_piece = last_move
        if is_winning_drop(board, last_row, last_col, last_piece):
            winner = last_piece
    else:
        if winning_move(board, AI):
            winner = AI
        elif winning_move(board, PLAYER):
            winner = PLAYER
    cache_key = (board_key(board), depth, maximizing_player)
    cached = MINIMAX_CACHE.get(cache_key)
    if cached is not None:
        MINIMAX_CACHE.move_to_end(cache_key)
        cached_col, cached_score, cached_bound = cached
        if cached_bound == "exact":
            return cached_col, cached_score
        if cached_bound == "lower":
            alpha = max(alpha, cached_score)
        elif cached_bound == "upper":
            beta = min(beta, cached_score)
        if alpha >= beta:
            return cached_col, cached_score

    valid_locations = get_valid_locations(board)
    terminal = bool(winner) or not valid_locations

    if not valid_locations:
        result = (None, 0 if terminal else score_position(board, AI))
        remember_minimax_result(cache_key, (result[0], result[1], "exact"))
        return result

    if depth == 0 or terminal:
        if winner == AI:
            result = (None, 1_000_000_000 + depth)
        elif winner == PLAYER:
            result = (None, -1_000_000_000 - depth)
        elif terminal:
            result = (None, 0)
        else:
            result = (None, score_position(board, AI))
        remember_minimax_result(cache_key, (result[0], result[1], "exact"))
        return result

    if maximizing_player:
        value = -math.inf
        best_col = valid_locations[0]
        for col in order_moves(board, valid_locations, AI):
            row = get_next_open_row(board, col)
            if row is None:
                continue
            temp_board = copy_board(board)
            drop_piece(temp_board, row, col, AI)
            _, new_score = minimax(temp_board, depth - 1, alpha, beta, False, deadline, (row, col, AI))
            if new_score > value:
                value = new_score
                best_col = col
                if new_score >= 1_000_000_000:
                    break
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        result = (best_col, int(value))
        bound = "exact"
        if result[1] <= alpha_original:
            bound = "upper"
        elif result[1] >= beta_original:
            bound = "lower"
        remember_minimax_result(cache_key, (result[0], result[1], bound))
        return result

    value = math.inf
    best_col = valid_locations[0]
    for col in order_moves(board, valid_locations, PLAYER):
        row = get_next_open_row(board, col)
        if row is None:
            continue
        temp_board = copy_board(board)
        drop_piece(temp_board, row, col, PLAYER)
        _, new_score = minimax(temp_board, depth - 1, alpha, beta, True, deadline, (row, col, PLAYER))
        if new_score < value:
            value = new_score
            best_col = col
            if new_score <= -1_000_000_000:
                break
        beta = min(beta, value)
        if alpha >= beta:
            break
    result = (best_col, int(value))
    bound = "exact"
    if result[1] <= alpha_original:
        bound = "upper"
    elif result[1] >= beta_original:
        bound = "lower"
    remember_minimax_result(cache_key, (result[0], result[1], bound))
    return result


def choose_ai_move(board: Board, depth: int = DEFAULT_DEPTH, time_limit: float | None = None) -> int:
    valid_locations = get_valid_locations(board)
    if not valid_locations:
        raise ValueError("No valid moves available.")

    for col in valid_locations:
        row = get_next_open_row(board, col)
        if row is None:
            continue
        board[row][col] = AI
        is_win = is_winning_drop(board, row, col, AI)
        board[row][col] = EMPTY
        if is_win:
            choose_ai_move.last_completed_depth = depth
            choose_ai_move.requested_depth = depth
            return col

    for col in valid_locations:
        row = get_next_open_row(board, col)
        if row is None:
            continue
        board[row][col] = PLAYER
        is_win = is_winning_drop(board, row, col, PLAYER)
        board[row][col] = EMPTY
        if is_win:
            choose_ai_move.last_completed_depth = depth
            choose_ai_move.requested_depth = depth
            return col

    while len(MINIMAX_CACHE) > MINIMAX_CACHE_TRIM_TO:
        MINIMAX_CACHE.popitem(last=False)

    fallback_moves = order_moves(board, valid_locations, AI)
    best_col = fallback_moves[0] if fallback_moves else valid_locations[0]
    deadline = time.perf_counter() + time_limit if time_limit is not None else None
    completed_depth = 0
    for search_depth in range(1, max(1, depth) + 1):
        try:
            candidate, _ = minimax(board, search_depth, -math.inf, math.inf, True, deadline)
        except _SearchTimeout:
            break
        if candidate in valid_locations:
            best_col = candidate
            completed_depth = search_depth
    choose_ai_move.last_completed_depth = completed_depth
    choose_ai_move.requested_depth = max(1, depth)
    return best_col


choose_ai_move.last_completed_depth = 0
choose_ai_move.requested_depth = DEFAULT_DEPTH


def difficulty_name(difficulty: int | None) -> str:
    if difficulty == EASY:
        return "Easy"
    if difficulty == MEDIUM:
        return "Medium"
    if difficulty == HARD:
        return "Hard"
    return ""


def get_ai_move(board: Board, difficulty: int | None) -> int:
    """Return a valid AI column for the requested difficulty."""
    valid_locations = get_valid_locations(board)
    if not valid_locations:
        raise ValueError("No valid moves available.")

    depth = AI_SEARCH_DEPTHS.get(difficulty, AI_SEARCH_DEPTHS[HARD])
    time_limit = AI_SEARCH_TIME_LIMITS.get(difficulty, AI_SEARCH_TIME_LIMITS[HARD])

    move = choose_ai_move(board, depth, time_limit=time_limit)
    return move if move in valid_locations else order_moves(board, valid_locations, AI)[0]


def board_full(board: Board) -> bool:
    return not get_valid_locations(board)


def piece_color(piece: int) -> tuple[int, int, int, int]:
    if piece == PLAYER:
        return RUBY_RED
    if piece == AI:
        return CYAN_BLUE
    return HOLE_COLOR + (200,)


def mode_name(mode: int) -> str:
    if mode == MODE_AI_FIRST:
        return "AI Start"
    if mode == MODE_AI_SECOND:
        return "You Start"
    return "2 Players"


def show_difficulty(mode: int, difficulty: int | None) -> str:
    if mode == MODE_PVP or difficulty is None:
        return mode_name(mode)
    return f"{mode_name(mode)} - {difficulty_name(difficulty)}"


def next_turn(turn: int) -> int:
    return AI if turn == PLAYER else PLAYER


def status_message_for_turn(mode: int, turn: int) -> str:
    if mode == MODE_PVP:
        return f"Player {turn}'s turn"
    if turn == PLAYER:
        return "Your turn"
    return "AI is thinking..."


def ask_player_move(board: Board) -> int:
    valid_locations = get_valid_locations(board)
    while True:
        try:
            col = int(input(f"Choose a column {valid_locations}: ").strip())
        except ValueError:
            print("Please enter a number.")
            continue

        if col in valid_locations:
            return col
        print("That column is not available.")


def play_game(depth: int = DEFAULT_DEPTH) -> None:
    board = create_board()
    turn = PLAYER

    print("Gravity 4")
    print("You are X. The AI is O.")
    print(f"Search depth: {depth}")

    while True:
        print_board(board)

        if turn == PLAYER:
            col = ask_player_move(board)
            row = get_next_open_row(board, col)
            if row is None:
                continue
            drop_piece(board, row, col, PLAYER)

            if winning_move(board, PLAYER):
                print_board(board)
                print("You win.")
                return
            turn = AI
        else:
            col = choose_ai_move(board, depth)
            row = get_next_open_row(board, col)
            if row is None:
                print("AI could not find a valid move.")
                return

            drop_piece(board, row, col, AI)
            print(f"AI plays column {col}.")

            if winning_move(board, AI):
                print_board(board)
                print("AI wins.")
                return
            turn = PLAYER

        if not get_valid_locations(board):
            print_board(board)
            print("Draw.")
            return


def draw_board(screen: pygame.Surface, board: Board, font: pygame.font.Font, message: str = "") -> None:
    draw_background(screen)
    draw_status_panel(screen, font, message)
    draw_board_panel(screen)

    board_rect = pygame.Rect(
        BOARD_LEFT,
        BOARD_TOP,
        BOARD_WIDTH,
        BOARD_HEIGHT,
    )
    screen.set_clip(board_rect)
    for row in range(ROWS):
        for col in range(COLUMNS):
            x, y = board_pixel_position(row, col)
            draw_hole(screen, x, y)
            if board[row][col] != EMPTY:
                draw_disc(screen, x, y, board[row][col])
    screen.set_clip(None)


def draw_background(screen: pygame.Surface) -> None:
    global BACKGROUND_SURFACE
    if BACKGROUND_SURFACE is None:
        BACKGROUND_SURFACE = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(HEIGHT):
            ratio = y / max(HEIGHT - 1, 1)
            color = (
                int(12 * (1 - ratio) + 62 * ratio),
                int(22 * (1 - ratio) + 92 * ratio),
                int(42 * (1 - ratio) + 138 * ratio),
            )
            pygame.draw.line(BACKGROUND_SURFACE, color, (0, y), (WIDTH, y))

        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (100, 180, 255, 34), (WIDTH // 2 - 260, 26, 520, 190))
        pygame.draw.ellipse(glow, (50, 210, 255, 16), (WIDTH // 2 - 320, HEIGHT // 2 - 140, 640, 260))
        pygame.draw.ellipse(glow, (255, 255, 255, 10), (WIDTH // 2 - 180, 10, 360, 100))
        BACKGROUND_SURFACE.blit(glow, (0, 0))

    screen.blit(BACKGROUND_SURFACE, (0, 0))


def draw_status_panel(screen: pygame.Surface, font: pygame.font.Font, message: str) -> None:
    panel_rect = pygame.Rect(18, 16, WIDTH - 36, TOP_BAR_HEIGHT - 30)
    shadow_rect = panel_rect.move(0, 6)
    pygame.draw.rect(screen, PANEL_SHADOW, shadow_rect, border_radius=24)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=24)
    pygame.draw.rect(screen, (56, 76, 106), panel_rect, width=2, border_radius=24)

    if message:
        message_rect = pygame.Rect(panel_rect.left + 10, panel_rect.top + 2, panel_rect.width - 20, panel_rect.height - 4)
        draw_text_box(
            screen,
            message,
            message_rect,
            color=TEXT_COLOR,
            max_size=max(18, font.get_height()),
            min_size=14,
            allow_wrap=True,
            padding=14,
            line_spacing=LINE_SPACING + 4,
            align="left",
        )


def draw_board_panel(screen: pygame.Surface) -> None:
    global BOARD_PANEL_SURFACE
    board_rect = pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_WIDTH, BOARD_HEIGHT)
    shadow_rect = board_rect.move(0, 10)
    pygame.draw.rect(screen, PANEL_SHADOW, shadow_rect, border_radius=34)

    if BOARD_PANEL_SURFACE is None:
        panel_surface = pygame.Surface((board_rect.width, board_rect.height), pygame.SRCALPHA)
        for y in range(board_rect.height):
            blend = y / max(board_rect.height - 1, 1)
            color = tuple(
                int(BOARD_TOP_COLOR[i] * (1 - blend) + BOARD_BOTTOM_COLOR[i] * blend)
                for i in range(3)
            )
            pygame.draw.line(panel_surface, color, (0, y), (board_rect.width, y))
        glow = pygame.Surface((board_rect.width + 20, board_rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow, (92, 176, 255, 20), glow.get_rect().inflate(-12, -12), border_radius=42)
        panel_surface.blit(glow, (-10, -10))
        pygame.draw.rect(panel_surface, (255, 255, 255, 32), (0, 0, board_rect.width, 20), border_radius=34)
        pygame.draw.rect(panel_surface, (255, 255, 255, 18), panel_surface.get_rect(), border_radius=34)
        pygame.draw.rect(panel_surface, (120, 180, 255), panel_surface.get_rect(), 3, border_radius=34)
        panel_mask = pygame.Surface((board_rect.width, board_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_mask, (255, 255, 255, 255), panel_mask.get_rect(), border_radius=34)
        panel_surface.blit(panel_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        BOARD_PANEL_SURFACE = panel_surface
    screen.blit(BOARD_PANEL_SURFACE, board_rect.topleft)


def draw_hole(screen: pygame.Surface, x: int, y: int) -> None:
    global HOLE_SURFACE
    if HOLE_SURFACE is None:
        HOLE_SURFACE = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(HOLE_SURFACE, (0, 0, 0, 52), (CELL_SIZE // 2, CELL_SIZE // 2 + 3), HOLE_RADIUS + 4)
        pygame.draw.circle(HOLE_SURFACE, (14, 18, 28), (CELL_SIZE // 2, CELL_SIZE // 2), HOLE_RADIUS + 2)
        pygame.draw.circle(HOLE_SURFACE, (28, 38, 58), (CELL_SIZE // 2, CELL_SIZE // 2), HOLE_RADIUS - 2)
        pygame.draw.circle(HOLE_SURFACE, (72, 98, 146), (CELL_SIZE // 2 - 5, CELL_SIZE // 2 - 5), max(4, HOLE_RADIUS - 12))
    screen.blit(HOLE_SURFACE, (x - CELL_SIZE // 2, y - CELL_SIZE // 2))


def draw_piece(
    screen: pygame.Surface,
    x: int,
    y: int,
    color: tuple[int, int, int, int],
    radius: int,
) -> None:
    circle_surf = pygame.Surface((radius * 2 + 20, radius * 2 + 20), pygame.SRCALPHA)
    center = (circle_surf.get_width() // 2, circle_surf.get_height() // 2)
    pygame.draw.circle(circle_surf, color, center, radius)
    screen.blit(circle_surf, (x - center[0], y - center[1]))


def generate_token_surface(color: tuple[int, int, int], size: int) -> pygame.Surface:
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    radius = size // 2 - 6
    palette = build_token_palette(color)
    outer_color, rim_color, center_color = palette["outer"], palette["rim"], palette["center"]
    for r in range(radius + 2, radius - 5, -1):
        blend = (radius + 2 - r) / 7
        shade = tuple(int(outer_color[i] * (1 - blend) + rim_color[i] * blend) for i in range(3))
        pygame.draw.circle(surface, (*shade, 255), (cx, cy), r)
    inner_radius = radius - 8
    for r in range(inner_radius, 0, -1):
        blend = 1.0 - r / max(inner_radius, 1)
        shade = tuple(int(rim_color[i] * (1 - blend) + center_color[i] * blend) for i in range(3))
        pygame.draw.circle(surface, (*shade, 220), (cx, cy), r)
    pygame.draw.circle(surface, (*outer_color, 58), (cx, cy), max(2, radius - 10), width=3)
    return surface


def get_token_glow(color: tuple[int, int, int], size: int, alpha: int) -> pygame.Surface:
    quantized_alpha = max(0, min(255, (alpha // 8) * 8))
    key = (color_cache_key(color), size, quantized_alpha)
    cached = TOKEN_GLOWS.get(key)
    if cached is not None:
        return cached
    glow = pygame.Surface((size + 30, size + 30), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, (*color, quantized_alpha), glow.get_rect().inflate(-18, -18))
    if len(TOKEN_GLOWS) > 128:
        TOKEN_GLOWS.clear()
    TOKEN_GLOWS[key] = glow
    return glow




def get_token_variant(piece: int, scale: float = 1.0, alpha: int = 255) -> pygame.Surface | None:
    target_size = max(12, int(TOKEN_SIZE * scale))
    color = token_color_for_piece(piece)
    cache_key = (color_cache_key(color), target_size, alpha)
    if cache_key in TOKEN_VARIANTS:
        return TOKEN_VARIANTS[cache_key]
    token_img = get_token_image(piece) or generate_token_surface(color, TOKEN_SIZE)
    variant = pygame.transform.smoothscale(token_img, (target_size, target_size)) if token_img.get_size() != (target_size, target_size) else token_img.copy()
    if alpha != 255:
        variant.set_alpha(alpha)
    TOKEN_VARIANTS[cache_key] = variant
    return variant


def get_token_shadow(size: int) -> pygame.Surface:
    if size in TOKEN_SHADOWS:
        return TOKEN_SHADOWS[size]

    shadow = pygame.Surface((size + 24, size // 2 + 20), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 78), shadow.get_rect().inflate(-10, -10))
    TOKEN_SHADOWS[size] = shadow
    return shadow


def load_token_image(filename: str) -> pygame.Surface | None:
    path = resource_path(filename)
    if not os.path.exists(path):
        return None
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error:
        return None
    return pygame.transform.smoothscale(image, (TOKEN_SIZE, TOKEN_SIZE))


def get_token_image(piece: int) -> pygame.Surface | None:
    return BLUE_TOKEN if piece == PLAYER else RED_TOKEN if piece == AI else None


def draw_piece_image(
    screen: pygame.Surface,
    x: int,
    y: int,
    piece: int,
    scale: float = 1.0,
    glow_alpha: int = 0,
) -> bool:
    token_alpha = 220 if glow_alpha > 0 else 255
    draw_surface = get_token_variant(piece, scale=scale, alpha=token_alpha)
    if draw_surface is None:
        return False

    w = draw_surface.get_width()
    h = draw_surface.get_height()

    shadow = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 66), shadow.get_rect())
    shadow = pygame.transform.smoothscale(shadow, (w + 10, h // 2))
    shadow_rect = shadow.get_rect(center=(x, y + h // 3))
    screen.blit(shadow, shadow_rect)

    total_glow = max(glow_alpha, 60)
    if glow_alpha > 0:
        screen.blit(get_token_glow(token_color_for_piece(piece), w, total_glow), (x - (w + 30) // 2, y - (h + 30) // 2))

    rect = draw_surface.get_rect(center=(x, y))
    screen.blit(draw_surface, rect)

    highlight = pygame.Surface((w, h), pygame.SRCALPHA)
    shine_alpha = 50
    pygame.draw.ellipse(highlight, (255, 255, 255, shine_alpha), (w * 0.18, h * 0.08, w * 0.5, h * 0.28))
    pygame.draw.ellipse(highlight, (255, 255, 255, max(18, shine_alpha // 2)), (w * 0.28, h * 0.18, w * 0.22, h * 0.1))
    screen.blit(highlight, rect)

    pygame.draw.circle(screen, (0, 0, 0, 52), (x, y), w // 2, 3)

    return True

def draw_disc(screen: pygame.Surface, x: int, y: int, piece: int, scale: float = 1.0, glow_alpha: int = 0) -> None:
    draw_piece_image(screen, x, y, piece, scale=scale, glow_alpha=glow_alpha)


def make_centered_button(width: int, height: int, y: int) -> pygame.Rect:
    rect = pygame.Rect(0, y, width, height)
    rect.centerx = WIDTH // 2
    return rect


def make_standard_button(y: int) -> pygame.Rect:
    rect = pygame.Rect(0, y, BUTTON_WIDTH, BUTTON_HEIGHT)
    rect.centerx = WIDTH // 2
    return rect


def ui_title_rect() -> pygame.Rect:
    return pygame.Rect(UI_HEADER_LEFT, START_MENU_TITLE_Y, UI_HEADER_WIDTH, UI_TITLE_HEIGHT)


def ui_subtitle_rect() -> pygame.Rect:
    return pygame.Rect(UI_SUBTITLE_LEFT, START_MENU_SUBTITLE_Y, UI_SUBTITLE_WIDTH, UI_SUBTITLE_HEIGHT)


def ui_info_rect() -> pygame.Rect:
    return pygame.Rect(UI_INFO_LEFT, START_MENU_INFO_Y, UI_INFO_WIDTH, UI_INFO_HEIGHT)


def content_title_rect() -> pygame.Rect:
    return pygame.Rect(UI_HEADER_LEFT, CONTENT_TITLE_Y, UI_HEADER_WIDTH, 104)


def content_subtitle_rect() -> pygame.Rect:
    return pygame.Rect(UI_SUBTITLE_LEFT, CONTENT_SUBTITLE_Y, UI_SUBTITLE_WIDTH, 76)


def content_info_rect() -> pygame.Rect:
    return pygame.Rect(UI_INFO_LEFT, CONTENT_INFO_Y, UI_INFO_WIDTH, 54)


def ui_center_panel_rect(*, top: int = UI_PANEL_TOP, side_margin: int = UI_PANEL_SIDE_MARGIN, bottom_margin: int = UI_PANEL_BOTTOM_MARGIN) -> pygame.Rect:
    width = WIDTH - side_margin * 2
    height = HEIGHT - top - bottom_margin
    return pygame.Rect(side_margin, top, width, height)


def ui_primary_button_rect(y: int = START_MENU_PLAY_BUTTON_Y, width: int = START_MENU_PLAY_BUTTON_WIDTH, height: int = START_MENU_PLAY_BUTTON_HEIGHT) -> pygame.Rect:
    return make_centered_button(width, height, y)


def ui_secondary_button_rect(side: str, y: int = START_MENU_SECONDARY_BUTTON_Y, width: int = START_MENU_SECONDARY_BUTTON_WIDTH, height: int = START_MENU_SECONDARY_BUTTON_HEIGHT) -> pygame.Rect:
    x = START_MENU_SIDE_MARGIN if side == "left" else WIDTH - START_MENU_SIDE_MARGIN - width
    return pygame.Rect(x, y, width, height)


def selection_option_rect(index: int, *, width: int = SELECTION_OPTION_WIDTH, height: int = SELECTION_OPTION_HEIGHT, start_y: int = SELECTION_BLOCK_START_Y, gap: int = SELECTION_OPTION_GAP) -> pygame.Rect:
    step = height + gap
    rect = pygame.Rect(0, 0, width, height)
    rect.center = (WIDTH // 2, start_y + index * step + height // 2)
    return rect


def pause_layout_rects() -> tuple[pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect]:
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    panel_rect = pygame.Rect(0, 0, PAUSE_PANEL_WIDTH, PAUSE_PANEL_HEIGHT)
    panel_rect.center = (center_x, center_y)

    continue_rect = pygame.Rect(0, 0, 360, 84)
    continue_rect.center = (center_x, center_y + PAUSE_STACK_START_OFFSET)

    menu_rect = pygame.Rect(0, 0, 300, 70)
    menu_rect.center = (center_x, continue_rect.centery + PAUSE_STACK_GAP)

    slider_rect = pygame.Rect(0, 0, panel_rect.width - 88, SLIDER_HEIGHT)
    slider_rect.center = (center_x, menu_rect.centery + PAUSE_STACK_GAP + 8)

    return panel_rect, continue_rect, menu_rect, slider_rect


def draw_screen_header(
    screen: pygame.Surface,
    title: str,
    subtitle: str,
    *,
    title_font: pygame.font.Font,
    subtitle_font: pygame.font.Font,
    info_text: str | None = None,
) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect | None]:
    title_rect = ui_title_rect()
    subtitle_rect = ui_subtitle_rect()
    info_rect = ui_info_rect() if info_text else None

    draw_text_box(
        screen,
        title,
        title_rect,
        color=TEXT_COLOR,
        max_size=max(112, title_font.get_height() + 50),
        min_size=max(82, title_font.get_height() + 14),
        padding=20,
        line_spacing=TEXT_LINE_GAP + 8,
        gradient=(TITLE_GRADIENT_TOP, TITLE_GRADIENT_BOTTOM),
        is_title=True,
        align="center",
        vertical_align="top",
        word_spacing=1,
    )
    draw_text_box(
        screen,
        subtitle,
        subtitle_rect,
        color=SUBTEXT_COLOR,
        max_size=max(34, subtitle_font.get_height() + 10),
        min_size=max(24, subtitle_font.get_height() + 2),
        padding=16,
        line_spacing=LINE_SPACING + 10,
        align="center",
        vertical_align="top",
    )
    if info_rect is not None and info_text is not None:
        draw_text_box(
            screen,
            info_text,
            info_rect,
            color=TEXT_COLOR,
            max_size=max(27, subtitle_font.get_height() + 7),
            min_size=max(20, subtitle_font.get_height() + 2),
            padding=12,
            line_spacing=LINE_SPACING + 6,
            align="center",
            vertical_align="top",
        )
    return title_rect, subtitle_rect, info_rect


def draw_centered_content_header(
    screen: pygame.Surface,
    title: str,
    subtitle: str,
    *,
    title_font: pygame.font.Font,
    subtitle_font: pygame.font.Font,
    info_text: str | None = None,
) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect | None]:
    title_rect = content_title_rect()
    subtitle_rect = content_subtitle_rect()
    info_rect = content_info_rect() if info_text else None

    draw_text_box(
        screen,
        title,
        title_rect,
        color=TEXT_COLOR,
        max_size=max(72, title_font.get_height() + 18),
        min_size=max(42, title_font.get_height() - 4),
        padding=16,
        line_spacing=TEXT_LINE_GAP + 4,
        gradient=(TITLE_GRADIENT_TOP, TITLE_GRADIENT_BOTTOM),
        is_title=True,
        align="center",
        vertical_align="top",
    )
    draw_text_box(
        screen,
        subtitle,
        subtitle_rect,
        color=SUBTEXT_COLOR,
        max_size=max(26, subtitle_font.get_height() + 4),
        min_size=max(18, subtitle_font.get_height()),
        padding=10,
        line_spacing=LINE_SPACING + 6,
        align="center",
        vertical_align="top",
    )
    if info_rect is not None and info_text is not None:
        draw_text_box(
            screen,
            info_text,
            info_rect,
            color=TEXT_COLOR,
            max_size=max(22, subtitle_font.get_height() + 2),
            min_size=max(18, subtitle_font.get_height()),
            padding=8,
            line_spacing=LINE_SPACING + 4,
            align="center",
            vertical_align="top",
        )
    return title_rect, subtitle_rect, info_rect


def draw_action_button(
    screen: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    mouse_pos: tuple[int, int],
    *,
    primary: bool,
    primary_font: pygame.font.Font,
    secondary_font: pygame.font.Font,
) -> None:
    draw_button(
        screen,
        rect,
        label,
        primary_font if primary else secondary_font,
        rect.collidepoint(mouse_pos),
        padding=26 if primary else 20,
    )


def play_button_rect() -> pygame.Rect:
    return pygame.Rect((WIDTH - BUTTON_WIDTH) // 2, HEIGHT // 2 + 18, BUTTON_WIDTH, BUTTON_HEIGHT)


def start_settings_button_rect() -> pygame.Rect:
    return make_centered_button(START_MENU_SECONDARY_BUTTON_WIDTH, START_MENU_SECONDARY_BUTTON_HEIGHT, START_MENU_SECONDARY_BUTTON_Y)




def start_play_button_rect() -> pygame.Rect:
    return ui_primary_button_rect()


def mode_back_button_rect() -> pygame.Rect:
    rect = pygame.Rect(0, HEIGHT - 82, 240, 60)
    rect.centerx = WIDTH // 2
    return rect


def centered_back_button_rect(y: int) -> pygame.Rect:
    return ui_secondary_button_rect("left", y, 220, 50)


def start_screen_buttons() -> list[tuple[pygame.Rect, str, str]]:
    return [
        (start_play_button_rect(), ACTION_PLAY, "Play Game"),
        (start_settings_button_rect(), ACTION_SETTINGS, "Settings"),
    ]


def play_menu_buttons() -> list[tuple[pygame.Rect, int | str, str]]:
    return [
        (selection_option_rect(0), ACTION_PLAY, "AI Mode"),
        (selection_option_rect(1), MODE_PVP, "2 Players"),
        (make_centered_button(220, 56, BOTTOM_NAV_Y), ACTION_BACK, "Back"),
    ]


def ai_menu_buttons() -> list[tuple[pygame.Rect, int | str, str]]:
    return [
        (selection_option_rect(0), MODE_AI_FIRST, "AI Start"),
        (selection_option_rect(1), MODE_AI_SECOND, "You Start"),
        (make_centered_button(220, 56, BOTTOM_NAV_Y), STATE_PLAY_MENU, "Back"),
    ]


def difficulty_buttons() -> list[tuple[pygame.Rect, int, str]]:
    return [
        (selection_option_rect(0), EASY, "Easy"),
        (selection_option_rect(1), MEDIUM, "Medium"),
        (selection_option_rect(2), HARD, "Hard"),
    ]


def difficulty_back_button_rect() -> pygame.Rect:
    return make_centered_button(220, 56, BOTTOM_NAV_Y)


def restart_button_rect() -> pygame.Rect:
    restart_rect, _ = game_over_button_rects()
    return restart_rect


def main_menu_button_rect() -> pygame.Rect:
    _, menu_rect = game_over_button_rects()
    return menu_rect


def pause_button_rect() -> pygame.Rect:
    rect = pygame.Rect(0, 0, 120, 44)
    rect.topright = (WIDTH - 20, 20)
    return rect


def settings_back_button_rect() -> pygame.Rect:
    panel_rect = settings_panel_rect()
    rect = pygame.Rect(0, 0, min(340, panel_rect.width - 80), 54)
    rect.centerx = panel_rect.centerx
    rect.top = panel_rect.top + 394
    return rect


def pause_panel_rect() -> pygame.Rect:
    panel_rect, _, _, _ = pause_layout_rects()
    return panel_rect


def pause_continue_button_rect() -> pygame.Rect:
    _, continue_rect, _, _ = pause_layout_rects()
    return continue_rect


def pause_menu_button_rect() -> pygame.Rect:
    _, _, menu_rect, _ = pause_layout_rects()
    return menu_rect


def pause_slider_rect() -> pygame.Rect:
    _, _, _, slider_rect = pause_layout_rects()
    return slider_rect


def settings_panel_rect() -> pygame.Rect:
    panel_width = min(WIDTH - 48, 520)
    panel_height = min(HEIGHT - 250, 460)
    panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
    panel_rect.center = (WIDTH // 2, HEIGHT // 2 + 100)
    return panel_rect


def settings_toggle_rect(index: int = 0) -> pygame.Rect:
    panel_rect = settings_panel_rect()
    rect = pygame.Rect(0, 0, min(380, panel_rect.width - 80), 54)
    rect.centerx = panel_rect.centerx
    rect.top = panel_rect.top + 276 + index * 62
    return rect


def settings_slider_rect(index: int) -> pygame.Rect:
    panel_rect = settings_panel_rect()
    slider_width = min(panel_rect.width - 100, SLIDER_WIDTH + 40)
    start_y = panel_rect.top + 126
    spacing = 96
    rect = pygame.Rect(0, 0, slider_width, SLIDER_HEIGHT)
    rect.centerx = panel_rect.centerx
    rect.top = start_y + index * spacing
    return rect


def _mix_color(color_a: tuple[int, int, int], color_b: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    clamped_ratio = max(0.0, min(1.0, ratio))
    return (
        int(color_a[0] * (1.0 - clamped_ratio) + color_b[0] * clamped_ratio),
        int(color_a[1] * (1.0 - clamped_ratio) + color_b[1] * clamped_ratio),
        int(color_a[2] * (1.0 - clamped_ratio) + color_b[2] * clamped_ratio),
    )


def _tint_color(color: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return _mix_color(color, (255, 255, 255), amount)


def _shade_color(color: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return _mix_color(color, (0, 0, 0), amount)


def _draw_gradient_rounded_rect(
    screen: pygame.Surface,
    rect: pygame.Rect,
    top_color: tuple[int, int, int],
    bottom_color: tuple[int, int, int],
    border_radius: int,
    *,
    border_color: tuple[int, int, int] | None = None,
    border_width: int = 0,
    gloss_alpha: int = 0,
    gloss_height: int | None = None,
) -> None:
    if rect.width <= 0 or rect.height <= 0:
        return

    gradient_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    for y in range(rect.height):
        ratio = y / max(1, rect.height - 1)
        row_color = _mix_color(top_color, bottom_color, ratio)
        pygame.draw.line(gradient_surface, (*row_color, 255), (0, y), (rect.width, y))

    if gloss_alpha > 0:
        gloss_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        resolved_gloss_height = min(rect.height, gloss_height if gloss_height is not None else max(24, rect.height // 3))
        pygame.draw.rect(
            gloss_surface,
            (255, 255, 255, gloss_alpha),
            pygame.Rect(0, 0, rect.width, resolved_gloss_height),
            border_radius=border_radius,
        )
        gradient_surface.blit(gloss_surface, (0, 0))

    mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=border_radius)
    gradient_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(gradient_surface, rect.topleft)

    if border_color is not None and border_width > 0:
        pygame.draw.rect(screen, border_color, rect, width=border_width, border_radius=border_radius)


def _draw_rect_glow(
    screen: pygame.Surface,
    rect: pygame.Rect,
    color: tuple[int, int, int],
    alpha: int,
    padding: int,
    border_radius: int,
) -> None:
    glow_rect = rect.inflate(padding * 2, padding * 2)
    glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(
        glow_surface,
        (*color, max(0, min(255, alpha))),
        glow_surface.get_rect(),
        border_radius=border_radius + padding,
    )
    softened = pygame.transform.smoothscale(
        glow_surface,
        (max(8, glow_rect.width - padding), max(8, glow_rect.height - padding)),
    )
    softened_rect = softened.get_rect(center=rect.center)
    screen.blit(softened, softened_rect)






def game_over_panel_rect() -> pygame.Rect:
    return ui_center_panel_rect(top=258, side_margin=120, bottom_margin=170)


def game_over_button_rects() -> tuple[pygame.Rect, pygame.Rect]:
    panel_rect = game_over_panel_rect()
    button_spacing = 40
    button_width = 190
    button_height = 64
    total_width = button_width * 2 + button_spacing
    start_x = panel_rect.centerx - total_width // 2
    top = panel_rect.centery + 40
    restart_rect = pygame.Rect(start_x, top, button_width, button_height)
    menu_rect = pygame.Rect(start_x + button_width + button_spacing, top, button_width, button_height)
    return restart_rect, menu_rect


def _legacy_draw_button(
    screen: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    font: pygame.font.Font,
    hovered: bool,
    *,
    padding: int | None = None,
) -> None:
    fill_color = BUTTON_HOVER_COLOR if hovered else BUTTON_COLOR
    border_color = ACCENT_COLOR if hovered else BOARD_COLOR
    pygame.draw.rect(screen, PANEL_SHADOW, rect.move(0, 6), border_radius=22)
    pygame.draw.rect(screen, fill_color, rect, border_radius=22)
    highlight_rect = pygame.Rect(rect.left, rect.top, rect.width, max(16, rect.height // 3))
    pygame.draw.rect(screen, (255, 255, 255, 24 if hovered else 14), highlight_rect, border_radius=22)
    pygame.draw.rect(screen, border_color, rect, width=3, border_radius=22)
    draw_text_box(
        screen,
        label,
        rect,
        BUTTON_TEXT_COLOR,
        max_size=max(18, font.get_height()),
        min_size=16,
        padding=padding if padding is not None else min(rect.width // 4, max(BUTTON_PADDING_X, BUTTON_PADDING_Y)),
        line_spacing=LINE_SPACING,
        shadow_offset=(1, 2),
        word_spacing=1,
        align="center",
    )


def draw_slider(
    screen: pygame.Surface,
    rect: pygame.Rect,
    value_ratio: float,
    label: str,
    value_text: str,
    font: pygame.font.Font,
    mouse_pos: tuple[int, int],
    fill_color: tuple[int, int, int],
) -> None:
    label_rect = pygame.Rect(rect.left - 18, rect.top - 54, rect.width + 36, 42)
    draw_text_box(
        screen,
        f"{label}: {value_text}",
        label_rect,
        color=TEXT_COLOR,
        max_size=max(16, font.get_height()),
        min_size=15,
        allow_wrap=True,
        padding=10,
        line_spacing=LINE_SPACING,
        align="left",
        vertical_align="bottom",
    )
    track_rect = rect.inflate(0, 18)
    hovered = track_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, PANEL_SHADOW, track_rect.move(0, 4), border_radius=18)
    pygame.draw.rect(screen, PANEL_COLOR, track_rect, border_radius=18)
    fill_width = int(track_rect.width * max(0.0, min(1.0, value_ratio)))
    if fill_width > 0:
        fill_rect = pygame.Rect(track_rect.left, track_rect.top, fill_width, track_rect.height)
        pygame.draw.rect(screen, fill_color, fill_rect, border_radius=18)
    knob_x = track_rect.left + fill_width
    knob_x = max(track_rect.left, min(track_rect.right, knob_x))
    glow_radius = 18 if hovered else 14
    glow_surface = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.circle(glow_surface, (*fill_color, 70 if hovered else 40), (24, 24), glow_radius)
    screen.blit(glow_surface, glow_surface.get_rect(center=(knob_x, track_rect.centery)))
    pygame.draw.circle(screen, BUTTON_COLOR, (knob_x, track_rect.centery), 14)
    pygame.draw.circle(screen, BOARD_COLOR, (knob_x, track_rect.centery), 14, width=3)


def draw_reward_info_tooltip(
    screen: pygame.Surface,
    anchor_rect: pygame.Rect,
    mouse_pos: tuple[int, int],
    font: pygame.font.Font,
) -> pygame.Rect:
    icon_rect = pygame.Rect(0, 0, 24, 24)
    icon_rect.midleft = (anchor_rect.right + 14, anchor_rect.centery)
    hovered = icon_rect.collidepoint(mouse_pos)

    glow = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(glow, (*ACCENT_COLOR, 42 if hovered else 22), (20, 20), 14 if hovered else 12)
    screen.blit(glow, glow.get_rect(center=icon_rect.center))
    pygame.draw.circle(screen, (18, 28, 42), icon_rect.center, 11)
    pygame.draw.circle(screen, ACCENT_COLOR if hovered else (168, 190, 220), icon_rect.center, 11, width=2)
    draw_text_box(
        screen,
        "i",
        icon_rect,
        color=TEXT_COLOR,
        max_size=16,
        min_size=14,
        padding=2,
        allow_wrap=False,
        shadow_offset=(1, 1),
    )

    if not hovered:
        return icon_rect

    tooltip_width = 280
    tooltip_height = 146
    tooltip_rect = pygame.Rect(0, 0, tooltip_width, tooltip_height)
    tooltip_rect.midbottom = (icon_rect.centerx, icon_rect.top - 10)
    if tooltip_rect.left < 20:
        tooltip_rect.left = 20
    if tooltip_rect.right > WIDTH - 20:
        tooltip_rect.right = WIDTH - 20
    if tooltip_rect.top < 20:
        tooltip_rect.top = icon_rect.bottom + 10

    tooltip_surface = pygame.Surface((tooltip_rect.width, tooltip_rect.height), pygame.SRCALPHA)
    pygame.draw.rect(tooltip_surface, (8, 12, 20, 215), tooltip_surface.get_rect(), border_radius=18)
    pygame.draw.rect(tooltip_surface, (92, 136, 196, 220), tooltip_surface.get_rect(), width=2, border_radius=18)
    pygame.draw.rect(tooltip_surface, (255, 255, 255, 18), pygame.Rect(0, 0, tooltip_rect.width, 24), border_radius=18)
    screen.blit(tooltip_surface, tooltip_rect.topleft)

    draw_text_list(
        screen,
        [
            {
                "text": reward_preview_lines()[0],
                "size": max(16, font.get_height()),
                "width": tooltip_rect.width - 24,
            },
            {
                "text": reward_preview_lines()[1],
                "size": max(16, font.get_height()),
                "width": tooltip_rect.width - 24,
            },
            {
                "text": reward_preview_lines()[2],
                "size": max(16, font.get_height()),
                "width": tooltip_rect.width - 24,
            },
        ],
        tooltip_rect.top + 22,
        spacing=36,
        center_x=tooltip_rect.centerx,
    )
    return icon_rect


def draw_pause_button(screen: pygame.Surface, font: pygame.font.Font, mouse_pos: tuple[int, int]) -> pygame.Rect:
    rect = pause_button_rect()
    hovered = rect.collidepoint(mouse_pos)
    fill_color = BUTTON_HOVER_COLOR if hovered else BUTTON_COLOR
    border_color = ACCENT_COLOR if hovered else BOARD_COLOR
    shadow_rect = rect.move(0, 6)
    pygame.draw.rect(screen, PANEL_SHADOW, shadow_rect, border_radius=22)
    pygame.draw.rect(screen, fill_color, rect, border_radius=22)
    highlight_rect = pygame.Rect(rect.left, rect.top, rect.width, max(16, rect.height // 3))
    pygame.draw.rect(screen, (255, 255, 255, 24 if hovered else 14), highlight_rect, border_radius=22)
    pygame.draw.rect(screen, border_color, rect, width=3, border_radius=22)

    text_surface = font.render("Pause", True, BUTTON_TEXT_COLOR).convert_alpha()
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    return rect


def draw_centered_button(
    screen: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    font: pygame.font.Font,
    hovered: bool,
    *,
    fill_color: tuple[int, int, int] | None = None,
    text_color: tuple[int, int, int] = BUTTON_TEXT_COLOR,
) -> None:
    resolved_fill = BUTTON_HOVER_COLOR if hovered else (fill_color if fill_color is not None else BUTTON_COLOR)
    border_color = ACCENT_COLOR if hovered else BOARD_COLOR
    pygame.draw.rect(screen, PANEL_SHADOW, rect.move(0, 6), border_radius=22)
    pygame.draw.rect(screen, resolved_fill, rect, border_radius=22)
    highlight_rect = pygame.Rect(rect.left, rect.top, rect.width, max(16, rect.height // 3))
    pygame.draw.rect(screen, (255, 255, 255, 24 if hovered else 14), highlight_rect, border_radius=22)
    pygame.draw.rect(screen, border_color, rect, width=3, border_radius=22)
    draw_text_box(
        screen,
        label,
        rect,
        color=text_color,
        max_size=max(18, font.get_height()),
        min_size=MIN_UI_FONT_SIZE,
        padding=16,
        line_spacing=LINE_SPACING,
        shadow_offset=(1, 2),
        align="center",
    )


def draw_pause_overlay(
    screen: pygame.Surface,
    subtitle_font: pygame.font.Font,
    button_font: pygame.font.Font,
    mouse_pos: tuple[int, int],
    overlay_alpha: float,
) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
    alpha = max(0, min(220, int(overlay_alpha)))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((6, 10, 18, alpha))
    screen.blit(overlay, (0, 0))

    primary_font = get_font(size=28, bold=False)
    secondary_font = get_font(size=28, bold=False)
    center_x = screen.get_width() // 2
    center_y = screen.get_height() // 2
    panel_rect, continue_rect, menu_rect, slider_rect = pause_layout_rects()
    panel_rect.center = (center_x, center_y)
    continue_rect.center = (center_x, center_y + PAUSE_STACK_START_OFFSET)
    menu_rect.center = (center_x, continue_rect.centery + PAUSE_STACK_GAP)
    slider_rect.center = (center_x, menu_rect.centery + PAUSE_STACK_GAP + 8)
    shadow_rect = panel_rect.move(0, 10)
    pygame.draw.rect(screen, PANEL_SHADOW, shadow_rect, border_radius=30)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=30)
    pygame.draw.rect(screen, (56, 76, 106), panel_rect, width=2, border_radius=30)
    pygame.draw.rect(screen, (255, 255, 255, 18), pygame.Rect(panel_rect.left, panel_rect.top, panel_rect.width, 30), border_radius=30)

    draw_text_box(
        screen,
        "Paused",
        pygame.Rect(panel_rect.left + 24, panel_rect.top + 22, panel_rect.width - 48, 64),
        color=TEXT_COLOR,
        max_size=max(42, button_font.get_height() + 10),
        min_size=max(26, subtitle_font.get_height() + 4),
        padding=10,
        line_spacing=LINE_SPACING + 4,
        gradient=(TITLE_GRADIENT_TOP, TITLE_GRADIENT_BOTTOM),
        is_title=True,
    )
    draw_text_box(
        screen,
        "Take a break or adjust the volume",
        pygame.Rect(panel_rect.left + 34, panel_rect.top + 92, panel_rect.width - 68, 42),
        color=SUBTEXT_COLOR,
        max_size=max(18, subtitle_font.get_height()),
        min_size=16,
        padding=8,
    )

    button_specs = [
        (continue_rect, "Continue Playing", primary_font, 26),
        (menu_rect, "Back to Menu", secondary_font, 20),
    ]
    for rect, label, font_obj, padding in button_specs:
        draw_button(screen, rect, label, font_obj, rect.collidepoint(mouse_pos), padding=padding)

    draw_slider(
        screen,
        slider_rect,
        float(SETTINGS["volume"]),
        "Volume",
        f"{int(float(SETTINGS['volume']) * 100)}%",
        subtitle_font,
        mouse_pos,
        ACCENT_COLOR,
    )
    return continue_rect, menu_rect, slider_rect


def draw_settings_screen(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    subtitle_font: pygame.font.Font,
    button_font: pygame.font.Font,
    mouse_pos: tuple[int, int],
) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect]:
    draw_background(screen)
    draw_text_box(
        screen,
        "Settings",
        content_title_rect(),
        color=TEXT_COLOR,
        max_size=max(72, title_font.get_height() + 18),
        min_size=max(42, title_font.get_height() - 4),
        padding=16,
        gradient=(TITLE_GRADIENT_TOP, TITLE_GRADIENT_BOTTOM),
        is_title=True,
        align="center",
        vertical_align="top",
    )

    panel_rect = settings_panel_rect()
    pygame.draw.rect(screen, PANEL_SHADOW, panel_rect.move(0, 10), border_radius=32)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=32)
    pygame.draw.rect(screen, (70, 95, 135), panel_rect, width=3, border_radius=32)
    pygame.draw.rect(
        screen,
        (34, 46, 68),
        pygame.Rect(panel_rect.left, panel_rect.top, panel_rect.width, 32),
        border_radius=32,
    )

    draw_text_box(
        screen,
        "Audio Settings",
        pygame.Rect(panel_rect.left + 32, panel_rect.top + 28, panel_rect.width - 64, 48),
        color=TEXT_COLOR,
        max_size=32,
        min_size=24,
        bold=True,
        gradient=(TITLE_GRADIENT_TOP, TITLE_GRADIENT_BOTTOM),
    )

    effects_slider = settings_slider_rect(0)
    music_slider = settings_slider_rect(1)
    effects_toggle = settings_toggle_rect(0)
    music_toggle = settings_toggle_rect(1)
    back_rect = settings_back_button_rect()

    draw_slider(
        screen,
        effects_slider,
        float(SETTINGS.get("effects_volume", SETTINGS.get("volume", 0.5))),
        "Effects Volume",
        f"{int(float(SETTINGS.get('effects_volume', SETTINGS.get('volume', 0.5))) * 100)}%",
        subtitle_font,
        mouse_pos,
        ACCENT_COLOR,
    )

    draw_slider(
        screen, music_slider, float(SETTINGS.get("music_volume", DEFAULT_SETTINGS["music_volume"])), "Music Volume",
        f"{int(float(SETTINGS.get('music_volume', DEFAULT_SETTINGS['music_volume'])) * 100)}%", subtitle_font, mouse_pos, (126, 116, 255),
    )

    for toggle_rect, label, setting_key in (
        (effects_toggle, "Sound Effects", "sound_enabled"),
        (music_toggle, "Background Music", "music_enabled"),
    ):
        enabled = bool(SETTINGS.get(setting_key, True))
        toggle_color = BUTTON_GREEN if enabled else (180, 70, 70)
        pygame.draw.rect(screen, PANEL_SHADOW, toggle_rect.move(0, 4), border_radius=18)
        pygame.draw.rect(screen, (28, 34, 48), toggle_rect, border_radius=18)
        pygame.draw.rect(screen, toggle_color, toggle_rect, width=3, border_radius=18)
        draw_text_box(screen, f"{label}: {'ON' if enabled else 'OFF'}", toggle_rect.inflate(-14, -6), color=(255, 255, 255), max_size=18, min_size=14, allow_wrap=False, align="center")

    draw_button(screen, back_rect, "Back to Menu", button_font, back_rect.collidepoint(mouse_pos), padding=20)
    return back_rect, effects_slider, effects_toggle, music_slider, music_toggle
























def draw_button(
    screen: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    font: pygame.font.Font,
    hovered: bool,
    *,
    padding: int | None = None,
) -> None:
    """Generic button with stronger padding and centered text."""
    base_fill = BUTTON_HOVER_COLOR if hovered else BUTTON_COLOR
    border_color = ACCENT_COLOR if hovered else BOARD_COLOR
    resolved_padding = padding if padding is not None else 20

    pygame.draw.rect(screen, PANEL_SHADOW, rect.move(0, 7), border_radius=rect.height // 2)
    _draw_gradient_rounded_rect(
        screen,
        rect,
        _tint_color(base_fill, 0.05),
        _shade_color(base_fill, 0.06),
        rect.height // 2,
        border_color=border_color,
        border_width=3,
        gloss_alpha=18 if hovered else 10,
        gloss_height=max(16, rect.height // 3),
    )
    draw_text_box(
        screen,
        label,
        rect,
        color=BUTTON_TEXT_COLOR,
        max_size=max(18, font.get_height()),
        min_size=14,
        allow_wrap=False,
        padding=resolved_padding,
        line_spacing=2,
        shadow_offset=(1, 1),
        align="center",
    )


































def draw_start_screen(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    subtitle_font: pygame.font.Font,
    button_font: pygame.font.Font,
    mouse_pos: tuple[int, int],
) -> list[tuple[pygame.Rect, str]]:
    draw_background(screen)
    play_font = get_font(size=max(32, button_font.get_height() + 10), bold=False)
    secondary_font = get_font(size=max(20, button_font.get_height() - 4), bold=False)
    draw_screen_header(
        screen,
        "GRAVITY 4",
        "Play against the AI or a friend.",
        title_font=title_font,
        subtitle_font=subtitle_font,
        info_text=f"Tokens: {int(PLAYER_DATA['tokens'])}",
    )

    buttons = start_screen_buttons()

    for rect, mode, label in buttons:
        draw_action_button(screen, rect, label, mouse_pos, primary=mode == ACTION_PLAY, primary_font=play_font, secondary_font=secondary_font)

    credit_rect = pygame.Rect(WIDTH - 270, HEIGHT - 34, 250, 28)
    draw_text_box(
        screen,
        "Credit: Aron DAVIDIAN",
        credit_rect,
        color=SUBTEXT_COLOR,
        max_size=18,
        min_size=14,
        allow_wrap=False,
        padding=4,
        align="right",
    )

    return [(rect, mode) for rect, mode, _ in buttons]


def draw_play_menu_screen(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    subtitle_font: pygame.font.Font,
    button_font: pygame.font.Font,
    mouse_pos: tuple[int, int],
) -> list[tuple[pygame.Rect, int | str]]:
    draw_background(screen)
    option_font = get_font(size=max(32, button_font.get_height() + 10), bold=False)
    secondary_font = get_font(size=max(20, button_font.get_height() - 4), bold=False)
    draw_centered_content_header(
        screen,
        "Play Game",
        "Choose who starts or switch to 2-player mode",
        title_font=title_font,
        subtitle_font=subtitle_font,
    )

    buttons = play_menu_buttons()
    for rect, mode, label in buttons:
        if mode == ACTION_BACK:
            draw_button(screen, rect, label, secondary_font, rect.collidepoint(mouse_pos), padding=18)
        else:
            draw_button(screen, rect, label, option_font, rect.collidepoint(mouse_pos), padding=24)

    return [(rect, mode) for rect, mode, _ in buttons]


def draw_ai_menu_screen(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    subtitle_font: pygame.font.Font,
    button_font: pygame.font.Font,
    mouse_pos: tuple[int, int],
) -> list[tuple[pygame.Rect, int | str]]:
    draw_background(screen)
    option_font = get_font(size=max(32, button_font.get_height() + 10), bold=False)
    secondary_font = get_font(size=max(20, button_font.get_height() - 4), bold=False)
    _, subtitle_rect, _ = draw_centered_content_header(
        screen,
        "AI Mode",
        "Choose who starts the AI game",
        title_font=title_font,
        subtitle_font=subtitle_font,
    )

    buttons = ai_menu_buttons()
    for rect, mode, label in buttons:
        if label == "Back":
            draw_button(screen, rect, label, secondary_font, rect.collidepoint(mouse_pos), padding=18)
        else:
            draw_button(screen, rect, label, option_font, rect.collidepoint(mouse_pos), padding=24)
    draw_reward_info_tooltip(screen, subtitle_rect, mouse_pos, subtitle_font)

    return [(rect, mode) for rect, mode, _ in buttons]


def draw_difficulty_screen(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    subtitle_font: pygame.font.Font,
    button_font: pygame.font.Font,
    mouse_pos: tuple[int, int],
    selected_mode: int,
) -> tuple[list[tuple[pygame.Rect, int]], pygame.Rect]:
    draw_background(screen)
    option_font = get_font(size=max(32, button_font.get_height() + 10), bold=False)
    secondary_font = get_font(size=max(20, button_font.get_height() - 4), bold=False)
    _, subtitle_rect, _ = draw_centered_content_header(
        screen,
        "AI Difficulty",
        f"{mode_name(selected_mode)} · choose a 3, 5, or 7-move search",
        title_font=title_font,
        subtitle_font=subtitle_font,
    )

    buttons = difficulty_buttons()
    for rect, difficulty, label in buttons:
        draw_button(screen, rect, label, option_font, rect.collidepoint(mouse_pos), padding=24)
    back_rect = difficulty_back_button_rect()
    draw_button(screen, back_rect, "Back", secondary_font, back_rect.collidepoint(mouse_pos), padding=18)
    draw_reward_info_tooltip(screen, subtitle_rect, mouse_pos, subtitle_font)

    return [(rect, difficulty) for rect, difficulty, _ in buttons], back_rect


def draw_game_over_screen(
    screen: pygame.Surface,
    board: Board,
    result_message: str,
    title_font: pygame.font.Font,
    subtitle_font: pygame.font.Font,
    button_font: pygame.font.Font,
    mouse_pos: tuple[int, int],
    winning_cells: list[tuple[int, int]] | None = None,
    highlight_visible: bool = True,
) -> tuple[pygame.Rect, pygame.Rect]:
    draw_board(screen, board, subtitle_font, "")
    if winning_cells and highlight_visible:
        draw_winning_highlight(screen, winning_cells)

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((4, 8, 14, 170))
    screen.blit(overlay, (0, 0))

    primary_font = get_font(size=max(32, button_font.get_height() + 10), bold=False)
    secondary_font = get_font(size=max(20, button_font.get_height() - 4), bold=False)
    panel_rect = game_over_panel_rect()
    pygame.draw.rect(screen, PANEL_SHADOW, panel_rect.move(0, 8), border_radius=28)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=28)
    pygame.draw.rect(screen, (56, 76, 106), panel_rect, width=2, border_radius=28)
    pygame.draw.rect(screen, (255, 255, 255, 18), pygame.Rect(panel_rect.left, panel_rect.top, panel_rect.width, 24), border_radius=28)

    draw_text_box(
        screen,
        result_message,
        pygame.Rect(panel_rect.left + 24, panel_rect.top + 20, panel_rect.width - 48, 82),
        color=TEXT_COLOR,
        max_size=max(40, title_font.get_height()),
        min_size=max(24, subtitle_font.get_height() + 4),
        padding=10,
        line_spacing=LINE_SPACING + 6,
        gradient=(TITLE_GRADIENT_TOP, TITLE_GRADIENT_BOTTOM),
        is_title=True,
    )
    draw_text_box(
        screen,
        "Choose what you want to do next",
        pygame.Rect(panel_rect.left + 26, panel_rect.top + 112, panel_rect.width - 52, 52),
        color=SUBTEXT_COLOR,
        max_size=max(22, subtitle_font.get_height() + 2),
        min_size=max(18, subtitle_font.get_height()),
        padding=8,
    )

    restart_rect, menu_rect = game_over_button_rects()
    draw_button(screen, restart_rect, "Restart", primary_font, restart_rect.collidepoint(mouse_pos), padding=18)
    draw_button(screen, menu_rect, "Main Menu", secondary_font, menu_rect.collidepoint(mouse_pos), padding=18)
    return restart_rect, menu_rect


def draw_falling_piece(
    screen: pygame.Surface,
    col: int,
    y: float,
    piece: int,
) -> None:
    x = BOARD_LEFT + col * CELL_SIZE + CELL_SIZE // 2
    travel_ratio = max(0.0, min(1.0, y / max(float(BOARD_TOP + BOARD_HEIGHT), 1.0)))
    draw_disc(screen, x, int(y), piece, scale=1.04 - travel_ratio * 0.04, glow_alpha=40)


def draw_winning_highlight(screen: pygame.Surface, cells: list[tuple[int, int]]) -> None:
    global WIN_GLOW_SURFACE
    if WIN_GLOW_SURFACE is None:
        WIN_GLOW_SURFACE = pygame.Surface((CELL_SIZE + 30, CELL_SIZE + 30), pygame.SRCALPHA)
        pygame.draw.circle(
            WIN_GLOW_SURFACE,
            (*WIN_HIGHLIGHT_COLOR, 70),
            (WIN_GLOW_SURFACE.get_width() // 2, WIN_GLOW_SURFACE.get_height() // 2),
            RADIUS + 10,
        )
    for row, col in cells:
        x, y = board_pixel_position(row, col)
        screen.blit(WIN_GLOW_SURFACE, (x - WIN_GLOW_SURFACE.get_width() // 2, y - WIN_GLOW_SURFACE.get_height() // 2))
        pygame.draw.circle(screen, WIN_HIGHLIGHT_COLOR, (x, y), RADIUS + 4, width=6)


def draw_fade_overlay(screen: pygame.Surface, alpha: float) -> None:
    if alpha <= 0:
        return
    resolved_alpha = max(0, min(255, int(alpha)))
    overlay = FADE_SURFACES.get(resolved_alpha)
    if overlay is None:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 12, 20, resolved_alpha))
        FADE_SURFACES[resolved_alpha] = overlay
    screen.blit(overlay, (0, 0))


def create_tone(
    frequencies: float | list[float] | tuple[float, ...],
    duration_ms: int,
    volume: float = 0.35,
    sample_rate: int = 44100,
) -> pygame.mixer.Sound | None:
    if pygame is None or pygame.mixer.get_init() is None:
        return None

    if isinstance(frequencies, (int, float)):
        tone_list = [float(frequencies)]
    else:
        tone_list = [float(value) for value in frequencies]

    sample_count = int(sample_rate * duration_ms / 1000)
    channel_count = int(pygame.mixer.get_init()[2])
    amplitude = int(32767 * max(0.0, min(volume, 1.0)))
    samples = array("h")

    for index in range(sample_count):
        time_position = index / sample_rate
        attack = min(1.0, index / max(sample_count * 0.12, 1))
        release = min(1.0, (sample_count - index) / max(sample_count * 0.28, 1))
        envelope = min(attack, release)

        value = 0.0
        for tone_index, frequency in enumerate(tone_list, start=1):
            weight = 1 / tone_index
            value += weight * math.sin(2 * math.pi * frequency * time_position)
        value /= sum(1 / index for index in range(1, len(tone_list) + 1))
        sample = int(amplitude * envelope * value)
        for _ in range(channel_count):
            samples.append(sample)

    return pygame.mixer.Sound(buffer=samples.tobytes())


def init_sounds() -> dict[str, pygame.mixer.Sound | None]:
    return {
        "drop": create_tone((392.0, 523.25, 784.0), 150, 0.34),
        "click": create_tone((660.0, 880.0), 55, 0.2),
        "transition": create_tone((440.0, 659.25), 140, 0.22),
        "purchase": create_tone((523.25, 659.25, 783.99, 1046.5), 260, 0.3),
        "win": create_tone((523.25, 659.25, 783.99), 420, 0.36),
        "loss": create_tone((392.0, 329.63, 261.63), 420, 0.32),
        "draw": create_tone((261.63, 329.63), 280, 0.28),
    }


def _create_synth_loop(
    notes: tuple[float, ...],
    bpm: int,
    sample_rate: int | None = None,
    *,
    pad_level: float = 0.0,
) -> pygame.mixer.Sound | None:
    if pygame.mixer.get_init() is None:
        return None
    mixer_format = pygame.mixer.get_init()
    sample_rate = sample_rate or int(mixer_format[0])
    channel_count = int(mixer_format[2])
    beat = 60.0 / bpm
    duration = beat * len(notes)
    samples = array("h")
    total = int(sample_rate * duration)
    for index in range(total):
        t = index / sample_rate
        note_index = min(len(notes) - 1, int(t / beat))
        local_t = (t - note_index * beat) / beat
        envelope = min(1.0, local_t * 8.0, (1.0 - local_t) * 4.0)
        frequency = notes[note_index]
        # A soft fundamental with a restrained octave shimmer.
        wave = math.sin(2 * math.pi * frequency * t) * 0.72
        wave += math.sin(2 * math.pi * frequency * 2 * t) * 0.16
        wave += math.sin(2 * math.pi * (frequency / 2) * t) * 0.12
        if pad_level:
            chord_root = notes[(note_index // 4 * 4) % len(notes)] / 2
            wave += math.sin(2 * math.pi * chord_root * t) * pad_level
        sample = int(32767 * 0.16 * max(0.0, envelope) * wave)
        for _ in range(channel_count):
            samples.append(sample)
    return pygame.mixer.Sound(buffer=samples.tobytes())


def create_menu_music(sample_rate: int | None = None) -> pygame.mixer.Sound | None:
    """Bright, lightly rhythmic original lobby loop."""
    return _create_synth_loop(
        (261.63, 329.63, 392.0, 523.25, 392.0, 329.63, 293.66, 392.0,
         440.0, 523.25, 659.25, 523.25, 392.0, 329.63, 293.66, 261.63),
        96,
        sample_rate,
        pad_level=0.12,
    )


def create_game_music(sample_rate: int | None = None) -> pygame.mixer.Sound | None:
    """Slower, softer original loop for focus during a match."""
    return _create_synth_loop(
        (196.0, 246.94, 293.66, 369.99, 329.63, 293.66, 246.94, 220.0,
         174.61, 220.0, 261.63, 329.63, 293.66, 261.63, 220.0, 196.0),
        76,
        sample_rate,
        pad_level=0.2,
    )


def sync_music(
    lobby_music: pygame.mixer.Sound | None,
    game_music: pygame.mixer.Sound | None,
    channels: tuple[pygame.mixer.Channel, pygame.mixer.Channel],
    in_game: bool,
    dt: float,
    state: dict[str, object],
) -> None:
    enabled = SOUND_OK and bool(SETTINGS.get("music_enabled", True))
    if not enabled:
        for channel in channels:
            channel.stop()
        state.clear()
        return

    target = "game" if in_game else "lobby"
    target_music = game_music if in_game else lobby_music
    if target_music is None:
        return
    if state.get("target") != target:
        factors = state.get("factors", [0.0, 0.0])
        tracks = state.get("tracks", [None, None])
        already_playing = next((index for index in range(2) if tracks[index] == target and channels[index].get_busy()), None)
        if already_playing is not None:
            to_index = already_playing
            from_index = 1 - to_index if channels[1 - to_index].get_busy() else None
        else:
            from_index = max(range(2), key=lambda index: float(factors[index])) if state.get("target") else None
            to_index = 0 if from_index is None else 1 - from_index
            channels[to_index].stop()
            channels[to_index].play(target_music, loops=-1)
            tracks = list(tracks)
            tracks[to_index] = target
        channels[to_index].set_volume(0.0 if from_index is None else channels[to_index].get_volume())
        state.update({"target": target, "from": from_index, "to": to_index, "elapsed": 0.0, "factors": list(factors), "tracks": tracks})

    elapsed = min(1.0, float(state.get("elapsed", 0.0)) + max(0.0, dt) / 1.4)
    state["elapsed"] = elapsed
    factors = [0.0, 0.0]
    from_index = state.get("from")
    to_index = int(state["to"])
    if from_index is not None and int(from_index) != to_index:
        factors[int(from_index)] = 1.0 - elapsed
    factors[to_index] = elapsed if from_index is not None else min(1.0, elapsed)
    volume = max(0.0, min(1.0, float(SETTINGS.get("music_volume", DEFAULT_SETTINGS["music_volume"]))))
    for index, channel in enumerate(channels):
        channel.set_volume(volume * factors[index])
        if index != to_index and factors[index] <= 0 and channel.get_busy():
            channel.stop()
    state["factors"] = factors
    if elapsed >= 1.0:
        state.update({"active": to_index, "from": None, "factors": [1.0 if index == to_index else 0.0 for index in range(2)]})


def play_sound(sounds: dict[str, pygame.mixer.Sound | None], name: str) -> None:
    if not SOUND_OK:
        return
    sound = sounds.get(name)
    if sound is not None and bool(SETTINGS.get("sound_enabled", True)):
        sound.set_volume(float(SETTINGS.get("effects_volume", SETTINGS.get("volume", 0.5))))
        sound.play()


def start_drop_animation(row: int, col: int, piece: int) -> dict[str, float | int]:
    """Create a drop animation payload for a token entering the board."""
    _, target_y = board_pixel_position(row, col)
    start_y = float(TOP_BAR_HEIGHT // 2)
    return {
        "row": row,
        "col": col,
        "piece": piece,
        "y": start_y,
        "start_y": start_y,
        "target_y": float(target_y),
        "velocity": DROP_START_VELOCITY,
        "gravity": DROP_GRAVITY,
        "max_velocity": DROP_MAX_VELOCITY,
        "bounced": False,
    }


def ai_controls_piece(mode: int, piece: int) -> bool:
    return mode != MODE_PVP and piece == AI


def start_ai_worker(state: dict[str, object]) -> None:
    if state.get("ai_worker_running") or state["game_over"] or state["animation"] is not None:
        return

    board_snapshot = copy_board(state["board"])
    board_snapshot_key = board_key(board_snapshot)
    difficulty = state["difficulty"]
    request_id = int(state.get("ai_request_id", 0)) + 1
    state["ai_request_id"] = request_id
    state["ai_worker_running"] = True
    state["ai_pending_board"] = board_snapshot_key
    state["ai_result"] = None

    def worker() -> None:
        try:
            column = get_ai_move(board_snapshot, difficulty)
        except Exception:
            column = None
        state["ai_result"] = (request_id, board_snapshot_key, column)
        state["ai_worker_running"] = False

    threading.Thread(target=worker, daemon=True).start()


def create_new_match(mode: int, difficulty: int | None = None) -> dict[str, object]:
    board = create_board()
    turn = AI if mode == MODE_AI_FIRST else PLAYER
    return {
        "mode": mode,
        "difficulty": difficulty,
        "board": board,
        "turn": turn,
        "status_message": status_message_for_turn(mode, turn),
        "result_message": "",
        "game_over": False,
        "ai_due_at": pygame.time.get_ticks() + AI_DELAY_MS if ai_controls_piece(mode, turn) else None,
        "animation": None,
        "winning_cells": None,
        "win_flash_visible": True,
        "win_flash_elapsed": 0.0,
        "win_flash_toggles": 0,
        "end_screen_at": None,
        "pending_sounds": [],
        "rewarded": False,
        "reward_tokens": 0,
        "score_awarded": False,
        "ai_worker_running": False,
        "ai_result": None,
        "ai_request_id": 0,
        "ai_pending_board": None,
    }


def finish_turn(state: dict[str, object], piece: int) -> None:
    board = state["board"]
    mode = state["mode"]
    winning_cells = get_winning_cells(board, piece)
    if winning_cells is not None:
        state["game_over"] = True
        state["winning_cells"] = winning_cells
        state["win_flash_visible"] = True
        state["win_flash_elapsed"] = 0.0
        state["win_flash_toggles"] = 0
        state["end_screen_at"] = None
        state["pending_sounds"].append("loss" if mode != MODE_PVP and piece == AI else "win")
        if mode == MODE_PVP:
            state["result_message"] = f"Player {piece} wins!"
        else:
            if piece == PLAYER:
                reward = reward_for_difficulty(state["difficulty"])
                state["reward_tokens"] = reward
                if reward > 0 and not bool(state["rewarded"]):
                    PLAYER_DATA["tokens"] = int(PLAYER_DATA.get("tokens", 0)) + reward
                    state["rewarded"] = True
                    state["result_message"] = f"You win! +{reward} points"
                else:
                    state["result_message"] = "You win!"
                if not bool(state["score_awarded"]):
                    PLAYER_DATA["ai_score"] = int(PLAYER_DATA.get("ai_score", 0)) + ai_match_points("win")
                    state["score_awarded"] = True
            else:
                state["result_message"] = "AI wins!"
                if not bool(state["score_awarded"]):
                    PLAYER_DATA["ai_score"] = int(PLAYER_DATA.get("ai_score", 0)) + ai_match_points("loss")
                    state["score_awarded"] = True
            save_progress()
        state["status_message"] = state["result_message"]
        state["ai_due_at"] = None
        state["ai_result"] = None
        state["ai_pending_board"] = None
        return

    if board_full(board):
        state["game_over"] = True
        state["winning_cells"] = None
        state["pending_sounds"].append("draw")
        draw_reward = 0
        if mode != MODE_PVP:
            draw_reward = draw_reward_for_difficulty(state["difficulty"])
            state["reward_tokens"] = draw_reward
            if draw_reward > 0 and not bool(state["rewarded"]):
                PLAYER_DATA["tokens"] = int(PLAYER_DATA.get("tokens", 0)) + draw_reward
                state["rewarded"] = True
                state["result_message"] = f"Draw! +{draw_reward} points"
            else:
                state["result_message"] = "Draw!"
        else:
            state["result_message"] = "Draw!"
        state["status_message"] = state["result_message"]
        state["ai_due_at"] = None
        state["ai_result"] = None
        state["ai_pending_board"] = None
        if mode != MODE_PVP and not bool(state["score_awarded"]):
            PLAYER_DATA["ai_score"] = int(PLAYER_DATA.get("ai_score", 0)) + ai_match_points("draw")
            state["score_awarded"] = True
        save_progress()
        return

    next_piece = next_turn(piece)
    state["turn"] = next_piece
    state["status_message"] = status_message_for_turn(mode, next_piece)
    if ai_controls_piece(mode, next_piece):
        state["ai_due_at"] = pygame.time.get_ticks() + AI_DELAY_MS
        state["ai_result"] = None
        state["ai_pending_board"] = None
    else:
        state["ai_due_at"] = None
        state["ai_result"] = None
        state["ai_pending_board"] = None


def update_win_flash(state: dict[str, object], dt: float) -> bool:
    if not state["game_over"] or state["winning_cells"] is None:
        return False
    if state["win_flash_toggles"] >= WIN_FLASH_TOGGLES:
        state["win_flash_visible"] = True
        return True

    state["win_flash_elapsed"] += dt
    if state["win_flash_elapsed"] >= WIN_FLASH_INTERVAL:
        state["win_flash_elapsed"] = 0.0
        state["win_flash_visible"] = not state["win_flash_visible"]
        state["win_flash_toggles"] += 1
    return state["win_flash_toggles"] >= WIN_FLASH_TOGGLES


def update_animation(state: dict[str, object], dt: float) -> None:
    """Advance the active drop animation and settle the piece onto the board."""
    animation = state["animation"]
    if animation is None:
        return

    animation["velocity"] += animation["gravity"] * dt
    if animation["velocity"] > animation["max_velocity"]:
        animation["velocity"] = animation["max_velocity"]
    animation["y"] += animation["velocity"] * dt
    if animation["y"] >= animation["target_y"]:
        if not bool(animation.get("bounced")) and float(animation["velocity"]) > DROP_MIN_BOUNCE_SPEED:
            overshoot = min(8.0, (float(animation["y"]) - float(animation["target_y"])) * 0.35 + 2.0)
            animation["y"] = float(animation["target_y"]) - overshoot
            animation["velocity"] = -float(animation["velocity"]) * DROP_BOUNCE_DAMPING
            animation["bounced"] = True
            return

        animation["y"] = animation["target_y"]
        board = state["board"]
        drop_piece(board, int(animation["row"]), int(animation["col"]), int(animation["piece"]))
        state["animation"] = None
        state["pending_sounds"].append("drop")
        finish_turn(state, int(animation["piece"]))


def begin_move(state: dict[str, object], col: int) -> bool:
    board = state["board"]
    turn = int(state["turn"])
    if not is_valid_location(board, col):
        return False
    row = get_next_open_row(board, col)
    if row is None:
        return False
    state["animation"] = start_drop_animation(row, col, turn)
    state["ai_due_at"] = None
    state["ai_result"] = None
    state["ai_pending_board"] = None
    return True


def update_ai_turn(state: dict[str, object], now: int) -> None:
    if state["game_over"] or state["animation"] is not None:
        return
    if not ai_controls_piece(int(state["mode"]), int(state["turn"])):
        return
    ai_due_at = state["ai_due_at"]
    if ai_due_at is None or now < int(ai_due_at):
        return
    current_board_key = board_key(state["board"])
    ai_result = state.get("ai_result")

    if ai_result is not None:
        request_id, result_board_key, col = ai_result
        if result_board_key == current_board_key and request_id == state.get("ai_request_id"):
            fallback_moves = order_moves(state["board"], get_valid_locations(state["board"]), AI)
            chosen_col = int(col) if isinstance(col, int) and col in fallback_moves else None
            if chosen_col is not None and begin_move(state, chosen_col):
                return
            if fallback_moves:
                begin_move(state, fallback_moves[0])
            return

    if state.get("ai_worker_running"):
        return

    pending_board = state.get("ai_pending_board")
    if pending_board != current_board_key:
        start_ai_worker(state)


def draw_playing_screen(
    screen: pygame.Surface,
    state: dict[str, object],
    font: pygame.font.Font,
    mouse_pos: tuple[int, int],
) -> None:
    difficulty_text = show_difficulty(int(state["mode"]), state["difficulty"])
    label = f"{difficulty_text} | {state['status_message']}" if difficulty_text else str(state["status_message"])
    draw_board(screen, state["board"], font, label)

    if state["winning_cells"] is not None and state["win_flash_visible"]:
        draw_winning_highlight(screen, state["winning_cells"])

    if state["animation"] is None and not state["game_over"] and not ai_controls_piece(int(state["mode"]), int(state["turn"])):
        hover_col = column_from_x(mouse_pos[0])
        if hover_col is not None and is_valid_location(state["board"], hover_col):
            draw_disc(screen, BOARD_LEFT + hover_col * CELL_SIZE + CELL_SIZE // 2, TOP_BAR_HEIGHT // 2, int(state["turn"]), scale=1.1, glow_alpha=60)

    animation = state["animation"]
    if animation is not None:
        draw_falling_piece(
            screen,
            int(animation["col"]),
            float(animation["y"]),
            int(animation["piece"]),
        )


def play_game_pygame(depth: int = DEFAULT_DEPTH) -> None:
    if pygame is None:
        raise RuntimeError("pygame is not installed. Install it with: pip install pygame")

    global RED_TOKEN, BLUE_TOKEN, SOUND_OK

    try:
        pygame.mixer.quit()
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(8)
        pygame.mixer.set_reserved(2)
        SOUND_OK = True
    except Exception:
        pygame.init()
        SOUND_OK = False
    mobile_device = sys.platform == "android"
    display_flags = pygame.FULLSCREEN if mobile_device else pygame.RESIZABLE
    display_surface = pygame.display.set_mode((0, 0), display_flags) if mobile_device else pygame.display.set_mode((WIDTH, HEIGHT), display_flags)
    pygame.display.set_caption("Gravity 4")
    # Render in the game's stable design coordinate space, then fit it to the
    # available window. This keeps every layout and hit target in sync.
    screen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def fitted_viewport() -> tuple[pygame.Rect, float]:
        window_w, window_h = display_surface.get_size()
        scale = min(window_w / WIDTH, window_h / HEIGHT)
        view_w = max(1, int(WIDTH * scale))
        view_h = max(1, int(HEIGHT * scale))
        return pygame.Rect((window_w - view_w) // 2, (window_h - view_h) // 2, view_w, view_h), scale

    def to_design_point(point: tuple[int, int]) -> tuple[int, int]:
        viewport, scale = fitted_viewport()
        x, y = point
        if not viewport.collidepoint(x, y):
            return -1, -1
        return int((x - viewport.left) / scale), int((y - viewport.top) / scale)
    RED_TOKEN = load_token_image("red_token.png")
    BLUE_TOKEN = load_token_image("blue_token.png")
    title_font = get_font(size=60, bold=False)
    font = get_font(size=40, bold=False)
    small_font = get_font(size=22, bold=False)
    clock = pygame.time.Clock()
    load_progress()
    sounds = init_sounds() if SOUND_OK else {}
    lobby_music = create_menu_music() if SOUND_OK else None
    game_music = create_game_music() if SOUND_OK else None
    music_channels = (pygame.mixer.Channel(0), pygame.mixer.Channel(1)) if SOUND_OK else None
    music_state: dict[str, object] = {}
    set_volume_for_sounds(sounds)
    game_state = STATE_MENU
    match_state: dict[str, object] | None = None
    selected_mode: int | None = None
    fade_alpha = 255.0
    active_slider: str | None = None
    paused_game_state: str | None = None
    pause_started_at: int | None = None
    pause_overlay_alpha = 0.0
    last_touch_at = -1000

    def touch_point(point: tuple[int, int]) -> tuple[int, int]:
        """Give undersized controls a 48 px physical touch area on phones."""
        design_point = to_design_point(point)
        viewport, scale = fitted_viewport()
        del viewport
        if scale >= 1.0 or design_point == (-1, -1):
            return design_point

        targets: list[tuple[pygame.Rect, bool]] = []
        if game_state == STATE_MENU:
            targets = [(rect, False) for rect, _, _ in start_screen_buttons()]
        elif game_state == STATE_PLAY_MENU:
            targets = [(rect, False) for rect, _, _ in play_menu_buttons()]
        elif game_state == STATE_AI_MENU:
            targets = [(rect, False) for rect, _, _ in ai_menu_buttons()]
        elif game_state == STATE_DIFFICULTY:
            targets = [(rect, False) for rect, _, _ in difficulty_buttons()]
            targets.append((difficulty_back_button_rect(), False))
        elif game_state == STATE_SETTINGS:
            targets = [
                (settings_back_button_rect(), False),
                (settings_slider_rect(0), True),
                (settings_slider_rect(1), True),
                (settings_toggle_rect(0), False),
                (settings_toggle_rect(1), False),
            ]
        elif game_state == STATE_GAME:
            targets = [(pause_button_rect(), False)]
        elif game_state == STATE_GAME_OVER:
            targets = [(rect, False) for rect in game_over_button_rects()]
        elif game_state == STATE_PAUSED:
            _, continue_rect, menu_rect, slider_rect = pause_layout_rects()
            targets = [(continue_rect, False), (menu_rect, False), (slider_rect, True)]

        if not targets:
            return design_point
        min_design_size = math.ceil(48 / scale)
        x, y = design_point
        expanded_targets: list[tuple[int, pygame.Rect, bool]] = []
        for rect, is_slider in targets:
            if rect.collidepoint(design_point):
                return design_point
            extra_w = max(0, min_design_size - rect.width)
            extra_h = max(0, min_design_size - rect.height)
            hit_rect = rect.inflate(extra_w, extra_h)
            if hit_rect.collidepoint(design_point):
                nearest_x = max(rect.left, min(x, rect.right))
                nearest_y = max(rect.top, min(y, rect.bottom))
                distance = (x - nearest_x) ** 2 + (y - nearest_y) ** 2
                expanded_targets.append((distance, rect, is_slider))
        if not expanded_targets:
            return design_point
        _, rect, is_slider = min(expanded_targets, key=lambda item: item[0])
        if is_slider:
            return max(rect.left, min(x, rect.right)), rect.centery
        return rect.center

    while True:
        dt = clock.tick(FPS) / 1000.0
        now = pygame.time.get_ticks()
        mouse_pos = to_design_point(pygame.mouse.get_pos())
        active_buttons = [(rect, mode) for rect, mode, _ in start_screen_buttons()]
        play_buttons = [(rect, mode) for rect, mode, _ in play_menu_buttons()]
        ai_buttons = [(rect, mode) for rect, mode, _ in ai_menu_buttons()]
        difficulty_options = [(rect, difficulty) for rect, difficulty, _ in difficulty_buttons()]
        difficulty_back_button = difficulty_back_button_rect()
        restart_button = restart_button_rect()
        main_menu_button = main_menu_button_rect()
        settings_back_button = settings_back_button_rect()
        settings_slider = settings_slider_rect(0)
        music_slider = settings_slider_rect(1)
        settings_toggle = settings_toggle_rect(0)
        music_toggle = settings_toggle_rect(1)
        pause_button = pause_button_rect()
        pause_continue_button = pause_continue_button_rect()
        pause_menu_button = pause_menu_button_rect()
        pause_volume_slider = pause_slider_rect()

        for event in pygame.event.get():
            if event.type in (pygame.VIDEORESIZE, getattr(pygame, "WINDOWRESIZED", -1)):
                new_size = (max(1, event.w), max(1, event.h))
                if not mobile_device:
                    display_surface = pygame.display.set_mode(new_size, pygame.RESIZABLE)
                continue
            if event.type in (getattr(pygame, "FINGERDOWN", -1), getattr(pygame, "FINGERUP", -1), getattr(pygame, "FINGERMOTION", -1)):
                window_w, window_h = display_surface.get_size()
                finger_point = touch_point((int(event.x * window_w), int(event.y * window_h)))
                if event.type == getattr(pygame, "FINGERDOWN", -1):
                    last_touch_at = now
                translated_type = pygame.MOUSEBUTTONDOWN if event.type == getattr(pygame, "FINGERDOWN", -1) else pygame.MOUSEBUTTONUP if event.type == getattr(pygame, "FINGERUP", -1) else pygame.MOUSEMOTION
                event = pygame.event.Event(translated_type, {"pos": finger_point, "button": 1, "buttons": (1, 0, 0), "rel": (0, 0)})
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                if event.type == pygame.MOUSEBUTTONDOWN and now - last_touch_at < 350:
                    continue  # Ignore SDL's duplicate mouse event for the same touch.
                event = pygame.event.Event(event.type, {**event.dict, "pos": to_design_point(event.pos)})
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button != 1:
                continue

            if event.type == pygame.MOUSEBUTTONUP:
                if active_slider is not None:
                    save_progress()
                active_slider = None

            if event.type == pygame.MOUSEMOTION and game_state == STATE_SETTINGS and active_slider is not None:
                if active_slider == "effects_volume":
                    update_setting_volume_from_mouse(settings_slider, event.pos[0], "effects_volume", persist=False)
                    set_volume_for_sounds(sounds)
                elif active_slider == "music_volume":
                    update_setting_volume_from_mouse(music_slider, event.pos[0], "music_volume", persist=False)
                continue


            if event.type == pygame.MOUSEMOTION and game_state == STATE_PAUSED and active_slider == "pause_volume":
                update_setting_volume_from_mouse(pause_volume_slider, event.pos[0], "effects_volume", persist=False)
                SETTINGS["volume"] = SETTINGS["effects_volume"]
                set_volume_for_sounds(sounds)
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_MENU:
                if event.button == 1:
                    play_sound(sounds, "click")
                for rect, mode in active_buttons:
                    if rect.collidepoint(event.pos):
                        if mode == ACTION_PLAY:
                            game_state = STATE_PLAY_MENU
                            play_sound(sounds, "transition")
                        elif mode == ACTION_SETTINGS:
                            game_state = STATE_SETTINGS
                            play_sound(sounds, "transition")
                        fade_alpha = 255.0
                        break
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_PLAY_MENU:
                if event.button == 1:
                    play_sound(sounds, "click")
                for rect, mode in play_buttons:
                    if rect.collidepoint(event.pos):
                        if mode == ACTION_PLAY:
                            game_state = STATE_AI_MENU
                            play_sound(sounds, "transition")
                        elif mode == MODE_PVP:
                            selected_mode = int(mode)
                            match_state = create_new_match(int(mode), None)
                            game_state = STATE_GAME
                            play_sound(sounds, "transition")
                        elif mode == ACTION_BACK:
                            game_state = STATE_MENU
                        else:
                            game_state = str(mode)
                        fade_alpha = 255.0
                        break
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_AI_MENU:
                if event.button == 1:
                    play_sound(sounds, "click")
                for rect, mode in ai_buttons:
                    if rect.collidepoint(event.pos):
                        if mode == MODE_AI_FIRST or mode == MODE_AI_SECOND:
                            selected_mode = int(mode)
                            game_state = STATE_DIFFICULTY
                            play_sound(sounds, "transition")
                        else:
                            game_state = str(mode)
                        fade_alpha = 255.0
                        break
                continue


            if event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_SETTINGS:
                if event.button == 1:
                    play_sound(sounds, "click")
                if settings_back_button.collidepoint(event.pos):
                    game_state = STATE_MENU
                    play_sound(sounds, "transition")
                    fade_alpha = 255.0
                    continue
                if settings_slider.inflate(0, 28).collidepoint(event.pos):
                    active_slider = "effects_volume"
                    update_setting_volume_from_mouse(settings_slider, event.pos[0], "effects_volume")
                    set_volume_for_sounds(sounds)
                    continue
                if music_slider.inflate(0, 28).collidepoint(event.pos):
                    active_slider = "music_volume"
                    update_setting_volume_from_mouse(music_slider, event.pos[0], "music_volume")
                    continue
                if settings_toggle.collidepoint(event.pos):
                    SETTINGS["sound_enabled"] = not bool(SETTINGS.get("sound_enabled", True))
                    set_volume_for_sounds(sounds)
                    save_progress()
                    continue
                if music_toggle.collidepoint(event.pos):
                    SETTINGS["music_enabled"] = not bool(SETTINGS.get("music_enabled", True))
                    save_progress()
                    continue
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_DIFFICULTY:
                if event.button == 1:
                    play_sound(sounds, "click")
                if difficulty_back_button.collidepoint(event.pos):
                    game_state = STATE_AI_MENU
                    play_sound(sounds, "transition")
                    fade_alpha = 255.0
                    continue
                if selected_mode is not None:
                    for rect, difficulty in difficulty_options:
                        if rect.collidepoint(event.pos):
                            match_state = create_new_match(selected_mode, difficulty)
                            game_state = STATE_GAME
                            play_sound(sounds, "transition")
                            fade_alpha = 255.0
                            break
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_GAME_OVER:
                if event.button == 1:
                    play_sound(sounds, "click")
                if restart_button and restart_button.collidepoint(event.pos) and match_state is not None:
                    match_state = create_new_match(int(match_state["mode"]), match_state["difficulty"])
                    game_state = STATE_GAME
                    play_sound(sounds, "transition")
                    fade_alpha = 255.0
                    continue
                if main_menu_button and main_menu_button.collidepoint(event.pos):
                    match_state = None
                    selected_mode = None
                    game_state = STATE_MENU
                    play_sound(sounds, "transition")
                    fade_alpha = 255.0
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_PAUSED:
                if event.button == 1:
                    play_sound(sounds, "click")
                if pause_continue_button.collidepoint(event.pos):
                    game_state = paused_game_state or STATE_GAME
                    if pause_started_at is not None and match_state is not None:
                        pause_duration = now - pause_started_at
                        if match_state["ai_due_at"] is not None:
                            match_state["ai_due_at"] = int(match_state["ai_due_at"]) + pause_duration
                        if match_state["end_screen_at"] is not None:
                            match_state["end_screen_at"] = int(match_state["end_screen_at"]) + pause_duration
                    paused_game_state = None
                    pause_started_at = None
                    continue
                if pause_menu_button.collidepoint(event.pos):
                    match_state = None
                    selected_mode = None
                    game_state = STATE_MENU
                    play_sound(sounds, "transition")
                    paused_game_state = None
                    pause_started_at = None
                    pause_overlay_alpha = 0.0
                    fade_alpha = 255.0
                    continue
                if pause_volume_slider.inflate(0, 28).collidepoint(event.pos):
                    active_slider = "pause_volume"
                    update_setting_volume_from_mouse(pause_volume_slider, event.pos[0], "effects_volume")
                    SETTINGS["volume"] = SETTINGS["effects_volume"]
                    set_volume_for_sounds(sounds)
                    continue

            if game_state not in {STATE_GAME}:
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and match_state is not None:
                if pause_button.collidepoint(event.pos):
                    play_sound(sounds, "click")
                    paused_game_state = game_state
                    game_state = STATE_PAUSED
                    pause_started_at = now
                    continue
                if match_state["game_over"] or match_state["animation"] is not None:
                    continue
                if ai_controls_piece(int(match_state["mode"]), int(match_state["turn"])):
                    continue

                col = column_from_x(event.pos[0])
                if col is None:
                    continue
                begin_move(match_state, col)

        if game_state == STATE_PAUSED:
            pause_overlay_alpha = min(190.0, pause_overlay_alpha + dt * 520.0)
        else:
            pause_overlay_alpha = max(0.0, pause_overlay_alpha - dt * 520.0)

        if game_state == STATE_GAME and match_state is not None:
            update_animation(match_state, dt)
            update_ai_turn(match_state, now)
            while match_state["pending_sounds"]:
                play_sound(sounds, match_state["pending_sounds"].pop(0))
            if match_state["game_over"]:
                if match_state["winning_cells"] is not None:
                    game_state = STATE_WIN_ANIMATION
                else:
                    game_state = STATE_GAME_OVER
                fade_alpha = 255.0
        elif game_state == STATE_WIN_ANIMATION and match_state is not None:
            if update_win_flash(match_state, dt):
                match_state["win_flash_visible"] = True
                match_state["end_screen_at"] = now + END_SCREEN_DELAY_MS
                game_state = STATE_WIN_PAUSE
        elif game_state == STATE_WIN_PAUSE and match_state is not None:
            if match_state["end_screen_at"] is not None and now >= int(match_state["end_screen_at"]):
                game_state = STATE_GAME_OVER
                fade_alpha = 255.0

        if game_state == STATE_MENU:
            active_buttons = draw_start_screen(screen, title_font, small_font, font, mouse_pos)
        elif game_state == STATE_PLAY_MENU:
            play_buttons = draw_play_menu_screen(screen, title_font, small_font, font, mouse_pos)
        elif game_state == STATE_AI_MENU:
            ai_buttons = draw_ai_menu_screen(screen, title_font, small_font, font, mouse_pos)
        elif game_state == STATE_DIFFICULTY and selected_mode is not None:
            difficulty_options, difficulty_back_button = draw_difficulty_screen(
                screen, title_font, small_font, font, mouse_pos, selected_mode
            )
        elif game_state == STATE_SETTINGS:
            (settings_back_button, settings_slider, settings_toggle,
             music_slider, music_toggle) = draw_settings_screen(
                screen, title_font, small_font, font, mouse_pos
            )
        elif game_state in {STATE_GAME, STATE_WIN_ANIMATION, STATE_WIN_PAUSE} and match_state is not None:
            draw_playing_screen(screen, match_state, small_font, mouse_pos)
            draw_pause_button(screen, small_font, mouse_pos)
        elif game_state == STATE_GAME_OVER and match_state is not None:
            restart_button, main_menu_button = draw_game_over_screen(
                screen, match_state["board"], str(match_state["result_message"]),
                title_font, small_font, font, mouse_pos,
                match_state.get("winning_cells"), bool(match_state.get("win_flash_visible", True)),
            )
        elif game_state == STATE_PAUSED and match_state is not None:
            draw_playing_screen(screen, match_state, small_font, mouse_pos)
            draw_pause_overlay(screen, small_font, font, mouse_pos, pause_overlay_alpha)

        if fade_alpha > 0:
            draw_fade_overlay(screen, fade_alpha)
            fade_alpha = max(0.0, fade_alpha - FADE_SPEED * dt)

        if music_channels is not None:
            sync_music(
                lobby_music,
                game_music,
                music_channels,
                game_state in {STATE_GAME, STATE_WIN_ANIMATION, STATE_WIN_PAUSE, STATE_PAUSED},
                dt,
                music_state,
            )
        viewport, _ = fitted_viewport()
        display_surface.fill((4, 7, 13))
        scaled_frame = pygame.transform.smoothscale(screen, viewport.size)
        display_surface.blit(scaled_frame, viewport.topleft)
        pygame.display.flip()


if __name__ == "__main__":
    if "--terminal" in sys.argv:
        play_game()
    else:
        play_game_pygame()
