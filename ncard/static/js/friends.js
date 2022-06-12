async function fetchFriendData() {
  const response = await fetch("/api/friend");
  const data = await response.json();
  if (data.data) {
    console.log(data);
    let infoArr = data.data;
    for (let info of infoArr) {
      console.log(info);
      let friendList = document.querySelector(".friend__list");
      let friendimgDiv = document.createElement("div");
      let friendImg = document.createElement("img");
      let friendDiv = document.createElement("div");
      let friendDataDiv = document.createElement("div");
      let friendName = document.createElement("p");
      let friendSchool = document.createElement("p");
      friendName.textContent = info.realname;
      friendSchool.textContent = info.school;
      friendImg.src = info.image;
      friendImg.classList.add("friend_img");
      friendimgDiv.classList.add("friendimg_div");
      friendDataDiv.classList.add("frienddata_div");
      friendDiv.classList.add("friendDiv");
      friendimgDiv.append(friendImg);
      friendDataDiv.append(friendName, friendSchool);
      friendDiv.append(friendimgDiv, friendDataDiv);
      friendList.append(friendDiv);
    }
  } else {
    console.log("沒朋友");
    document.querySelector(".nofriend ").style.display = "flex";
  }
}
fetchFriendData();
