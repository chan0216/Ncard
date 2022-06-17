let warning = document.querySelector(".profile__warning");
fetch("/api/ncard-verify")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    if (data.verify_status == "Ncard") {
      document.querySelector(".ncard__card").style.display = "block";
    } else if (data.verify_status == "profile") {
      document.querySelector(".ncard__card").style.display = "block";
    } else if (data.verify_status == "basic") {
      let noprofile = document.querySelector(".noprofile");
      noprofile.style.display = "block";
    }
  });
//獲取自我介紹
fetch("/api/cardprofile")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    if (data.data) {
      let info = data.data;
      let image = document.createElement("img");
      image.src = info.image;
      image.classList.add("image");
      image.setAttribute("id", "ncardimage");
      document.querySelector(".imagediv").append(image);
      document.querySelector(".realname").textContent = info.realname;
      document.querySelector(".school").textContent = info.school;
      document.querySelector(".interest").value = info.interest;
      document.querySelector(".club").value = info.club;
      document.querySelector(".course").value = info.course;
      document.querySelector(".country").value = info.country;
      document.querySelector(".worry").value = info.worry;
      document.querySelector(".exchange").value = info.exchange;
      document.querySelector(".trying").value = info.trying;
    } else {
      let welTitle = document.querySelector(".wel_title");
      welTitle.textContent = "只要回答三個問題，並新增照片就可以開啟抽卡功能";
    }
  });
//上傳頭貼
document.querySelector("#upload_img").addEventListener("change", (event) => {
  let file = event.target.files[0];
  let data = new FormData();
  data.append("file", file);
  fetch("/api/image", {
    method: "POST",
    body: data,
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      document.querySelector(".imagediv").innerHTML = "";
      let image = document.createElement("img");
      image.src = data["imgurl"];
      image.setAttribute("id", "ncardimage");
      image.classList.add("image");
      document.querySelector(".imagediv").appendChild(image);
    });
});
//填寫自我介紹
const postNcard = async () => {
  const ncardImage = document.querySelector("#ncardimage");
  if (ncardImage == null) {
    warning.textContent = "請新增照片";
    return;
  }
  let interest = document.querySelector(".interest").value;
  let club = document.querySelector(".club").value;
  let course = document.querySelector(".course").value;
  let country = document.querySelector(".country").value;
  let worry = document.querySelector(".worry").value;
  let exchange = document.querySelector(".exchange").value;
  let trying = document.querySelector(".trying").value;
  let NcardArr = [interest, club, course, country, worry, exchange, trying];
  if (NcardArr.filter((q) => !q).length > 4) {
    warning.textContent = "請至少回答三個問題";
    return;
  }
  const postNcard = {
    ncardImage: ncardImage.src,
    interest: interest,
    club: club,
    course: course,
    country: country,
    worry: worry,
    exchange: exchange,
    trying: trying,
  };
  const config = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(postNcard),
  };
  const result = await fetch(`/api/cardprofile`, config);
  const data = await result.json();
  const res = data;
  if (res.ok) {
    window.location.reload();
  }
};
