//This function should be called if the data structure has not been initlized yet
//Defines data structure and gets initial emotion
function StartEmotionProtocol() {
    if (!variable_global_exists("emotion_data")) {
        global.emotion_data = {
            status: "idle", //http status
            last_result: "unknown", //emotion shown
            last_update: 0, //when updated
            pending: false, //are we waiting for request
            request_count: 0, //how many requests were sent out 
        };
    }

    global.emotion_data.status = "ready";
    global.emotion_data.last_result = "waiting";
    RequestEmotion();
}
