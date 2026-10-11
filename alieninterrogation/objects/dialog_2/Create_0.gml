audio_play_sound(interrogation_music, 0, true);
// Dialogue array
messages = [

    {
		type: "dialogue",
        name: "",
        msg: "You were surprised.",
		portrait: empty_sprite
    },
	
    {
		type: "dialogue",
        name: "Interrogator",
        msg: "I was trying to shock you with that one.",
        portrait: int_neutral
    },

    {
		type: "dialogue",
        name: "Interrogator",
        msg: "I see that I succeeded.",
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