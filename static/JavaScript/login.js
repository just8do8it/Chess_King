function login(){
	var username = $('#inputUsername').val();
	var pass = $('#inputPassword').val();
	$.ajax({
		url: '/loginDB',
		data: $('form').serialize(),
		type: 'POST',
		success: function(response){
			localStorage.setItem("username", username);
			window.location = "http://localhost:5000/";
			$('#login').attr("href", "http://localhost:5000/logout");
			document.getElementById('login').innerHTML = "Logout";
			alert("Welcome, " + username + "!");
			console.log(response);
			location.reload();
		},
		error: function(error){
			console.log(error);
		}
	});
}