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
  if (data.ok) {
    let p = document.createElement("p");
    p.textContent = "填寫成功";
    p.style.marginBottom = "0";
    document.querySelector(".userform__card").append(p);
  } else {
    let p = document.createElement("p");
    p.textContent = "填寫失敗，請重新填寫";
    p.style.marginBottom = "0";
    document.querySelector(".userform__card").append(p);
  }
}
