//debug box thing



dragging = false;
drag_offset_x = 0;
drag_offset_y = 0;

box_w = 600;
box_h = 200;


//starts the emotion process


if (!variable_global_exists("emotion_data")) {
    StartEmotionProtocol();
}


x = room_width * 0.5;
y = room_height * 0.2;	