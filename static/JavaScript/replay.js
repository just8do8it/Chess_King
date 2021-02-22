var count = 0;
var sourceId = "";
var destinationId = "";
var prevColor = "";
var command = "";
var board = [];
var all_figures, w_won_figures, b_won_figures, w_player, b_player, game_ended = 0, move_counter = 0;
sendCommand();

document.getElementById("yourWonFigures").innerHTML = "Your won figures:<br>";
document.getElementById("opponentsWonFigures").innerHTML = "Opponent's won figures:<br>";

function previous() {
    if (move_counter > 0) {
        move_counter -= 1;
    }
    sendCommand();
}

function next() {
    move_counter++;
    sendCommand();
}

function sendCommand() {
    var url = "/replay/";
	var game = new String(window.location);
    game = game.slice(29);
    url = url.concat(game);
    
    str_move = String(move_counter);
	console.log(move_counter);
	fetch(url, {
	    method: 'POST',
		body: JSON.stringify(str_move),
		headers: {
			'Content-Type': 'application/json'
		}
	}).then(function (response) {
		response.json().then(function(data) {
			console.log(data);

			board = data["board"];
			alive_figures = data["alive_figures"];
			taken_figures = data['taken_figures'];
            move_counter = data["move_counter"];
            w_player = data["w_player"];
            b_player = data["b_player"];

            document.getElementById("w_player").innerHTML = w_player;
            document.getElementById("b_player").innerHTML = b_player;
			updateTakenFigures();
			updateBoard();
		});
	}).catch(error => {
		console.error('Error:', error);
	});
}

function updateTakenFigures() {
	if (taken_figures.length == 0) {
		return
	}

	var myColor = "";
	var page = document.getElementById("htmlPage").innerHTML;
	if (page == "whites_replay.html") {
		myColor = "white";
	} else {
		myColor = "black";
	}

	document.getElementById("yourWonFigures").innerHTML = "Your won figures:<br>";
	document.getElementById("opponentsWonFigures").innerHTML = "Opponent's won figures:<br>";

	var currFig, black, w_first = 0, w_second = 0, b_first = 0, b_second = 0;
	
	for (var j = 0; j < taken_figures.length; ++j) {
		newline = 0;
		currFig = taken_figures[j];
		black = 0;
		if (currFig[3] == "black") {
			black = 1;
		}

		var special_id = "";
		if (black) {
			if (myColor == "white") {
				w_first++;
				special_id = "yourWonFigures";
			} else {
				w_second++;
				special_id = "opponentsWonFigures";
			}
		} else {
			if (myColor == "black") {
				b_first++;
				special_id = "yourWonFigures";
			} else {
				b_second++;
				special_id = "opponentsWonFigures";
			}
		}


		if ((w_first % 7 == 0 && w_first > 0) || 
			(w_second % 7 == 0 && w_second > 0) || 
			(b_first % 7 == 0 && b_first > 0) || 
			(b_second % 7 == 0 && b_second > 0)) {
				newline = 1;
		}

		addTakenFigure(black, currFig[0], special_id, newline);
	}
}


function addTakenFigure(black, figure, special_id, newline) {
	if (figure == "R1" || figure == "R2") {
		if (black) {
			document.getElementById(special_id).innerHTML += "&#9820; ";
		} else {
			document.getElementById(special_id).innerHTML += "&#9814; ";
		}
	} 

	else if (figure == "H1" || figure == "H2") {
		if (black) {
			document.getElementById(special_id).innerHTML += "&#9822; ";
		} else {
			document.getElementById(special_id).innerHTML += "&#9816; ";
		}
	} 

	else if (figure == "B1" || figure == "B2") {
		if (black) {
			document.getElementById(special_id).innerHTML += "&#9821; ";
		} else {
			document.getElementById(special_id).innerHTML += "&#9815; ";
		}
	} 

	else if (figure == "Q1") {
		if (black) {
			document.getElementById(special_id).innerHTML += "&#9819; ";
		} else {
			document.getElementById(special_id).innerHTML += "&#9813; ";
		}
	}

	else if (figure == "K1") {
		if (black) {
			document.getElementById(special_id).innerHTML += "&#9818; ";
		} else {
			document.getElementById(special_id).innerHTML += "&#9812; ";
		}
	}

	else if (figure[0] == "P") {
		if (black) {
			document.getElementById(special_id).innerHTML += "&#9823; ";
		} else {
			document.getElementById(special_id).innerHTML += "&#9817; ";
		}
	}

	if (newline) {
		document.getElementById(special_id).innerHTML += "<br>";
	}
}

function updateBoard() {
	for (var i = 0; i < 8; i++) {
		var currLine = board[i];

		for (var key in currLine) {
			if (currLine[key] == "  ") {
				document.getElementById(key + String(i + 1)).innerHTML = "&nbsp;";
				continue;
			}

			var currFig;
			var black = 0;

			for (var j = 0; j < alive_figures.length; ++j) {
				currFig = alive_figures[j];

				if (String.fromCharCode(currFig[0]) == key && currFig[1] == (i + 1)) {
					if (currFig[2] == "black") {
						black = 1;
					}

					determineFigure(black, currLine, key, i);
				}
			}
		}
	}
}

function determineFigure(black, currLine, key, i) {
	var figure = currLine[key];

	if (figure == "R1" || figure == "R2") {
		if (black)
			document.getElementById(key + String(i + 1)).innerHTML = "&#9820;";
		else
			document.getElementById(key + String(i + 1)).innerHTML = "&#9814;";
	} 

	else if (figure == "H1" || figure == "H2") {
		if (black)
			document.getElementById(key + String(i + 1)).innerHTML = "&#9822;";
		else
			document.getElementById(key + String(i + 1)).innerHTML = "&#9816;";
	} 

	else if (figure == "B1" || figure == "B2") {
		if (black)
			document.getElementById(key + String(i + 1)).innerHTML = "&#9821;";
		else
			document.getElementById(key + String(i + 1)).innerHTML = "&#9815;";
	} 

	else if (figure == "Q1") {
		if (black)
			document.getElementById(key + String(i + 1)).innerHTML = "&#9819;";
		else
			document.getElementById(key + String(i + 1)).innerHTML = "&#9813;";
	} 

	else if (figure == "K1") {
		if (black)
			document.getElementById(key + String(i + 1)).innerHTML = "&#9818;";
		else
			document.getElementById(key + String(i + 1)).innerHTML = "&#9812;";
	}

	else if (figure[0] == "P") {
		if (black)
			document.getElementById(key + String(i + 1)).innerHTML = "&#9823;";
		else
			document.getElementById(key + String(i + 1)).innerHTML = "&#9817;";
	}
}