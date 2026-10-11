
//Requests an emotion at each step (Is this a tick?)
if (global.emotion_data.pending == false) {
    RequestEmotion();
}

// Select an option
if (keyboard_check_pressed(vk_space)) {
            room_goto(rm_start);
}