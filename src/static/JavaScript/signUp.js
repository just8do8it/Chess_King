function signUp(event){
	event.preventDefault();
	$.ajax({
		url: '/signupDB',
		data: $('form').serialize(),
		type: 'POST',
		success: function(response){
			overlayOn("Successful registration!");
			setTimeout(function () {
				window.location = "http://localhost:5000/login";
			}, 4000);
		},
		error: function(error){
			overlayOn("Wrong credentials, try again.");
		}
	});
}