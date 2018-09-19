let username = document.getElementById('Username').value;
let email = document.getElementById('Email').value;
let password = document.getElementById('Password').value;
let confirmPassword = document.getElementById('ConfirmPassword').value;

fetch('https://stackoverflowlitev3.herokuapp.com/api/v2/auth/registration', {
    method: 'POST',
    headers:{
        'Content-Type': 'application/json'
      },
    body:JSON.stringify({
        username:username, 
        email:email, 
        password:password, 
        confirmPassword:confirmPassword})
}).then(function(response) {
    return response.json();
})
     