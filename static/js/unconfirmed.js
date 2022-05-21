async function getEmail() {
  const response = await fetch("/api/unconfirmed");
  const data = await response.json();
  if (data.data) {
    document.querySelector("body").style.visibility = "visible";
    let emailtext = document.querySelector(".email");
    emailtext.textContent = data.data.Email;
  } else {
    window.location.replace("/");
  }
}
getEmail();
