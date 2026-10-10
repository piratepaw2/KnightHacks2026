function create_dialog(messages){
	if (instance_exists(obj_dialog)) return;
	
	var inst = instance_create_depth(0,0,0,obj_dialog);
	
	inst.messages = messages;
	inst.cur_message = 0;
}

welcome_dialog = [
{
	name:"Interrogator",
	msg:"Sit down."
},
{
	name: "Interrogator",
	msg: "We have a lot to talk about."
}
]