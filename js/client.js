/********************************************
*											*
*		parse and render lots				*
*											*
********************************************/

var i = 0;
var coordinates;
var xCoord;
var yCoord;

function parseLotsJson(json){
	var dict = JSON.parse(json);
	for(var key in dict) {
		var value = dict[key];
		console.log(key, value);
		//possibly remove quotes at beg and end of coords
		coordinates = key.split(', ');
		xCoord = coordinates[0].substring(1, coordinates[0].length - 1);
		yCoord = coordinates[1].substring(0, coordinates[1].length - 2);
		renderLots(xCoord, yCoord, value);
	}
}

function renderLots(x, y, value){
	if (value == "House") { 
		var sprite = game.add.sprite(x*(window.innerWidth/9)-((window.innerWidth/9)/2), y*(window.innerHeight/9)-((window.innerHeight/9)/2), 'house');
	} else {
		var sprite = game.add.sprite(x*(window.innerWidth/9)-((window.innerWidth/9)/2), y*(window.innerHeight/9)-((window.innerHeight/9)/2), 'empty_lot');
	}
}

//render json lots function
//render streets function



/********************************************
*											*
*		load house, empty ,and business		*
*		lots sprites						*
*											*
********************************************/

function preload() {
	
	game.load.baseURL = 'http://examples.phaser.io/assets/';
	game.load.crossOrigin = 'anonymous';
	game.load.image('empty_lot', 'sprites/phaser-dude.png');

	game.load.image('house', 'Sprites/house.png');


}
function create() {
}

function update() {
}

function render() {
}