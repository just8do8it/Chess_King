var count = 0;
var sourceId = "";
var destinationId = "";
var prevColor = "";
var command = "";
var board = [];
var all_figures, w_won_figures, b_won_figures, my_turn, can_move = 1, game_ended = 0, stop = 0;
localStorage.setItem("game_ended", 0);
localStorage.setItem("waiting", 0);
localStorage.setItem("final", 0);
waitForOpponent();
refreshMessages();

$(window).on('beforeunload', function() {
	return "OK";
});

function chatTrigger() {
	var state = document.getElementById("chat").style.display;
	if (state == "none") {
		document.getElementById("chat").style.display = "inline";
		document.getElementById("message").style.display = "inline";
		document.getElementById("chatButton").innerHTML = "Hide chat";
	} else {
		document.getElementById("chat").style.display = "none";
		document.getElementById("message").style.display = "none";
		document.getElementById("chatButton").innerHTML = "Show chat";
	}
}

function quit_game(){
	$.ajax({
		url: '/quit_game',
        type: 'POST',
		success: function(response){
			console.log(response);
		},
		error: function(error){
			console.log(error);
		}
	});
};

function clicked(clicked_id) {
	if (can_move == 0 || game_ended == 1) {
		return;
	}
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
		sendCommand(0);
	}
}

function waitForOpponent() {
	setInterval(function() {
		if (!stop)
			sendCommand(1);
	}, 2000);
}

function refreshMessages() {
	getMessages();
	setInterval(function () {
		if (!stop)
			getMessages();
	}, 5000);
}

function getMessages() {
	var game_id = new String(window.location.pathname);
	var url = game_id + "/messages";
	fetch(url, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}
	}).then(function (response) {
		response.json().then(function(data) {
			console.log(data);
			data = data['chat'];
			var chat = "";
			for (var i = data.length - 1; i >= 0; --i) {
				for (var j = 0; j < data[i].length; ++j) {
					if (data[i][j - 1] == ")") {
						chat += "<strong>";
					} else if (data[i][j - 1] == ":") {
						chat += "</strong>";
					}
					chat += data[i][j];
				}
				chat += "<br><br>";
			}
			document.getElementById("chat").innerHTML = chat;
		}).catch(function() {
			console.log("error");
		});
	});
}

function sendMessage(event) {
	if (stop) {
		return;
	}
	event.preventDefault();
	var message = $('#message').val();
	$('#message').val("");
	var game_id = new String(window.location.pathname);
	var url = game_id + "/messages";
	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		},
		body: JSON.stringify(message)
	}).then(function() {
		getMessages();
	});
}


function sendCommand(update) {
	if (update)
		command = "update";
	var game_id = new String(window.location.pathname);
	console.log(command);
	fetch(game_id, {
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

			if (game_ended) {
				stop = 1;
				localStorage.setItem("game_ended", 1);
			}

			// alert("Game ended: " + String(localStorage.getItem("game_ended")));
			// alert("Tournament: " + String(localStorage.getItem("tournament")));
			// alert("Final: " + String(localStorage.getItem("final")));

			if (localStorage.getItem("game_ended") == "1") {
				if (localStorage.getItem("tournament") == "1") {
					fetch('/tournament_matchmaking', {
						method: 'GET',
						headers: {
							'Content-Type': 'application/json',
							'Accept': 'application/json'
						}
					}).then(function (response) {
						response.json().then(function(data) {
							console.log(data);
							if (typeof(data) != typeof("string")) {
								localStorage.setItem("tournament", 0);
								alert(data["winner"]);
								window.location = "http://localhost:5000/play";
							}
						}).catch(function() {
							console.log("error");
						});
					});
	
					setInterval(function() {
						document.getElementById("waiting").style.display = "inline";
						fetch('/get_in_game', {
							method: 'GET',
							headers: {
								'Content-Type': 'application/json',
								'Accept': 'application/json'
							}
						}).then(function (response) {
							response.json().then(function(data) {
								console.log(data);
								window.onbeforeunload = null;
								localStorage.setItem("game_ended", 0);
								localStorage.setItem("final", 1);
								window.location = "http://localhost:5000/game/" + data['game_id'];
							}).catch(function() {
								console.log("error");
							});
						});
					}, 2000);
				} else {
					setTimeout(function () {
						alert("The game has ended. You'll be redirected to the Play page.");
						window.onbeforeunload = null;
						window.location = "http://localhost:5000/play";
					}, 2000);
				}
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