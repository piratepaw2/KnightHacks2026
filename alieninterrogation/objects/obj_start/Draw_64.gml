// Get screen dimensions
var gw = display_get_gui_width();
var gh = display_get_gui_height();
draw_set_font(start_font);

draw_sprite_stretched(
    spr_menu_bg,
    0,
    0,
    0,
    gw,
    gh
);

// Title
draw_set_color(c_white);
draw_set_halign(fa_center);

draw_text(gw / 2, gh * 0.25, "alien interrogation");

// Menu options
for (var i = 0; i < array_length(menu_options); i++) {

    if (selected == i) {
        draw_set_color(c_olive);
    } else {
        draw_set_color(c_white);
    }

    draw_text(
        gw / 2,
        gh * 0.55 + (i * 50),
        menu_options[i]
    );
}

// Reset drawing settings
draw_set_color(c_white);
draw_set_halign(fa_left);