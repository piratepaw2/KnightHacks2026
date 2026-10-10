//methodology to extract emotion data
var state = global.emotion_data.status;
var result = global.emotion_data.last_result;
var count = string(global.emotion_data.request_count);

//everything below is just graphics things.

var left = x - box_w * 0.5;
var top = y - box_h * 0.5;
var right = left + box_w;
var bottom = top + box_h;

draw_set_font(Font1);
draw_set_halign(fa_left);
draw_set_valign(fa_top);

draw_set_color(c_black);
draw_set_alpha(0.8);
draw_roundrect(left, top, right, bottom, false);

draw_set_color(c_white);
draw_set_alpha(1);
draw_roundrect(left, top, right, bottom, true);

draw_text(left + 16, top + 16, "Emotion HTTP Debug");
draw_text(left + 16, top + 42, "Status: " + state);
draw_text(left + 16, top + 68, "Result: " + result);
draw_text(left + 16, top + 94, "Requests: " + count);