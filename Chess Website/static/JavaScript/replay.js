var count = 0;
var sourceId = "";
var destinationId = "";
var prevColor = "";
var command = "";
var board = [];
var all_figures, w_won_figures, b_won_figures, my_turn, can_move = 1, game_ended = 0;

waitForOpponent();

function previous() {
    command = "previous";
}

function next() {
    command = "next";
}

function waitForOpponent() {
	setInterval(function() {
		sendCommand(1);
	}, 2000);
}

function sendCommand(update) {
	var game = new String(window.location);
    game = game.slice(27);
    
    var url = "/replay/";
    url = url.concat(game);

	console.log(command);
	fetch(url, {
	    method: 'POST',
		body: JSON.stringify(command),
		headers: {
			'Content-Type': 'application/json'
		}
	}).then(function (response) {
		response.json().then(function(data) {
			console.log(data);

			board = data["board"];
			all_figures = data["all_figures"];
			w_won_figures = data["w_won_figures"];
			b_won_figures = data["b_won_figures"];
			my_turn = data['my_turn'];
			changeHTML();

			if(my_turn == 1) {
				can_move = 1;
				document.getElementById("turn").innerHTML = "Your turn";
			} else if (my_turn == 0) {
				can_move = 0;
				document.getElementById("turn").style.left = "100%";
				document.getElementById("turn").innerHTML = "Opponent's turn";
			} else if (my_turn == -1) {
				document.getElementById("turn").style.left = "100%";
				document.getElementById("turn").innerHTML = "Black player wins!";
				game_ended = 1;
			} else if (my_turn == -2) {
				document.getElementById("turn").style.left = "100%";
				document.getElementById("turn").innerHTML = "White player wins!";
				game_ended = 1;
			} else if (my_turn == -3) {
				document.getElementById("turn").innerHTML = "Draw!";
				game_ended = 1;
			}
		});
	}).catch(error => {
		console.error('Error:', error);
	});
}

function changeHTML() {
	for (var i = 0; i < 8; i++) {
		var currLine = board[i];

		for (var key in currLine) {
			if (currLine[key] == "  ") {
				document.getElementById(key + String(i + 1)).innerHTML = "&nbsp;";
				continue;
			}

			var currFig;
			var black = 0;

			for (var j = 0; j < all_figures.length; ++j) {
				currFig = all_figures[j];

				if (String.fromCharCode(currFig[0]) == key && currFig[1] == (i + 1)) {
					if (currFig[2] == "black") {
						black = 1;
					}
				}
			}

			if (currLine[key] == "R1" || currLine[key] == "R2") {
				if (black)
					document.getElementById(key + String(i + 1)).innerHTML = "&#9820;";
				else
					document.getElementById(key + String(i + 1)).innerHTML = "&#9814;";
			} 

			else if (currLine[key] == "H1" || currLine[key] == "H2") {
				if (black)
					document.getElementById(key + String(i + 1)).innerHTML = "&#9822;";
				else
					document.getElementById(key + String(i + 1)).innerHTML = "&#9816;";
			} 

			else if (currLine[key] == "B1" || currLine[key] == "B2") {
				if (black)
					document.getElementById(key + String(i + 1)).innerHTML = "&#9821;";
				else
					document.getElementById(key + String(i + 1)).innerHTML = "&#9815;";
			} 

			else if (currLine[key] == "Q1") {
				if (black)
					document.getElementById(key + String(i + 1)).innerHTML = "&#9819;";
				else
					document.getElementById(key + String(i + 1)).innerHTML = "&#9813;";
			} 

			else if (currLine[key] == "K1") {
				if (black)
					document.getElementById(key + String(i + 1)).innerHTML = "&#9818;";
				else
					document.getElementById(key + String(i + 1)).innerHTML = "&#9812;";
			}

			else if (currLine[key][0] == "P") {
				if (black)
					document.getElementById(key + String(i + 1)).innerHTML = "&#9823;";
				else
					document.getElementById(key + String(i + 1)).innerHTML = "&#9817;";
			}
		}
	}
}