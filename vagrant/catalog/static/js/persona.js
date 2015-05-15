

var signinLink = document.getElementById('signin');
if (signinLink) {
  signinLink.onclick = function() { navigator.id.request(); };
}

var signoutLink = document.getElementById('signout');
if (signoutLink) {
  signoutLink.onclick = function() {
    navigator.id.logout();
    sessionStorage.clear();
    toggleLoggedInState(null);
    location.reload();
  };
}
var currentUser = '';

var toggleLoggedInState = function(session) {
  // Toggle from logged in state to logged out
  if ((session == null || session.email == null) && sessionStorage['email'] == null) {
    document.querySelector('#message').innerText = "";
    document.querySelector('#signin').style.display = "block";
    document.querySelector('#signout').style.display = "none";
  } else {
    // Toggle to logged in
    var text = "Logged in as "+ sessionStorage['email'];
    document.querySelector('#message').innerText = text;
    document.querySelector('#signin').style.display = "none";
    document.querySelector('#signout').style.display = "block";
  }
}

navigator.id.watch({
  loggedInUser: currentUser,
  onlogin: function(assertion) {
    // A user has logged in! Here you need to:
    // 1. Send the assertion to your backend for verification and to create a session.
    // 2. Update your UI.
    $.ajax({ /* <-- This example uses jQuery, but you can use whatever you'd like */
      type: 'POST',
      url: '/login', // This is a URL on your website.
      data: {assertion: assertion},
      dataType: 'json',
      success: function(res, status, xhr) {
        sessionStorage['email'] = res.email;
        location.reload();
      },
      error: function(xhr, status, err) {
        sessionStorage.clear();
        navigator.id.logout();
        alert("Login failure: " + err);
      }
    });
  },
  onlogout: function() {
    // A user has logged out! Here you need to:
    // Tear down the user's session by redirecting the user or making a call to your backend.
    // Also, make sure loggedInUser will get set to null on the next page load.
    // (That's a literal JavaScript null. Not false, 0, or undefined. null.)
    $.ajax({
      type: 'POST',
      url: '/logout', // This is a URL on your website.
      success: function(res, status, xhr) {
      },
      error: function(xhr, status, err) { alert("Logout failure: " + err); }
    });
  }
});
$(document).ready(toggleLoggedInState(null));
