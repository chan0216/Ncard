let nooncard;
async function checkStatus() {
  const response = await fetch("/api/status");
  const data = await response.json();
  if (data.error) {
    window.location.replace("/");
  } else if (data.verify_status == "basic") {
    document.querySelector(".ncard__unverified").style.display = "flex";
    let unverified_btn = document.querySelector(".unverified_btn");
    unverified_btn.style.visibility = "visible";
    unverified_btn.textContent = "填寫基本資料";
    unverified_btn.setAttribute("href", "/verify/school");
  } else if (data.verify_status == "profile") {
    document.querySelector(".ncard__unverified").style.display = "flex";
    let unverified_btn = document.querySelector(".unverified_btn");
    unverified_btn.style.visibility = "visible";
    unverified_btn.textContent = "填寫自我介紹";
    unverified_btn.setAttribute("href", "/my/profile");
  } else if (data.message) {
    document.querySelector(".ncard__card").style.display = "none";
    document.querySelector(".ncard__unverified").style.display = "flex";
    let unverified_btn = document.querySelector(".unverified_btn");
    unverified_btn.style.visibility = "visible";
    unverified_btn.setAttribute("onclick", "return false;");
    unverified_btn.textContent = "午夜即可抽卡";
  }
}

fetch("/api/ncard")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    if (data.data) {
      let ncardUnverified = document.querySelector(".ncard__unverified ");
      ncardUnverified.style.display = "none";
      let ncardCard = document.querySelector(".ncard__card");
      ncardCard.style.display = "block";
      let info = data.data;
      if (info.is_friend) {
        let invite = document.querySelector(".invite");
        invite.innerText = "已成為卡友";
        invite.disabled = true;
        invite.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
      } else if (info["invited"]) {
        let invite = document.querySelector(".invite");
        invite.innerText = "已送出好友邀請";
        invite.disabled = true;
        invite.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
        invite.style.width = "144px";
        invite.style.opacity = "0.2";
      }
      let image = document.createElement("img");
      image.src = info.image;
      image.classList.add("image");
      document.querySelector(".imagediv").append(image);
      document.querySelector(".school").textContent = info.realname;
      document.querySelector(".interest").textContent = info.interest;
      document.querySelector(".club").textContent = info.club;
      document.querySelector(".course").textContent = info.course;
      document.querySelector(".country").textContent = info.country;
      document.querySelector(".worry").textContent = info.worry;
      document.querySelector(".exchange").textContent = info.exchange;
      document.querySelector(".trying").textContent = info.trying;

      if (info.gender == "F") {
        document.querySelector(".gender").textContent = "女同學";
      } else {
        document.querySelector(".gender").textContent = "男同學";
      }
    }
  });
async function addFriend() {
  const messageData = {
    message: "雙方已成為好友，現在開始聊天吧",
  };
  const res = await fetch("/api/ncard", {
    method: "POST",
    body: JSON.stringify(messageData),
    headers: { "content-type": "application/json" },
  });
  const data = await res.json();
  if (data.friend) {
    let invite = document.querySelector(".invite");
    invite.innerText = "已成為卡友";
    invite.disabled = true;
    invite.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
  } else {
    let invite = document.querySelector(".invite");
    invite.innerText = "已送出好友邀請";
    invite.disabled = true;
    invite.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    invite.style.width = "144px";
    invite.style.opacity = "0.2";
  }
}
checkStatus();
