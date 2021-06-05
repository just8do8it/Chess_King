function logout(event){
	event.preventDefault();
	$.ajax({
		url: '/logoutDB',
		data: $('form').serialize(),
		type: 'GET',
		success: function(response){
			localStorage.clear();
			$('#login').attr("href", "http://localhost:5000/login");
			document.getElementById('login').innerHTML = "Login";
			overlayOn("Now you can login with another profile.");
			setTimeout(function () {
				window.location = "http://localhost:5000/";
			}, 2000);
		}
	});
}