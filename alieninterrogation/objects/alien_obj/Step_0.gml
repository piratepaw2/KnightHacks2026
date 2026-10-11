if (instance_exists(obj_dialog)) exit;

/*if (keyboard_check_pressed(vk_space)){
	create_dialog([
	{
		name: "Test dialog",
		msg: "It works"
	}
	])

} */

var hor = keyboard_check(ord("D")) - keyboard_check(ord("A"));
var ver = keyboard_check(ord("S")) - keyboard_check(ord("W"));

move_and_collide(hor * move_speed, ver * move_speed, tilemap);

/* here just put the walking sprites
if(hor != 0 || ver != 0){

	if (ver > 0) sprite_index = 
} */


