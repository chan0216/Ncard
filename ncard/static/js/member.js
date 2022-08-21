async function fetchValidation() {
  const response = await fetch("/api/validation");
  const data = await response.json();
  if (data.error) {
    window.location.replace("/");
  } else if (data.data) {
    let member__card = document.querySelector(".member__card");
    member__card.style.visibility = "visible";
    let name = document.querySelector("#name");
    name.textContent = data.data.name;
    let school = document.querySelector("#school");
    school.textContent = data.data.school;
  } else {
    let member__card = document.querySelector(".member__card");
    member__card.style.visibility = "visible";
    let title = document.querySelector("#name");
    title.textContent = "填寫個人資料";
    let school = document.querySelector("#school");
    school.innerHTML = "立即填寫個人資料啟用<br />Ncard 完整功能";
    let button = document.createElement("a");
    button.innerText = "填寫資料";
    button.classList.add("button");
    button.setAttribute("href", "/verify/school");
    let btn = document.querySelector(".btn");
    btn.append(button);
  }
}
fetchValidation();
