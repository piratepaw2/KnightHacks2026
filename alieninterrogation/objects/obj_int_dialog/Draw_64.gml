// Screen dimensions
var gw = display_get_gui_width();
var gh = display_get_gui_height();

// Get current dialogue
var current = messages[cur_message];

// Background
draw_set_color(c_black);
draw_rectangle(0, 0, gw, gh, false);

// Draw character portrait
var portrait = current.portrait;

// Scale portrait to fit the screen
var portrait_scale = min(
    (gw * 0.65) / sprite_get_width(portrait),
    (gh * 0.75) / sprite_get_height(portrait)
);

draw_sprite_ext(
    portrait,
    0,
    gw / 2,
    gh * 0.40,
    portrait_scale,
    portrait_scale,
    0,
    c_white,
    1
);

// Dialogue box
draw_set_alpha(0.9);
draw_set_color(c_black);

draw_rectangle(
    gw * 0.05,
    gh * 0.72,
    gw * 0.95,
    gh * 0.95,
    false
);

draw_set_alpha(1);

// Box border
draw_set_color(c_white);

draw_rectangle(
    gw * 0.05,
    gh * 0.72,
    gw * 0.95,
    gh * 0.95,
    true
);

// Speaker name
draw_set_color(c_yellow);

draw_text(
    gw * 0.08,
    gh * 0.75,
    current.name
);

// Dialogue text
draw_set_color(c_white);

draw_text_ext(
    gw * 0.08,
    gh * 0.81,
    current.msg,
    6,
    gw * 0.80
);

// Continue indicator
draw_text(
    gw * 0.87,
    gh * 0.91,
    "SPACE >"
);

// Reset drawing settings
draw_set_color(c_white);
draw_set_alpha(1);