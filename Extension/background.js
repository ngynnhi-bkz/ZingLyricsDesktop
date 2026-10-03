const API = "http://127.0.0.1:8001";


chrome.runtime.onMessage.addListener(
    (message, sender, sendResponse) => {

        if (!message || !message.type) {
            return;
        }


        // ==================================================
        // PLAYER UPDATE
        // ==================================================

        if (message.type === "PLAYER_UPDATE") {

            fetch(`${API}/player/update`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(message.data)
            })
                .then(response => {

                    if (!response.ok) {
                        throw new Error(
                            `HTTP ${response.status}`
                        );
                    }

                    return response.json();
                })
                .then(data => {

                    sendResponse({
                        success: true,
                        data: data
                    });

                })
                .catch(error => {

                    console.error(
                        "[ZingLyricsDesktop] Player API error:",
                        error
                    );

                    sendResponse({
                        success: false,
                        error: error.message
                    });

                });

            return true;
        }


        // ==================================================
        // LYRICS UPDATE
        // ==================================================

        if (message.type === "LYRICS_UPDATE") {

            fetch(`${API}/lyrics/update`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(message.data)
            })
                .then(response => {

                    if (!response.ok) {
                        throw new Error(
                            `HTTP ${response.status}`
                        );
                    }

                    return response.json();
                })
                .then(data => {

                    sendResponse({
                        success: true,
                        data: data
                    });

                })
                .catch(error => {

                    console.error(
                        "[ZingLyricsDesktop] Lyrics API error:",
                        error
                    );

                    sendResponse({
                        success: false,
                        error: error.message
                    });

                });

            return true;
        }


        // ==================================================
        // FETCH ZINGMP3 LYRIC URL
        // ==================================================

        if (message.type === "FETCH_LYRICS_URL") {

            const url = message.url;

            if (!url) {

                sendResponse({
                    success: false,
                    error: "Missing lyric URL"
                });

                return;
            }


            fetch(url, {
                method: "GET",
                credentials: "include",
                cache: "no-store"
            })
                .then(response => {

                    if (!response.ok) {
                        throw new Error(
                            `Lyrics HTTP ${response.status}`
                        );
                    }

                    return response.json();
                })
                .then(data => {

                    sendResponse({
                        success: true,
                        data: data
                    });

                })
                .catch(error => {

                    console.error(
                        "[ZingLyricsDesktop] Fetch lyric error:",
                        error
                    );

                    sendResponse({
                        success: false,
                        error: error.message
                    });

                });

            return true;
        }
    }
);