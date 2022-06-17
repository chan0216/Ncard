const userformSubmit = document.querySelector(".userform__submit");
const userformAlert = document.querySelector(".userform__alert");
fetch("/api/verify")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    if (data.error) {
      userformSubmit.disabled = true;
      userformAlert.textContent = "請先登入";
      userformSubmit.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    }
    if (data.data) {
      //已經填過的狀況
      document.querySelector(".userform__submit").disabled = true;
      userformAlert.textContent = "你已經填過基本資料了喔！";
    }
  });
//提交基本資料
async function submitProfile() {
  let realname = document.querySelector("#realname").value;
  let gender = document.querySelector("#gender").value;
  let school = document.querySelector("#school").value;
  if (realname === "" || school === "") {
    userformAlert.textContent = "資料請輸入完整";
    return;
  }
  userformAlert.innerText = "";
  const profile = {
    realname: realname,
    gender: gender,
    school: school,
  };
  const config = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(profile),
  };
  const response = await fetch("/api/verify", config);
  const data = await response.json();
  if (data.ok) {
    document.querySelector(".userform__popup ").style.display = "block";
  } else {
    userformAlert.textContent = "填寫失敗，請重新嘗試";
  }
}
