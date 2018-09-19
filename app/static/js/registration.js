fetch('https://stackoverflowlitev3.herokuapp.com/api/v2/auth/registration', {
    method: 'POST',
    headers:{
        'Content-Type': 'application/json'
      },
	body: JSON.stringify({
		"username" : document.getElementById('Username').value,
        "email" : document.getElementById('Email').value,
        "password" : document.getElementById('Password').value,
        "confirmPass" : document.getElementById('confirmPassword').value
	})
});