function login(event){
	event.preventDefault();
	var username = $('#inputUsername').val();
	$.ajax({
		url: '/loginDB',
		data: $('form').serialize(),
		type: 'POST',
		success: function(response){
			localStorage.setItem("username", username);
			var text = "Welcome, " + username + "!";
			overlayOn(text);
			setTimeout(function () {
				window.location = "http://localhost:5000/";
			}, 2000);
		},
		error: function(error){
			overlayOn("Wrong credentials, try again.");
		}
	});
}