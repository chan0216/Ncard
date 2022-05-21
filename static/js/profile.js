async function submitProfile() {
  // let realname = document.querySelector("#realname").value;
  // let gender = document.querySelector("#gender").value;
  // let school = document.querySelector("#school").value;
  // console.log(realname, gender, school);
  const profile = {
    realname: document.querySelector("#realname").value,
    gender: document.querySelector("#gender").value,
    school: document.querySelector("#school").value,
  };
  const config = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(profile),
  };
  const response = await fetch("/api/profile", config);
  const data = await response.json();
  console.log(data);
  // if (data.data) {
  //   document.querySelector("body").style.visibility = "visible";
  //   let emailtext = document.querySelector(".email");
  //   emailtext.textContent = data.data.Email;
  // } else {
  //   window.location.replace("/");
  // }
}
// submitData();
