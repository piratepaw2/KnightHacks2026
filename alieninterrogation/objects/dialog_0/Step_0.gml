if (keyboard_check_pressed(vk_space)) {

    cur_message++;

    // End conversation if we've reached the end
    if (cur_message >= array_length(messages)) {
        instance_destroy();
        exit;
    }
}