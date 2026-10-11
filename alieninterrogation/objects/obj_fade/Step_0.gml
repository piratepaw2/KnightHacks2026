if (fading) {
    fade_alpha += fade_speed;

    if (fade_alpha >= 1) {
        fade_alpha = 1;

        // The screen is now completely black.
        // Put your transition action here.
    }
}