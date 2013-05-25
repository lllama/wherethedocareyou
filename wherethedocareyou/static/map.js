var circle;
var accum = 0;

function draw() {
	console.log("Drawing!");

	var paper = Raphael(10, 50, 320, 200);
	
	accum += 10;

	if (circle)
	{
		circle.remove();
	}

	// Creates circle at x, y with radius r (x,y,r)
	circle = paper.circle(100+accum, 40, 10);

	// Sets the fill attribute of the circle to red (#f00)
	circle.attr("fill", "#f00", "stroke", "#000");
}

window.setInterval(draw, 1000);