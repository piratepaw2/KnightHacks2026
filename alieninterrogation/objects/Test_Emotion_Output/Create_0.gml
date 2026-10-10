dragging = false;
drag_offset_x = 0;
drag_offset_y = 0;

box_w = 360;
box_h = 120;

if (!variable_global_exists("emotion_debug")) {
    StartEmotionDebug();
}

x = room_width * 0.5;
y = room_height * 0.2;