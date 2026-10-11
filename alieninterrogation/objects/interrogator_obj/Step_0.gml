if (instance_exists(obj_dialog)) exit;

if (instance_exists(alien_obj) && distance_to_object(alien_obj) < 8 && bello == 0){

	can_talk = true;
	if (keyboard_check_pressed(input_key)){
		create_dialog(welcome_dialog);
		bello = 1;
	}
}else{
	can_talk = false;
}