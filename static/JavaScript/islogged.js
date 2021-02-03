window.onload = function() {
	$.ajax({
		url: '/islogged',
		type: 'GET',
		success: function(response){
			document.getElementById('profile').style.display = "inline";
			
			if (String(window.location).substring(0, 27) == "http://localhost:5000/login" || window.location == "http://localhost:5000/signUp")
				window.location = "http://localhost:5000/";

			if (window.location == "http://localhost:5000/") {
				$('#login').attr("href", "http://localhost:5000/logout");
				document.getElementById('login').innerHTML = "Logout";
			}
			
			if (String(window.location).substring(0, 27) != "http://localhost:5000/game/" &&
				localStorage.getItem("waiting") != 1) {
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
			}
		},
		error: function(error){
			document.getElementById('profile').style.display = "none";

			if (window.location != "http://localhost:5000/signUp" && 
				window.location != "http://localhost:5000/login" &&
				window.location != "http://localhost:5000/")
				window.location = "http://localhost:5000/login";

			if (window.location != "http://localhost:5000/") {
				$('#login').attr("href", "http://localhost:5000/login");
				document.getElementById('login').innerHTML = "Login";
			}
			console.log(error);
		}
	});
}