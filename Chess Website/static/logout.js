function logout(){
	$.ajax({
		url: '/logoutDB',
		data: $('form').serialize(),
		type: 'GET',
		success: function(response){
			localStorage.clear();
			$('#login').attr("href", "http://localhost:5000/login");
			document.getElementById('login').innerHTML = "Login";
			window.location = "http://localhost:5000/home";
			alert("Now you can login with another profile.");
			console.log(response);
		},
		error: function(error){
			console.log(error);
		}
	});
}