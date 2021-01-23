window.onload = function() {
	$.ajax({
		url: '/islogged',
		type: 'GET',
		success: function(response){
			if (window.location == "http://localhost:5000/login" || window.location == "http://localhost:5000/signUp")
				window.location = "http://localhost:5000/logout";
		},
		error: function(error){
			if (window.location != "http://localhost:5000/signUp")
				window.location = "http://localhost:5000/login";
			console.log(error);
		}
	});
}