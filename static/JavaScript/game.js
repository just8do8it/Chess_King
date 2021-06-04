var count = 0;
var sourceId = "";
var destinationId = "";
var prevColor = "";
var command = "";
var board = [];
var commands = "", alive_figures, taken_figures, my_turn, winner_is_me, can_move = 1, game_ended = 0, stop = 0;
localStorage.setItem("game_ended", 0);
localStorage.setItem("waiting", 0);
document.getElementById("yourWonFigures").innerHTML = "Your won figures:<br>";
document.getElementById("opponentsWonFigures").innerHTML = "Opponent's won figures:<br>";

// $(function(){
// 	$("#white_chessboard").load("white_chessboard.html");
// 	$("#black_chessboard").load("black_chessboard.html"); 
// });

waitForOpponent();
refreshMessages();

window.onbeforeunload = function() {
	quit_game();
	return "OK";
};

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
	localStorage.setItem("waiting", 0);
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
		if (stop != 1)
			sendCommand(1);
	}, 2000);
}

function refreshMessages() {
	getMessages();
	setInterval(function () {
		if (stop != 1)
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
	console.log("тук");
	if (update)
		command = "update" + commands;
	else
		stop = 1;
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

			board = data['board'];
			commands = data['commands'];
			alive_figures = data['alive_figures'];
			taken_figures = data['taken_figures'];
			my_turn = data['my_turn'];
			winner_is_me = data['winner_is_me'];
			updateTakenFigures();
			updateBoard();

			if (command[4] == 1 || command[4] == 8){
				if (board[command[4] - 1][command[3]][0] == "P") {
					var figure = prompt("Choose what figure to revive:", "For example 'Q' for queen");
					while (figure == null || figure.length > 1 || 
						(figure != "Q" && figure != "B" && figure != "H" && figure != "R" && figure != "P")) {
						figure = prompt("Choose what figure to revive:", "For example 'Q' for queen");
					}
					command = figure;
					sendCommand(0);
				}
			}

			if(my_turn == 1) {
				can_move = 1;
				document.getElementById("turn").innerHTML = "Your turn";
			} else if (my_turn == 0) {
				can_move = 0;
				document.getElementById("turn").style.left = "100%";
				document.getElementById("turn").innerHTML = "Opponent's turn";
			} else if (my_turn < 0) {
				game_ended = 1;
			}

			if (game_ended && !stop) {
				stop = 1;
				localStorage.setItem("game_ended", 1);
			}
			
			if (localStorage.getItem("game_ended") == "1") {
				if (localStorage.getItem("tournament") != "0") {
					window.onbeforeunload = null;
					if (winner_is_me == 0) {
						overlayOn("You lose! You'll be redirected to the Play page.");
						setTimeout(function () {
							window.location = "http://localhost:5000/play";
						}, 4000);
					} else {
						fetch('/tournament_matchmaking', {
							method: 'GET',
							headers: {
								'Content-Type': 'application/json',
								'Accept': 'application/json'
							}
						}).then(function (response) {
							response.json().then(function(data) {
								console.log(data);
								if (data instanceof Object) {
									console.log("quitted");
									localStorage.setItem("tournament", 0);
									on(data["winner"]);
									window.location = "http://localhost:5000/play";
								}
							});
						});

						if (winner_is_me == 1) {
							overlayOn("You win! Wait to get matched for the next game.");
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
										if (localStorage.getItem("game_ended") == "1") {
											console.log(data);
											localStorage.setItem("game_ended", 0);
											setTimeout(function () {
												window.location = "http://localhost:5000/game/" + data['game_id'];
											}, 2000);
										}
									}).catch(function() {
										console.log("error");
									});
								});
							}, 4000);
						} else {
							overlayOn("Draw! If you have higher win rate than your opponent, you will proceed in the tournament.");
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
										if (localStorage.getItem("game_ended") == "1") {
											console.log(data);
											localStorage.setItem("game_ended", 0);
											setTimeout(function () {
												if (data['game_id'] == "http://localhost:5000/play") {
													window.location = "http://localhost:5000/play"
												} else {
													window.location = "http://localhost:5000/game/" + data['game_id'];
												}
											}, 2000);
										}
									}).catch(function() {
										console.log("error");
									});
								});
							}, 4000);
						}
					}	
				} else {
					window.onbeforeunload = null;
					str = "";
					if (winner_is_me == 0) {
						str = "You lose!";
					} else if (winner_is_me == 1) {
						str = "You win!";
					} else {
						str = "Draw!";
					}
					var overlayText = String(str) + " You'll be redirected to the Play page."
					overlayOn(overlayText);
					for (var i = 0; i < 5; ++i) {
						fetch('/get_in_game', {
							method: 'GET',
							headers: {
								'Content-Type': 'application/json',
								'Accept': 'application/json'
							}
						}).then(function (response) {
							response.json().then(function(data) {}
							).catch(function() {
								console.log("error");
							});
						});
					}
					
					setTimeout(function () {
						window.location = "http://localhost:5000/play";
					}, 4000);
				}
			}
		});
	}).finally(function () {
		stop = 0;
	});
}
