audio_play_sound(interrogation_music, 0, true);
// Dialogue array
messages = [
    {
		type: "dialogue",
        name: "Interrogator",
        msg: "You remained neutral.",
        portrait: int_neutral
    },

    {
		type: "dialogue",
        name: "Interrogator",
        msg: "I see my stare had no effect on you.",
        portrait: int_neutral
    },
	
	    {
		type: "dialogue",
        name: "Interrogator",
        msg: "Here's the next image.",
        portrait: int_neutral
    }

];

// Current dialogue line
cur_message = 0;