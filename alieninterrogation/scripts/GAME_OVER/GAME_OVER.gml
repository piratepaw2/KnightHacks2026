function GAME_OVER(){

	//Failure Dialogues
	switch(global.mostCommonEmotion){

	
		case("Happy"):
		//failure, smile
		global.message_GAME_OVER_ROOM = [{
			type: "dialogue",
			name: "Interrogator",
			msg: "You thought that was funny? I didn't.",
			portrait: int_angry
		}, 
		{
			type: "dialogue",
			name: "Interrogator",
			msg: "I guess you really are an alien.",
			portrait: int_angry_covered
		}];
	
		//THEN'
		room_goto(GAME_OVER_ROOM);
		break;
	
		case("Surprised"):
		//failure, surprised
		global.message_GAME_OVER_ROOM = [{
			type: "dialogue",
			name: "Interrogator",
			msg: "What is wrong with you!?!",
			portrait: int_angry	
		},
		{
			type: "dialogue",
			name: "Interrogator",
			msg: "Guards, take him away!",
			portrait: int_angry_covered
		}];
	
		//THEN'
		room_goto(GAME_OVER_ROOM);
		break;
	
		case("Neutral"):
		//failure, neutral
		global.message_GAME_OVER_ROOM = [{
			type: "dialogue",
			name: "Interrogator",
			msg: "Stone cold, even after that?",
			portrait: int_angry
		},
		{
			type: "dialogue",
			name: "Interrogator",
			msg: "I'll see you in the labs, alien.",
			portrait: int_angry_covered
		}
		];
	
		//THEN'
		room_goto(GAME_OVER_ROOM);
		break;
	
		case("Sad"):
		//failure, sad
		global.message_GAME_OVER_ROOM = [{
			type: "dialogue",
			name: "Interrogator",
			msg:  "What? How could you even be sad about that?",
			portrait: int_angry //surprise? angry?
		},
		{
			type: "dialogue",
			name: "Interrogator",
			msg:  "You're clearly an alien!",
			portrait: int_angry_covered //surprise? angry?
		}
		];
	
		//THEN'
		room_goto(GAME_OVER_ROOM);
		break;
	
	
	}

}