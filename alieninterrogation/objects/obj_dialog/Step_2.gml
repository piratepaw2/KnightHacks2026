if (cur_message < 0) exit;

var _str = messages[cur_message].msg;

if (cur_char < string_length(_str)){

	cur_char += char_speed * (1 + real(keyboard_check(input_key)));
	draw_msg = string_copy(_str, 0, cur_char);
}else if (keyboard_check_pressed(input_key)){
	cur_message++;
	if(cur_message >= array_length(messages)){
		instance_destroy();
	}else{
		cur_char = 0;
	}
}