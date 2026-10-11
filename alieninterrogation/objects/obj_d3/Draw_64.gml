// Screen dimensions
var gw = display_get_gui_width();
var gh = display_get_gui_height();



var current = messages[cur_message];

// Draw background
draw_set_color(c_black);
draw_rectangle(0, 0, gw, gh, false);


// IMAGE EVENT
if (current.type == "image") {

    var img = current.image;

    // Scale image to fit screen
    var scale = min(
        (gw * 0.8) / sprite_get_width(img),
        (gh * 0.8) / sprite_get_height(img)
    );

    // Center image
    draw_sprite_ext(
        img,
        0,
        gw / 2,
        gh / 2,
        scale,
        scale,
        0,
        c_white,
        1
    );

    // Continue prompt
    draw_set_color(c_white);
    draw_text(
        gw * 0.75,
        gh * 0.92,
        "press space"
    );

}


// DIALOGUE EVENT
else if (current.type == "dialogue") {

    var portrait = current.portrait;

    var portrait_scale = min(
        (gw * 0.65) / sprite_get_width(portrait),
        (gh * 0.75) / sprite_get_height(portrait)
    );

    // Draw character
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

    // Speaker name
    draw_set_color(c_yellow);
    draw_set_font(Font1);

    draw_text(
        gw * 0.08,
        gh * 0.75,
        current.name
    );

    // Dialogue text
    draw_set_color(c_white);
    draw_set_font(Font1);

    draw_text_ext(
        gw * 0.08,
        gh * 0.81,
        current.msg,
        6,
        gw * 0.80
    );

    draw_text(
        gw * 0.87,
        gh * 0.91,
        "SPACE >"
    );
}

// Reset drawing settings
draw_set_color(c_white);
draw_set_alpha(1);