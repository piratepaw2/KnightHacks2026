
	//this instance sets the most common emotion after 
	//n seconds (rn its 10) and then destroys itself.
	//The draw part is how the system counts and stuff.
	//initializes most common emotion to N/A
	
	//graphics data 
	/*
	dragging = false;
	drag_offset_x = 0;
	drag_offset_y = 0;

	box_w = 600;
	box_h = 200;

	x = room_width * 0.5;
	y = room_height * 0.8;	
	*/
	
	
	global.mostCommonEmotion = "N/A";
	
	
	counts = [
	[0, "Sad"], 
	[0, "Happy"],
	[0, "Surprised"], 
	[0, "Neutral"]
	];
	
	time_to_emote_in_seconds = 10;
	
	sadIndex = 0;
	happyIndex = 1;
	surprisedIndex = 2;
	neutralIndex = 3;
	
	gatherData = true;
	
	if (!variable_global_exists("emotion_data")) {
		StartEmotionProtocol();
	}

	
	// Trigger an inline function after a 2-second delay
	time_source = time_source_create(time_source_global, time_to_emote_in_seconds, time_source_units_seconds, function() {
	    //This is where the most common will be calculated
		gatherData = false;
		
		//bubble sort
		counts = MCE_BubbleSort(counts);
		
		global.mostCommonEmotion = counts[0, 1];
		
		instance_destroy();
		
	});
	
	

	time_source_start(time_source); // Time sources must be manually started

