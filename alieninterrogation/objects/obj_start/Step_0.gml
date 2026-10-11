// Move selection down
if (keyboard_check_pressed(vk_down)) {
    selected++;

    if (selected >= array_length(menu_options)) {
        selected = 0;
    }
}

// Move selection up
if (keyboard_check_pressed(vk_up)) {
    selected--;

    if (selected < 0) {
        selected = array_length(menu_options) - 1;
    }
}

// Select an option
if (keyboard_check_pressed(vk_enter)) {

    switch (selected) {

        case 0:
            room_goto(interrogation);
            break;

        case 1:
            game_end();
            break;
    }
}