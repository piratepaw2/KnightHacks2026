// Screen dimensions
var gw = display_get_gui_width();
var gh = display_get_gui_height();


var img = image_to_print.image;

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
	
	