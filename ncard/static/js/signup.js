const loginForm = document.querySelector("#loginForm");
const errorText = document.querySelector(".error__text");
loginForm.addEventListener("submit", signin);
async function signin(e) {
  e.preventDefault();
  const email = document.querySelector('input[name="email"]').value;
  const password = document.querySelector('input[name="password"]').value;
  const pattern = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if (pattern.test(email) === false) {
    errorText.textContent = "電子郵件不符合格式";
    return false;
  }
  if (password == "") {
    errorText.textContent = "密碼不得為空";
    return false;
  }
  const signinData = {
    email: email,
    password: password,
    signintype: "website",
  };
  const response = await fetch("/api/user", {
    method: "POST",
    body: JSON.stringify(signinData),

    headers: { "Content-Type": "application/json" },
  });
  const data = await response.json();
  if (data.ok) {
    window.location.replace("/");
  } else {
    errorText.textContent = data.message;
  }
}

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
