// Dialogue array
messages = [
    {
		type: "dialogue",
        name: "",
        msg: "You smiled.",
		portrait: empty_sprite
    },
    {
		type: "dialogue",
        name: "Interrogator",
        msg: "I see..",
        portrait: int_neutral
    },

    {
		type: "dialogue",
        name: "Interrogator",        
        msg: "You smiled. The natural reaction.",
        portrait: int_happy
    },
	
	    {
		type: "dialogue",
        name: "Interrogator",
        msg: "Here's the next image.",
        portrait: int_neutral
    },

];

// Current dialogue line
cur_message = 0;