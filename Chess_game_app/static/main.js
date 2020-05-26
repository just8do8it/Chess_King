var count = 0;
var sourceId = "";
var destinationId = "";
var prevColor = "";
var command = "";
var board = [];
var htmlIds = [
	"A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1", 
	"A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2", 
	"A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3", 
	"A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4",
	"A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5", 
	"A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6", 
	"A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7", 
	"A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8"
];

document.getElementById("board").style.display = "none";

function clicked(clicked_id) {
	if (count == 0) {
		prevColor = document.getElementById(clicked_id).style.backgroundColor;
		sourceId = clicked_id;
		document.getElementById(clicked_id).style.backgroundColor = "#5c5c5c";
		count++;
	} else {
		destinationId = clicked_id;
		document.getElementById(sourceId).style.backgroundColor = prevColor;
		count = 0;
		command = sourceId + "-" + destinationId;
		sendCommand();
	}
}

function sendCommand() {
	alert(command);

	fetch('/postmethod', {
	    method: 'POST',
	    body: JSON.stringify(command)
	}).then(function (response) { // At this point, Flask has printed our JSON
	    return response.text();
	}).then(function (text) {
	    console.log('POST response: ');
	    console.log(text);
	});

	board = document.getElementById("board").innerHTML;
	alert(board);

	changeHTML();
}


// R: &#9820;
// H: &#9822;
// B: &#9821;
// Q: &#9819;
// K: &#9818;
// P: &#9823;


function changeHTML() {
	for (var i = 0, id_counter = 0; i < 8; i++) {
		var currLine = board[i];
		for (var key in currLine) {
			if (key == "R1" || key == "R2") {
				document.getElementById(htmlIds[id_counter]).innerHTML = "&#9820;";
			} else if (key == "H1" || key == "H2") {
				document.getElementById(htmlIds[id_counter]).innerHTML = "&#9822;";
			} else if (key == "B1" || key == "B2") {
				document.getElementById(htmlIds[id_counter]).innerHTML = "&#9821;";
			} else if (key == "Q1") {
				document.getElementById(htmlIds[id_counter]).innerHTML = "&#9819;";
			} else if (key == "K1") {
				document.getElementById(htmlIds[id_counter]).innerHTML = "&#9818;";
			} else { //(key == "P1" || key == "P2" || key == "P3" || key == "P4" || key == "P5" || key == "P6") {
				document.getElementById(htmlIds[id_counter]).innerHTML = "&#9823;";
			}

			id_counter++;
		}
	}
}