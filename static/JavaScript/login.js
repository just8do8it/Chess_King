function login(event){
	event.preventDefault();
	var username = $('#inputUsername').val();
	$.ajax({
		url: '/loginDB',
		data: $('form').serialize(),
		type: 'POST',
		success: function(response){
			localStorage.setItem("username", username);
			window.location = "http://localhost:5000/";
			alert("Welcome, " + username + "!");
			console.log(response);
			location.reload();
		},
		error: function(error){
			alert("Wrong credentials, try again.");
		}
	});
}