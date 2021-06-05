var username = localStorage.getItem("username");
localStorage.setItem("tournament", 0);
var game_id, white_player, black_player;

function end_waiting(){
	if (localStorage.getItem("tournament") == "1") {
		$.ajax({
			url: '/tournament_end_waiting',
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	} else {
		$.ajax({
			url: '/end_waiting',
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	}
};

function multiplayer() {
	window.onbeforeunload = function () {
		end_waiting();
		return "OK";
	}

	document.getElementById("multiplayer").style.display = 'none';
	document.getElementById("tournament").style.display = 'none';
	document.getElementById("heading").innerHTML = 'Waiting...';

	localStorage.setItem("waiting", 1);
	
	// -------------------------------------------------------------------------------

	// const response = await fetch('/get_online_players', {
	// 	method: 'GET',
	// 	headers: {
	// 		'Content-Type': 'application/json',
	// 		'Accept': 'application/json'
	// 	}
	// });

	// const data = await response.json().catch(function() {
	// 	setInterval(async function() {
	// 		const response2 = await fetch('/get_in_game', {
	// 			method: 'GET',
	// 			headers: {
	// 				'Content-Type': 'application/json',
	// 				'Accept': 'application/json'
	// 			}
	// 		});
			
	// 		const data2 = response2.json();
	// 		console.log(data2);
	// 		window.onbeforeunload = null;
	// 		end_waiting();
	// 		alert(data2['game_id']);
	// 		window.location = "http://localhost:5000/game/" + data2['game_id'];
	// 	}, 2000);
	// });
	
	
	
	// console.log(data);
	// window.onbeforeunload = null;
	// end_waiting();
	// game_id = data['game_id'];
	// window.location = "http://localhost:5000/game/" + game_id;

	// -------------------------------------------------------------------------------

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

function tournament() {
	window.onbeforeunload = function () {
		end_waiting();
		return "OK";
	}

	document.getElementById("multiplayer").style.display = 'none';
	document.getElementById("tournament").style.display = 'none';
	document.getElementById("heading").innerHTML = 'Waiting...';

	localStorage.setItem("waiting", 1);
	localStorage.setItem("tournament", 1);

	fetch('/tournament_getting_players', {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			'Accept': 'application/json'
		}
	}).then(function (response) {
			fetch('/tournament_matchmaking', {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'Accept': 'application/json'
				}
			}).then(function (response) {
				response.json().then(function(data) {
					console.log(data);
				}).catch(function() {
					console.log("error");
				});
			});

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
						window.location = "http://localhost:5000/game/" + data['game_id'];
					}).catch(function() {
						console.log("error");
					});
				});
			}, 2000);
		}).catch(function() {

		});
}