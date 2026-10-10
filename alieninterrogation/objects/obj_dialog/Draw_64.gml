var dx = 0;
var dy = gui_h * 0.7;
var boxw = gui_w;
var boxh = gui_h - dy;

draw_sprite_stretched(spr_box, 0, dx, dy, boxw, boxh);


dx += 16;
dy +=16;

draw_set_font(Font1);

var name = messages[cur_message].name;
draw_text(dx, dy, name);

dy += 40;

draw_text_ext(dx, dy, draw_msg, -1, boxw - dx * 2);