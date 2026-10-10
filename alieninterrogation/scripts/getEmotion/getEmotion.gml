function RequestEmotion() {
    if (!variable_global_exists("emotion_debug")) {
        StartEmotionDebug();
    }

    if (global.emotion_debug.pending) {
        return;
    }

    global.emotion_debug.pending = true;
    global.emotion_debug.status = "requesting";
    global.emotion_debug.request_count += 1;
    http_get("http://127.0.0.1:5000/emotion");
}

function ParseEmotionResponse(_response) {
    var json = json_parse(_response);

    if (is_struct(json)) {
        if (variable_struct_exists(json, "emotion")) {
            global.emotion_debug.last_result = json[$ "emotion"];
        } else if (variable_struct_exists(json, "face_shape")) {
            global.emotion_debug.last_result = json[$ "face_shape"];
        } else {
            global.emotion_debug.last_result = "unknown";
        }

        global.emotion_debug.status = "ok";
    } else {
        global.emotion_debug.last_result = "error";
        global.emotion_debug.status = "invalid-json";
    }

    global.emotion_debug.pending = false;
    global.emotion_debug.last_update = current_time;
}

