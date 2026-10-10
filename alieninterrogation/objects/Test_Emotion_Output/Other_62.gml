if (async_load[? "http_status"] == 200) {
    ParseEmotionResponse(async_load[? "result"]);
} else {
    global.emotion_debug.status = "http-error";
    global.emotion_debug.last_result = "error";
    global.emotion_debug.pending = false;
}