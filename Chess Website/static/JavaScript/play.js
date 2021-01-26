var username = localStorage.getItem("username");
var game_id, white_player, black_player;

// function start_waiting(){
// 	$.ajax({
// 		url: '/start_waiting',
// 		// data: $('form').serialize(),
//         type: 'POST',
// 		success: function(response){
			
// 			console.log(response);
// 		},
// 		error: function(error){
// 			console.log(error);
// 		}
// 	});
// };

function end_waiting(){
	$.ajax({
		url: '/end_waiting',
		// data: $('form').serialize(),
        type: 'POST',
		success: function(response){
			console.log(response);
		},
		error: function(error){
			console.log(error);
		}
	});
};

function play() {
	window.onbeforeunload = function () {
		end_waiting();
		return "OK";
	}

	document.getElementById("multiplayer").style.display = 'none';
	document.getElementById("tournament").style.display = 'none';
	document.getElementById("heading").innerHTML = 'Waiting...';

	fetch('/get_online_players', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}
	}).then(function (response) {
		response.json().then(function(data) {
			console.log(data);
			window.onbeforeunload = null;
			end_waiting();
			game_id = data['game_id'];
			window.location = "http://localhost:5000/game/" + game_id;
		}).catch(function() {
			setInterval(function() {
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
						end_waiting();
						window.location = "http://localhost:5000/game/" + data['game_id'];
					}).catch(function() {
						console.log("error");
					});
				});		
			}, 2000);
		});
	});
}

function multiplayer() {
	play();
}

function tournament() {
    window.location = "http://localhost:5000/tournament";
}
