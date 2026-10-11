if (!instance_exists(obj_fade)) {

    var fade = instance_create_depth(
        0, 0, -10000, obj_fade
    );

    fade.target_room = rm_int;
    fade.fade_state = 1;
}