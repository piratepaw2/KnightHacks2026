//methodology to extract emotion data

var result = global.emotion_data.last_result;

if(result == "frown"){
	counts[sadIndex, 0]++;
}else if( result == "smile"){
	counts[happyIndex, 0]++;
}else if(result == "surprise"){
	counts[surprisedIndex, 0]++;
}else if(result == "neutral"){
	counts[neutralIndex, 0]++;
}


//everything below is just graphics things.
/*
var left = x - box_w * 0.5;
var top = y - box_h * 0.5;
var right = left + box_w;
var bottom = top + box_h;

draw_set_font(Font1);
draw_set_halign(fa_left);
draw_set_valign(fa_top);

draw_set_color(c_black);
draw_set_alpha(0.8);
draw_roundrect(left, top, right, bottom, false);

draw_set_color(c_white);
draw_set_alpha(1);
draw_roundrect(left, top, right, bottom, true);

draw_text(left + 16, top + 16, "Sad: " + string(counts[sadIndex, 0]));
draw_text(left + 16, top + 42, "Happy: " + string(counts[happyIndex, 0]));
draw_text(left + 16, top + 68, "Surprised: " + string(counts[surprisedIndex, 0]));
draw_text(left + 16, top + 92, "Neutral: " + string(counts[neutralIndex, 0]));
draw_text(left + 16, top + 116, "MCE: " + global.mostCommonEmotion);
draw_text(left + 16, top + 140,string(counts));
*/