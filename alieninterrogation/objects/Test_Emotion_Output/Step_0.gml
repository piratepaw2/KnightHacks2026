var left = x - box_w * 0.5;
var top = y - box_h * 0.5;
var right = left + box_w;
var bottom = top + box_h;

var hover = point_in_rectangle(mouse_x, mouse_y, left, top, right, bottom);

if (mouse_check_button_pressed(mb_left) && hover) {
    dragging = true;
    drag_offset_x = mouse_x - x;
    drag_offset_y = mouse_y - y;
}

if (dragging) {
    x = mouse_x - drag_offset_x;
    y = mouse_y - drag_offset_y;
}

if (mouse_check_button_released(mb_left)) {
    dragging = false;
}

if (global.emotion_debug.pending == false) {
    RequestEmotion();
}