audio_play_sound(interrogation_music, 0, true);
// Dialogue array
messages = [
    {
		type: "dialogue",
        name: "Interrogator",
        msg: "Hee hee!",
        portrait: int_happy
    },

    {
		type: "dialogue",
        name: "Interrogator",
        msg: "Ahem.. sorry.",
        portrait: int_neutral
    }

];

// Current dialogue line
cur_message = 0;