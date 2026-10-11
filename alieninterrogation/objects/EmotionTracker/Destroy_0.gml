if(global.mostCommonEmotion == global.Emotion_Solution_Array[global.CURRENT_DIALOGUE]){
	global.CURRENT_DIALOGUE++;
	instance_create_layer(x, y, "Dialogue", global.Dialogue_Object_Array[global.CURRENT_DIALOGUE]);
}else{
	GAME_OVER();	
}