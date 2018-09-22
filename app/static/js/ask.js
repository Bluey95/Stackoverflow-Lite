var request = new XMLHttpRequest();
console.log("starting here");
request.open('POST', 'https://stackoverflowlitev3.herokuapp.com/api/v2/questions', true);
request.withCredentials = true;
console.log(".............");
console.log("then here");
token = window.sessionStorage.getItem("token");
console.log(token)
console.log("and then here.........");
request.setRequestHeader('Authorization', 'Basic [base64 encoded password here]' );
request.onload = function () {
}
request.send();