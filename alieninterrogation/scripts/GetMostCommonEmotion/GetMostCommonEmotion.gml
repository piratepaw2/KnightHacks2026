//return string of most common emotion
function GetMostCommonEmotion(){
	
	var counts = [
	[0, "Sad"], 
	[0, "Happy"],
	[0, "Surprised"], 
	[0, "Neutral"]
	];
	
	var sadIndex = 0;
	var happyIndex = 1;
	var surprisedIndex = 2;
	var neutralIndex = 3;
	
	var gatherData = true;
	
	var time_to_emote_in_seconds = 5;
	// Trigger an inline function after a 2-second delay
	time_source = time_source_create(time_source_global, time_to_emote_in_seconds, time_source_units_seconds, function() {
	    //This is where the most common will be calculated
		gatherData = false;
		
		//bubble sort
		counts = MCE_BubbleSort(counts);
		
		global.mostCommonEmotion = counts[0, 1];
		
	});

	time_source_start(time_source); // Time sources must be manually started
	
	

}

//descending order bubblesort for the Most common emotion array
function MCE_BubbleSort(array){
	
	for(i = 0; i < 3; i++){
		for( j = 0; j < 3 - i; j++){
			if(array[j,0] < array[j+1,0]){
				temp = array[j];
				array[j] = array[j+1];
				array[j+1] = temp;
			}
		}
	}
	
	return array;
}