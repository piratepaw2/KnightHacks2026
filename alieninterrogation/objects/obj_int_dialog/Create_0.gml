// Dialogue array
messages = [
    {
        name: "Interrogator",
        msg: "Let's begin.",
        portrait: int_neutral
    },

    {
        name: "Interrogator",
        msg: "I have recieved claims that you're..",
        portrait: int_neutral
    },
	
	    {
        name: "Interrogator",
        msg: "An alien.",
        portrait: int_angry
    },
	
	
    {
        name: "Alien",
        msg: "...",
        portrait: al_surprise
    },

    {
        name: "Alien",
        msg: "That's ridiculous.",
        portrait: al_neutral
    },

    {
        name: "Interrogator",
        msg: "Today you will undergo a series of tests..",
        portrait: int_neutral
    },
	
	    {
        name: "Interrogator",
        msg: "that will tell me all I need to know.",
        portrait: int_neutral
    },

    {
        name: "Alien",
        msg: "...",
        portrait: al_neutral
    }
];

// Current dialogue line
cur_message = 0;