function handleCredentialResponse(response) {
  fetch(`/api/user`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_token: response.credential,
      signintype: "Google",
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["ok"]) {
        window.location.replace("/");
      }
    });
}

window.fbAsyncInit = function () {
  FB.init({
    appId: "955010961871784",
    cookie: true,
    xfbml: true,
    version: "v13.0",
  });

  FB.AppEvents.logPageView();
};

(function (d, s, id) {
  var js,
    fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) {
    return;
  }
  js = d.createElement(s);
  js.id = id;
  js.src = "https://connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
})(document, "script", "facebook-jssdk");
function checkLoginState() {
  FB.getLoginStatus(function (response) {
    statusChangeCallback(response);
  });
}
function statusChangeCallback(response) {
  // Called with the results from FB.getLoginStatus().
  // console.log("statusChangeCallback");
  // console.log(response); // The current login status of the person.
  if (response.status === "connected") {
    // Logged into your webpage and Facebook.
    console.log("你已經登入囉");
    getFBUserData();
  } else {
    // Not logged into your webpage or we are unable to tell.
    loginFB();
  }
}
function loginFB() {
  FB.login(function (response) {
    getFBUserData();
  });
}
function getFBUserData() {
  FB.api("/me", { fields: "id,email" }, function (user) {
    if (user["error"]) {
      console.log("error");
    } else {
      console.log(user.id, user.email);
      const signinFbData = {
        email: user.email,
        userid: user.id,
        signintype: "FB",
      };
      fetch("/api/user", {
        method: "POST",
        body: JSON.stringify(signinFbData),
        headers: { "Content-Type": "application/json" },
      });
    }
  });
}
