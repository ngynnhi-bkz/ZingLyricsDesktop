import sys
import requests

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QApplication

from ui import LyricsWindow


API = "http://127.0.0.1:8001"

app = QApplication(sys.argv)

print("QApplication OK")

window = LyricsWindow()

window.show()
window.raise_()
window.activateWindow()

print("Window showed")


# ==========================================================
# CACHE
# ==========================================================

session = requests.Session()

lyrics_cache = []

last_song_key = ""

pending_song_key = ""
pending_count = 0

SONG_CONFIRM_COUNT = 3

last_line_index = -1


# ==========================================================
# KARAOKE
# ==========================================================

STAR = "⋆ ⋆ ⋆"

GAP_MIN_MS = 750

LEAD_MS = 550


def get_line_index(lines, time_ms):

    if not lines:
        return -1

    current_index = -1

    for i, line in enumerate(lines):

        start = int(
            line.get("start_time", 0)
            or 0
        )

        if time_ms >= start:
            current_index = i
        else:
            break

    return current_index


def build_display(lines, index, time_ms):

    if not lines or index < 0:
        return None

    current_line = lines[index]

    current_start = int(
        current_line.get("start_time", 0) or 0
    )

    current_end = int(
        current_line.get("end_time", current_start)
        or current_start
    )

    prev_line = (
        lines[index - 1]
        if index > 0
        else None
    )

    next_line = (
        lines[index + 1]
        if index + 1 < len(lines)
        else None
    )

    following_line = (
        lines[index + 2]
        if index + 2 < len(lines)
        else None
    )

    # ==========================================
    # GAP SAU C?U HI?N T?I
    # ==========================================

    if next_line:

        next_start = int(
            next_line.get(
                "start_time",
                current_end
            )
            or current_end
        )

        gap = next_start - current_end

        # Tr??c khi c?u hi?n t?i k?t th?c
        if (
            time_ms >= current_end - LEAD_MS
            and time_ms < current_end
            and gap >= GAP_MIN_MS
        ):
            return {
                "prev": (
                    prev_line.get("text", "")
                    if prev_line
                    else ""
                ),
                "current": current_line.get(
                    "text", ""
                ),
                "next": STAR,
                "words": current_line.get(
                    "words", []
                ),
                "time_ms": time_ms
            }

        # ?ang trong kho?ng d?o
        if (
            time_ms >= current_end
            and time_ms < next_start
            and gap >= GAP_MIN_MS
        ):
            return {
                "prev": current_line.get(
                    "text", ""
                ),
                "current": STAR,
                "next": next_line.get(
                    "text", ""
                ),
                "words": [],
                "time_ms": time_ms
            }

        # C?u ti?p theo b?t ??u
        if (
            time_ms >= next_start
            and gap >= GAP_MIN_MS
        ):
            return {
                "prev": STAR,
                "current": next_line.get(
                    "text", ""
                ),
                "next": (
                    following_line.get("text", "")
                    if following_line
                    else ""
                ),
                "words": next_line.get(
                    "words", []
                ),
                "time_ms": time_ms
            }

    # ==========================================
    # C?U CU?I ?? K?T TH?C
    # ==========================================

    if (
        next_line is None
        and time_ms >= current_end
    ):
        return {
            "prev": "",
            "current": STAR,
            "next": "",
            "words": [],
            "time_ms": time_ms
        }

    # ==========================================
    # HI?N TH? B?NH TH??NG
    # ==========================================

    return {
        "prev": (
            prev_line.get("text", "")
            if prev_line
            else ""
        ),
        "current": current_line.get(
            "text", ""
        ),
        "next": (
            next_line.get("text", "")
            if next_line
            else ""
        ),
        "words": current_line.get(
            "words", []
        ),
        "time_ms": time_ms
    }

def update():

    global last_song_key
    global pending_song_key
    global pending_count
    global lyrics_cache
    global last_line_index

    try:

        # ==================================================
        # PLAYER
        # ==================================================

        response = session.get(
            f"{API}/player",
            timeout=0.5
        )

        if response.status_code != 200:
            return

        player = response.json()

        title = (
            player.get("title", "")
            or ""
        ).strip()

        url = (
            player.get("url", "")
            or ""
        ).strip()

        current_time = float(
            player.get(
                "current_time",
                0
            )
            or 0
        )

        if not title:
            return

        time_ms = int(
            current_time * 1000
        )

        # ==================================================
        # SONG KEY
        # ==================================================

        song_key = f"{title}|{url}"

        # ==================================================
        # SONG CHANGE
        # ==================================================

        if song_key == last_song_key:

            pending_song_key = ""
            pending_count = 0

        else:

            if song_key != pending_song_key:

                pending_song_key = song_key
                pending_count = 1

            else:

                pending_count += 1

            if pending_count < SONG_CONFIRM_COUNT:
                return

            print(
                "SONG CHANGED:",
                title
            )

            last_song_key = song_key

            pending_song_key = ""
            pending_count = 0

            lyrics_cache = []
            last_line_index = -1

            window.showUpdating()

        # ==================================================
        # LYRICS
        # ==================================================

        response = session.get(
            f"{API}/lyrics",
            timeout=0.5
        )

        if response.status_code != 200:
            return

        lyrics_data = response.json()

        lyrics_list = (
            lyrics_data.get(
                "lyrics",
                []
            )
            or []
        )

        if not lyrics_list:
            return

        # Cache lyrics
        if len(lyrics_list) != len(lyrics_cache):

            lyrics_cache = lyrics_list

        else:

            # cập nhật nếu API có thay đổi words
            lyrics_cache = lyrics_list

        if not lyrics_cache:
            return

        # ==================================================
        # CURRENT LINE
        # ==================================================

        index = get_line_index(
            lyrics_cache,
            time_ms
        )

        if index < 0:
            window.showInstrumental()
            return

        data = build_display(
            lyrics_cache,
            index,
            time_ms
        )

        if not data:
            return

        # ==================================================
        # UPDATE UI
        # ==================================================

        window.updateLyrics(data)

        last_line_index = index

    except Exception as e:

        print(
            "ERROR:",
            e
        )


# ==========================================================
# TIMER
# ==========================================================

timer = QTimer()

timer.setTimerType(
    Qt.PreciseTimer
)

timer.timeout.connect(update)

timer.start(50)


print("Entering event loop")

sys.exit(app.exec())


