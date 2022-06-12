let loginForm = document.querySelector(".login");
async function signin(e) {
  e.preventDefault();
  let email = document.querySelector('input[name="email"]').value;
  let password = document.querySelector('input[name="password"]').value;
  let pattern = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if (pattern.test(email) === false) {
    document.querySelector(".error_text").textContent = "電子郵件不符合格式";
    return false;
  }
  if (password == "") {
    document.querySelector(".error_text").textContent = "密碼不得為空";
    return false;
  }
  const signinData = {
    email: document.querySelector('input[name="email"]').value,
    password: document.querySelector('input[name="password"]').value,
    signintype: "website",
  };
  const response = await fetch("/api/user", {
    method: "POST",
    body: JSON.stringify(signinData),
    headers: { "Content-Type": "application/json" },
  });
  const data = await response.json();
  if (data.data) {
    window.location.replace("/");
  } else if (data.ok) {
    // window.location.replace("/unconfirmed");
    window.location.replace("/");
  } else {
    console.log(data.message);
    document.querySelector(".error_text").textContent = data.message;
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
