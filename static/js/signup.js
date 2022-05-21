let loginForm = document.querySelector(".login");
async function signin(e) {
  e.preventDefault();
  const signinData = {
    email: document.querySelector('input[name="email"]').value,
    password: document.querySelector('input[name="password"]').value,
    signintype: "website",
  };
  console.log(signinData);
  const response = await fetch("/api/user", {
    method: "POST",
    body: JSON.stringify(signinData),
    headers: { "Content-Type": "application/json" },
  });
  const data = await response.json();
  if (data.data) {
    window.location.replace("/");
  } else if (data.ok) {
    window.location.replace("/unconfirmed");
  } else {
    //error handle
  }
}
loginForm.addEventListener("submit", signin);
fetch("/api/user")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    if (data.ok) {
      document.body.style.backgroundColor = "white";
      window.location.replace("/");
    } else {
      document.querySelector("body").style.visibility = "visible";
    }
  });
