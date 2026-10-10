//calls data from the server
if (async_load[? "http_status"] == 200) {
    ParseEmotionResponse(async_load[? "result"]);
} else {
    global.emotion_data.status = "http-error";
    global.emotion_data.last_result = "error";
    global.emotion_data.pending = false;
}