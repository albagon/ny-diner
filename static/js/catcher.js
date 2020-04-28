document.addEventListener('DOMContentLoaded', (event) => {
  Auth.check_token_fragment();
});

getRestaurants = () => {
  jwt = localStorage.getItem("JWTS_LOCAL_KEY");
  //alert('Well done number Alba! You are in restaurants' + jwt);

  const XHR = new XMLHttpRequest();

  // Define what happens on successful data submission
  XHR.addEventListener("load", function(event) {
    //window.location.href = "/restaurants/" + id.toString();
    console.log(event.target.responseText)
    alert('Success: ' + event.target.responseText);
  } );

  // Define what happens in case of error
  XHR.addEventListener("error", function(event) {
    alert('Oops! Something went wrong.');
  } );

  // Set up our request
  XHR.open("GET", "/restaurants");

  // Add Authorization header
  XHR.setRequestHeader("Authorization", "bearer " + jwt);

  // Send the request without data
  XHR.send();
}
