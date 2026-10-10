//Changes the global emotion data 
function RequestEmotion() {
	
	//explicit call may not be required for start emotion protocol. 
    if (!variable_global_exists("emotion_data")) {
        StartEmotionProtocol();
    }
	

    if (global.emotion_data.pending) {
        return;
    }

    global.emotion_data.pending = true;
    global.emotion_data.status = "requesting";
    global.emotion_data.request_count += 1;
    http_get("http://127.0.0.1:5000/emotion");
}

//parses response and sets data blah blah blah 
//Requires an asyncronous HTTP event in order to process. 
function ParseEmotionResponse(_response) {
    var json = json_parse(_response);

    if (is_struct(json)) {
        if (variable_struct_exists(json, "emotion")) {
            global.emotion_data.last_result = json[$ "emotion"];
        } else if (variable_struct_exists(json, "face_shape")) {
            global.emotion_data.last_result = json[$ "face_shape"];
        } else {
            global.emotion_data.last_result = "unknown";
        }

        global.emotion_data.status = "ok";
    } else {
        global.emotion_data.last_result = "error";
        global.emotion_data.status = "invalid-json";
    }

    global.emotion_data.pending = false;
    global.emotion_data.last_update = current_time;
}
//example call for async http call
/*
//calls data from the server
if (async_load[? "http_status"] == 200) {
    ParseEmotionResponse(async_load[? "result"]);
} else {
    global.emotion_data.status = "http-error";
    global.emotion_data.last_result = "error";
    global.emotion_data.pending = false;
}
*/
