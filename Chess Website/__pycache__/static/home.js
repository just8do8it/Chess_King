window.onload = function() {
	$.ajax({
		url: '/islogged',
		type: 'GET',
		success: function(response){
			$('#login').attr("href", "http://localhost:5000/logout");
			document.getElementById('login').innerHTML = "Logout";
		},
		error: function(error){
			$('#login').attr("href", "http://localhost:5000/login");
			document.getElementById('login').innerHTML = "Login";
			console.log(error);
		}
	});
}