function signUp(){
	var username = $('#inputUsername').val();
	var pass = $('#inputPassword').val();
	$.ajax({
		url: '/signupDB',
		data: $('form').serialize(),
		type: 'POST',
		success: function(response){
			window.location = "http://localhost:5000/login";
			console.log(response);
		},
		error: function(error){
			console.log(error);
		}
	});
}