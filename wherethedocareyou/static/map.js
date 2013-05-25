var circle;
var accum = 0;
var paper;

function draw() {
	console.log("Drawing!");
	paper = Raphael(10, 50, 1000, 5000);
	
	if (circle)
	{
		circle.remove();
	}
	getData();
}


function getData(){
	$.getJSON('/whereami', function(coords) {
	  $('.result');
	  console.log('Load was performed: '+JSON.stringify(coords));
	

	circle = paper.circle(coords['x'], coords['y'], 10);
	circle.attr("fill", "#f00", "stroke", "#000");

});	

	
}

window.setInterval(draw, 1000);

