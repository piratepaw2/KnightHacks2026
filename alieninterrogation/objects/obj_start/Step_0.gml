// Move selection down
if (keyboard_check_pressed(ord("S"))) {
    selected++;

    if (selected >= array_length(menu_options)) {
        selected = 0;
    }
}

bg_frame += bg_speed;

if (bg_frame >= sprite_get_number(start_menu)) {
    bg_frame = 0;
}

// Move selection up
if (keyboard_check_pressed(ord("W"))) {
    selected--;

    if (selected < 0) {
        selected = array_length(menu_options) - 1;
    }
}

// Select an option
if (keyboard_check_pressed(vk_space)) {

    switch (selected) {

       case 0:

		if (!instance_exists(obj_fade)) {

        var fade = instance_create_depth(
            0, 0, -10000, obj_fade
        );

        fade.target_room = interrogation;
        fade.fade_state = 1;
		}

		break;

		case 1:
			room_goto(PerceivedEmotionTestRoom);
			break;
        case 2:
            game_end();
            break;
    }
}