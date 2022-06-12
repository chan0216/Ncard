let url = new URL(window.location.href);
let date = new Date();
let now =
  date.getFullYear() +
  "/" +
  ("0" + (date.getMonth() + 1)).slice(-2) +
  "/" +
  ("0" + date.getDate()).slice(-2) +
  " " +
  ("0" + date.getHours()).slice(-2) +
  ":" +
  ("0" + date.getMinutes()).slice(-2) +
  ":" +
  ("0" + date.getSeconds()).slice(-2);

//顯示留言
const post = async () => {
  const result = await fetch(`/api/${url.pathname}`);
  const data = await result.json();
  const post = data.data;

  if (post) {
    let schoolText = document.createElement("p");
    schoolText.textContent = post.school;
    let icon = document.createElement("i");
    icon.classList.add("bi-person-circle");
    document.querySelector(".originator").append(icon, schoolText);
    //時間
    document.querySelector(".post__time").textContent = post.time;
    //標題
    let titleDiv = document.createElement("div");
    titleDiv.textContent = post.title;
    titleDiv.classList.add("post_title");
    let br = document.createElement("br");
    //文章
    let articleDiv = document.createElement("div");
    articleDiv.innerHTML = post.content;

    let postCard = document.querySelector(".post__card");

    postCard.append(titleDiv, br, articleDiv);
    if (post["gender"] == "F") {
      icon.classList.add("women");
      document.querySelector(".women").style.display = "block";
    } else {
      icon.classList.add("man");
      document.querySelector(".man").style.display = "block";
    }
  }
};
post();

//上傳留言
const postComment = async () => {
  let contenteditable = document.querySelector("[contenteditable]");
  let commentText = contenteditable.innerHTML;
  if (commentText === "") {
    console.log("沒填寫內容");
    return false;
  }
  const comment = {
    postId: url.pathname.split("/")[2],
    comment: commentText.replace(/<\/?span.*?>/g, ""),
    createTime: now,
  };
  const config = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(comment),
  };
  const result = await fetch(`/api/comment`, config);
  const data = await result.json();
  const res = data;

  if (res.ok) {
    window.location.reload();
  } else {
    document.querySelector(".comment_warning").textContent = "請先登入";
    document.querySelector(".comment_btn").disabled = true;
  }
};
const getComment = async () => {
  const result = await fetch(`/api/comment/${url.pathname.split("/")[2]}`);
  const data = await result.json();
  const res = data.data;
  if (res) {
    let commentCard = document.createElement("div");
    commentCard.classList.add("comment_card");
    //留言版標題
    let titleDiv = document.createElement("div");
    titleDiv.textContent = "留言";
    titleDiv.classList.add("title_div");
    commentCard.append(titleDiv);
    let commContainer = document.querySelector(".comment__container");
    commContainer.append(commentCard);
    for (const obj of res) {
      //留言div
      let commentDiv = document.createElement("div");
      commentDiv.classList.add("comment_div");
      //學校
      let icon = document.createElement("i");
      icon.classList.add("bi-person-circle");
      if (obj["gender"] == "F") {
        icon.classList.add("women");
        icon.style.display = "block";
      } else {
        icon.classList.add("man");
        icon.style.display = "block";
      }
      let school = document.createElement("p");
      school.textContent = obj["school"];
      school.classList.add("school");
      let text = document.createElement("p");
      text.innerHTML = obj["comment"];
      let createtime = document.createElement("p");
      createtime.textContent = obj["create_time"];
      createtime.classList.add("createtime");
      let content = document.createElement("div");
      content.append(school, text, createtime);
      commentDiv.append(icon, content);
      commentCard.append(commentDiv);
    }
  }
};
getComment();
fetch("/api/verify")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    if (data.error) {
      document.querySelector(".comment_warning").textContent = "請先登入！";
      return;
    }
    if (data.data == null) {
      document.querySelector(".comment_warning").textContent =
        "請先填寫基本資料才能留言喔！";
      return;
    }
    if (data.data) {
      document.querySelector(".post__school").textContent = data.data.school;
      document.querySelector(".user__time").textContent = now;
      let icon = document.createElement("i");
      icon.classList.add("bi-person-circle");
      if (data.data.gender == "F") {
        icon.classList.add("women");
        icon.style.display = "block";
      } else {
        icon.classList.add("man");
        icon.style.display = "block";
      }
      document.querySelector(".user__gender").append(icon);
    }
  });
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
      let image = document.createElement("img");
      let imageDiv = document.createElement("div");
      image.src = data["imgurl"];
      imageDiv.append(image);
      imageDiv.classList.add("imageDiv");
      let comment__box = document.querySelector(".comment__box");
      comment__box.append(imageDiv);
    });
});
function showmessage() {
  fetch("/api/verify")
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data.data) {
        document.querySelector(".full__comment").style.display = "block";
      }
    });
}
function hidemessage() {
  document.querySelector(".full__comment").style.display = "none";
}
