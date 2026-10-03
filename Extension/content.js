/* ==========================================================
   ZingLyricsDesktop - ZingMP3 Content Script
   ========================================================== */

let stopped = false;

let lastSong = "";

let lastLyricsUrl = "";

let lastLyricsSignature = "";


/* ==========================================================
   SAFE MESSAGE
   ========================================================== */

function safeSendMessage(message, callback) {

    if (stopped) {
        return;
    }

    try {

        chrome.runtime.sendMessage(
            message,
            response => {

                if (chrome.runtime.lastError) {

                    const error =
                        chrome.runtime.lastError.message || "";

                    if (
                        error.includes(
                            "Extension context invalidated"
                        )
                    ) {

                        stopped = true;

                        return;
                    }

                    return;
                }

                if (callback) {
                    callback(response);
                }
            }
        );

    } catch (error) {

        if (
            String(error).includes(
                "Extension context invalidated"
            )
        ) {

            stopped = true;

            return;
        }
    }
}


/* ==========================================================
   STOP
   ========================================================== */

function stopExtensionContext() {

    stopped = true;
}


/* ==========================================================
   FIND AUDIO
   ========================================================== */

function getAudio() {

    const audio =
        document.querySelector("audio");

    return audio || null;
}


/* ==========================================================
   GET SONG INFO
   ========================================================== */

function getSongInfo(audio) {

    let title = "";

    let artist = "";

    let url = "";


    const selectorsTitle = [

        ".song-title",

        ".player-title",

        ".song-info .title",

        '[class*="song-title"]',

        '[class*="song-info"] .title'
    ];


    for (const selector of selectorsTitle) {

        const element =
            document.querySelector(selector);

        if (
            element &&
            element.textContent.trim()
        ) {

            title =
                element.textContent.trim();

            break;
        }
    }


    const selectorsArtist = [

        ".song-artist",

        ".player-artist",

        ".song-info .artist",

        '[class*="song-artist"]',

        '[class*="song-info"] .artist'
    ];


    for (const selector of selectorsArtist) {

        const element =
            document.querySelector(selector);

        if (
            element &&
            element.textContent.trim()
        ) {

            artist =
                element.textContent.trim();

            break;
        }
    }


    if (!title) {

        const titleElement =
            document.querySelector("title");

        if (titleElement) {

            title =
                titleElement.textContent
                    .replace(
                        /\s*\|\s*Zing MP3.*$/i,
                        ""
                    )
                    .trim();
        }
    }


    if (audio) {

        url =
            audio.src || "";
    }


    return {
        title,
        artist,
        url
    };
}


/* ==========================================================
   PLAYER UPDATE
   ========================================================== */

function sendPlayer(audio) {

    if (!audio) {
        return;
    }


    const info =
        getSongInfo(audio);


    safeSendMessage({

        type: "PLAYER_UPDATE",

        data: {

            title:
                info.title,

            url:
                info.url,

            artist:
                info.artist,

            current_time:
                Number(audio.currentTime) || 0,

            duration:
                Number(audio.duration) || 0,

            playing:
                !audio.paused &&
                !audio.ended
        }
    });
}


/* ==========================================================
   PARSE LYRICS
   ========================================================== */

function parseLyricsResponse(payload) {

    const sentences =

        payload &&
        payload.data &&
        Array.isArray(payload.data.sentences)

            ? payload.data.sentences

            : [];


    const result = [];


    for (const sentence of sentences) {

        const words =

            Array.isArray(sentence.words)
                ? sentence.words
                : [];


        if (!words.length) {
            continue;
        }


        const validWords =

            words.filter(word => {

                return (
                    word &&
                    typeof word.data === "string"
                );

            });


        if (!validWords.length) {
            continue;
        }


        const startTimes =

            validWords
                .map(word =>
                    Number(word.startTime)
                )
                .filter(Number.isFinite);


        const endTimes =

            validWords
                .map(word =>
                    Number(word.endTime)
                )
                .filter(Number.isFinite);


        if (
            !startTimes.length ||
            !endTimes.length
        ) {
            continue;
        }


        const startTime =
            Math.min(...startTimes);


        const endTime =
            Math.max(...endTimes);


        const text =

            validWords
                .map(word =>
                    String(word.data).trim()
                )
                .filter(Boolean)
                .join(" ")
                .trim();


        if (!text) {
            continue;
        }


        if (
            !Number.isFinite(startTime) ||
            !Number.isFinite(endTime)
        ) {
            continue;
        }


        if (endTime < startTime) {
            continue;
        }


        result.push({

            text: text,

            start_time: startTime,

            end_time: endTime,

            words: validWords
        });
    }


    return result;
}


/* ==========================================================
   FIND LYRIC REQUEST
   ========================================================== */

function findLyricResourceUrl() {

    let entries = [];


    try {

        entries =
            performance.getEntriesByType(
                "resource"
            );

    } catch (error) {

        return null;
    }


    for (
        let i = entries.length - 1;
        i >= 0;
        i--
    ) {

        const entry =
            entries[i];


        if (
            !entry ||
            !entry.name
        ) {
            continue;
        }


        const url =
            String(entry.name);


        if (
            /\/lyric(?:\?|\/|$)/i.test(url)
        ) {

            return url;
        }
    }


    return null;
}


/* ==========================================================
   FETCH LYRICS
   ========================================================== */

function fetchLyrics() {

    if (stopped) {
        return;
    }


    const url =
        findLyricResourceUrl();


    if (!url) {
        return;
    }


    if (url === lastLyricsUrl) {
        return;
    }


    console.log(
        "[ZingLyricsDesktop] Found lyric URL:",
        url
    );


    lastLyricsUrl =
        url;


    safeSendMessage(

        {
            type:
                "FETCH_LYRICS_URL",

            url:
                url
        },

        response => {

            if (
                !response ||
                !response.success ||
                !response.data
            ) {

                console.warn(
                    "[ZingLyricsDesktop] Could not fetch lyrics."
                );

                return;
            }


            const lyrics =
                parseLyricsResponse(
                    response.data
                );


            if (!lyrics.length) {

                console.warn(
                    "[ZingLyricsDesktop] No timestamped lyrics."
                );

                return;
            }


            const signature =
                JSON.stringify(lyrics);


            if (
                signature === lastLyricsSignature
            ) {

                return;
            }


            lastLyricsSignature =
                signature;


            console.log(
                "[ZingLyricsDesktop] Lyrics loaded:",
                lyrics.length,
                "lines"
            );


            safeSendMessage({

                type:
                    "LYRICS_UPDATE",

                data: {
                    lyrics: lyrics
                }
            });
        }
    );
}


/* ==========================================================
   UPDATE
   ========================================================== */

function update() {

    if (stopped) {
        return;
    }


    const audio =
        getAudio();


    if (!audio) {
        return;
    }


    const info =
        getSongInfo(audio);


    /* ======================================================
       SONG CHANGED
       ====================================================== */

    if (
        info.title &&
        info.title !== lastSong
    ) {

        console.log(
            "[ZingLyricsDesktop] SONG CHANGED:",
            info.title
        );


        lastSong =
            info.title;


        /*
         * Không clearLyrics().
         *
         * Giữ lyric hiện tại trong khi lyric mới
         * đang được tải.
         */

        lastLyricsUrl =
            "";

        lastLyricsSignature =
            "";
    }


    /* ======================================================
       PLAYER
       ====================================================== */

    sendPlayer(audio);


    /* ======================================================
       LYRICS
       ====================================================== */

    fetchLyrics();
}


/* ==========================================================
   START
   ========================================================== */

function start() {

    console.log(
        "[ZingLyricsDesktop] Content script started."
    );


    // 100 ms
    setInterval(
        update,
        100
    );


    const observer =
        new MutationObserver(() => {

            if (!stopped) {
                update();
            }
        });


    observer.observe(
        document.documentElement,
        {
            childList: true,
            subtree: true
        }
    );


    update();
}


start();


