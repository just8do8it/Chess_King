var count = 0;
var sourceId = "";
var destinationId = "";
var prevColor = "";
var command = "";
var board = [];
var all_figures;
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
	fetch('/', {
	    method: 'POST',
	    body: JSON.stringify(command)
	}).then(function (response) {
	    return response.text();
	}).then(function (text) {
	    console.log('POST response: ');
	    console.log(text);
	});

	board = document.getElementById("board").innerHTML;
	all_figures = document.getElementById("all_figures").innerHTML;

	alert(all_figures);

	changeHTML();
}

function changeHTML() {
	for (var i = 0, id_counter = 0; i < 8; i++) {
		var currLine = board[i];
		var index = 0;
		for (var key in currLine) {
			var currFig = all_figures[i];
			var black = 0;

			for (var j = 0; j < 64; ++j) {
				if (key == currFig[0] && index == currFig[1]) {
					if (currFig[2] == 1) {
						if (currFig[3] == "black") {
							black = 1;
						}
					} else {
						document.getElementById(htmlIds[id_counter]).innerHTML = "&nbsp;";
						return;
					}
				}
			}

			if (currLine[currLine[key]] == "R1" || currLine[currLine[key]] == "R2") {
				if (black)
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9820;";
				else
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9814;";
			} 

			else if (currLine[currLine[key]] == "H1" || currLine[currLine[key]] == "H2") {
				if (black)
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9822;";
				else
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9816;";
			} 

			else if (currLine[currLine[key]] == "B1" || currLine[currLine[key]] == "B2") {
				if (black)
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9821;";
				else
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9815;";
			} 

			else if (currLine[key] == "Q1") {
				if (black)
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9819;";
				else
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9813;";
			} 

			else if (currLine[key] == "K1") {
				if (black)
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9818;";
				else
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9812;";
			} 

			else if (currLine[key] == "P1" || currLine[key] == "P2" || currLine[key] == "P3" || currLine[key] == "P4" || currLine[key] == "P5" || currLine[key] == "P6") {
				if (black)
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9823;";
				else
					document.getElementById(htmlIds[id_counter]).innerHTML = "&#9817;";
			}

			index++;
			id_counter++;
		}
	}
}