lyrics = []


def update(data):
    global lyrics

    lyrics = data.get(
        "lyrics",
        []
    )


def get():

    return {
        "lyrics": lyrics
    }


def get_current(time_ms=None):

    if not lyrics:

        return {
            "prev": "",
            "current": "",
            "next": "",
            "instrumental": False,
            "index": -1
        }


    if time_ms is None:

        return {
            "prev": "",
            "current": "",
            "next": "",
            "instrumental": True,
            "index": -1
        }


    current_index = -1


    for i, line in enumerate(lyrics):

        try:

            start_time = float(
                line.get(
                    "start_time",
                    0
                )
            )

            end_time = float(
                line.get(
                    "end_time",
                    0
                )
            )

        except (
            TypeError,
            ValueError
        ):

            continue


        if (
            start_time <= time_ms
            and time_ms < end_time
        ):

            current_index = i
            break


    # ==============================================
    # INSTRUMENTAL / GAP
    # ==============================================

    if current_index == -1:

        return {
            "prev": "",
            "current": "",
            "next": "",
            "instrumental": True,
            "index": -1
        }


    # ==============================================
    # CURRENT
    # ==============================================

    current_line = lyrics[current_index]


    prev_text = ""

    next_text = ""


    if current_index > 0:

        prev_text = (
            lyrics[current_index - 1].get(
                "text",
                ""
            )
            or ""
        )


    if current_index < len(lyrics) - 1:

        next_text = (
            lyrics[current_index + 1].get(
                "text",
                ""
            )
            or ""
        )


    return {
        "prev": prev_text,

        "current": (
            current_line.get(
                "text",
                ""
            )
            or ""
        ),

        "next": next_text,

        "instrumental": False,

        "index": current_index
    }