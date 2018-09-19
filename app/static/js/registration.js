function validateForm() {
    var name = document.forms["myForm"]["Username"].value;
    if (name.length < 3) {
        alert("username must be more than 3 characters");
        return false;
    }else if (!(/^[A-Za-z\s]+$/.test(name))){
        alert("Your username should only contain letters");
        return false;
    } else {
        return true;
    }
} 

let username = document.getElementById('Username').value;
let email = document.getElementById('Email').value;
let password = document.getElementById('Password').value;
let confirmPassword = document.getElementById('ConfirmPassword').value;

fetch('https://stackoverflowlitev3.herokuapp.com/api/v2/auth/registration', {
    method: 'POST',
    mode: 'cors', 
	redirect: 'follow',
	headers: new Headers({
		'Content-Type': 'application/json'
	}),
    body:JSON.stringify({
        username:username, 
        email:email, 
        password:password, 
        confirmpass:confirmPassword})
}).then(function(response) {
    return response.json();
}).then(function(body) {
    console.log(body);
})