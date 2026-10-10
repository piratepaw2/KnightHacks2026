function StartEmotionDebug() {
    if (!variable_global_exists("emotion_debug")) {
        global.emotion_debug = {
            status: "idle",
            last_result: "unknown",
            last_update: 0,
            pending: false,
            request_count: 0,
        };
    }

    global.emotion_debug.status = "ready";
    global.emotion_debug.last_result = "waiting";
    RequestEmotion();
}
