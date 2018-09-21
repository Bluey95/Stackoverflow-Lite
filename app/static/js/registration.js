function submitForm(){
    let username = document.getElementById('Username').value
    let email = document.getElementById('Email').value
    let password = document.getElementById('Password').value
    let confirmpass = document.getElementById('ConfirmPassword').value
    
    var http = new XMLHttpRequest();
    var url = 'https://stackoverflowlitev3.herokuapp.com/api/v2/auth/registration';
    var params = JSON.stringify({
        "username" : username, 
        "email" : email, 
        "password" : password, 
        "confirmpass" : confirmpass
    });
    http.open('POST', url, true);
    
    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/json');
    
    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            alert(http.responseText);
        }
    }
    http.send(params);
    }