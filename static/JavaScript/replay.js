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
		move_counter *= -1;
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