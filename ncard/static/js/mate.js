const friend_id = location.pathname.split("/").pop();
fetch(`/api/friend/${friend_id}`)
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    let ncard = document.querySelector(".ncard__card");
    ncard.style.display = "block";
    if (data.data) {
      let info = data.data;
      let image = document.createElement("img");
      image.src = info.image;
      image.classList.add("image");
      document.querySelector(".imagediv").append(image);
      document.querySelector(".realname").textContent = info.friendName;
      document.querySelector(".school").textContent = info.school;
      document.querySelector(".interest").textContent = info.interest;
      document.querySelector(".club").textContent = info.club;
      document.querySelector(".course").textContent = info.course;
      document.querySelector(".country").textContent = info.country;
      document.querySelector(".worry").textContent = info.worry;
      document.querySelector(".exchange").textContent = info.exchange;
      document.querySelector(".trying").textContent = info.trying;
      document
        .querySelector(".invite")
        .setAttribute("onclick", `location.href='/chats/${info.ncardId}'`);
    }
  });
