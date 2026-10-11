audio_play_sound(main_music, 0, true);
// Dialogue array
messages = [
    {
		type: "dialogue",
        name: "Interrogator",
        msg: "The test is complete.",
        portrait: int_neutral
    },

    {
		type: "dialogue",
        name: "Interrogator",
        msg: "I have only one thing to say.",
        portrait: int_neutral
    },
	
	    {
		type: "dialogue",
        name: "Interrogator",
        msg: "I knew you were a human!",
        portrait: int_happy
    },
	
	
    {
		type: "dialogue",
        name: "Alien",
        msg: "!!!",
        portrait: al_surprise
    },

    {
		type: "dialogue",
        name: "Alien",
        msg: "Of course I am!",
        portrait: al_smile_1
    },

    {
		type: "dialogue",
        name: "Interrogator",
        msg: "I'm sorry for the trouble.",
        portrait: int_neutral
    },
	
	{
		type: "dialogue",
        name: "Interrogator",
        msg: "Let's get dinner.. on me.",
        portrait: int_neutral
    },
	
    {
		type: "dialogue",
        name: "Alien",
        msg: "Thank you, fellow human!",
        portrait: al_smile_1
    },
	{
			type: "image",
			image: win_screen
		}
];

// Current dialogue line
cur_message = 0;