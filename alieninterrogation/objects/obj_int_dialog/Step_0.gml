// Advance dialogue when Space is pressed
if (keyboard_check_pressed(vk_space)) {

    cur_message++;

    // Check if conversation has ended
    if (cur_message >= array_length(messages)) {
        instance_destroy();
        exit;
    }
}