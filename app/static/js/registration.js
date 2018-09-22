document.addEventListener("DOMContentLoaded", function() {
    var button = document.getElementById("register");
    button.onclick = function(){
        var Username = document.getElementById("Username").value;
        var Email = document.getElementById("Email").value;
        var Password = document.getElementById("Password").value;
        var Confirmpass = document.getElementById("ConfirmPassword").value;
    
        p = {
            username:Username,
            email:Email,
            password:Password,
            confirmpass:Confirmpass
        }

        console.log(JSON.stringify(p))

        fetch('https://stackoverflowlitev3.herokuapp.com/api/v2/auth/registration', {
        method: 'POST',
        mode: 'cors', 
        redirect: 'follow',
        headers: new Headers({
        'Content-Type': 'application/json'
        }),
        body:JSON.stringify(p)
        }).then(function(response) {
        if (response.status == 201){
            response.json().then(data => example(data));
            alert("You have been successfuly Registered. Please Login To Continue");
            window.location.replace("signin.html")
        }else if (response.status == 400 || response.status == 422){
            response.json().then(
                data => 
                { var arr = [];

                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        arr.push( [ key, data[key] ] );
                    }
                }alert(data[key]); window.location.reload(true);});
        }
        else{
        //failed
        response.json().then(data => console.log("Failed: ", data));
        }
        }).catch(err => console.log(err));
        function example(data){
            //execute some statements
            console.log(JSON.stringify(data));
        }
        return false;
    }
}) 

