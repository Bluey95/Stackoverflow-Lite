function submitForm(){
    let username = "cheruto"
    let email = "cheruto@gmail.com"
    let password = "Cheruto123"
    let confirmpass = "Cheruto123"
    
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