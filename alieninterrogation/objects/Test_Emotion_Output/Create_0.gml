//debug box thing

menu_options = [
   "RETURN TO MAIN MENU"
];

dragging = false;
drag_offset_x = 0;
drag_offset_y = 0;

box_w = 600;
box_h = 200;


//starts the emotion process

global.emotion_data = {
    status: "idle",
    last_result: "unknown",
    last_update: 0,
    pending: false,
    request_count: 0,
    current_request: undefined
};


StartEmotionProtocol();



x = room_width * 0.5;
y = room_height * 0.2;	