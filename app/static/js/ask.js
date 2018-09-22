document.addEventListener("DOMContentLoaded", function() {
    var button = document.getElementById("submit");
    button.onclick = function(){
        var questionTitle = document.getElementById("questionTitle").value;
        var questionBody = document.getElementById("questionBody").value;
        var getTOken = window.sessionStorage.getItem('token');
        var token = "Bearer " + getTOken;
        alert(token)

        p = {
            title:questionTitle,
            body:questionBody
        }
        console.log(p)

        fetch('https://stackoverflowlitev3.herokuapp.com/api/v2/questions', {
        method: 'POST',
        mode: 'cors', 
        crossdomain: true,
        redirect: 'follow',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': token
        },
        body: p
        }).then(function(response) {
        if (response.status == 201){
            response.json().then(data => example(data));
            window.location.replace("index.html")
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

