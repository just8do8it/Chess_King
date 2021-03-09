function signUp(event){
	event.preventDefault();
	$.ajax({
		url: '/signupDB',
		data: $('form').serialize(),
		type: 'POST',
		success: function(response){
			window.location = "http://localhost:5000/login";
		}
	});
}