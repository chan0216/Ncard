let url = new URL(window.location.href);
let date = new Date();
let comment = document.querySelector(".comment");
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

//顯示文章
const post = async () => {
  const result = await fetch(`/api/${url.pathname}`);
  const data = await result.json();
  const post = data.data;
  if (data.error) {
    document.querySelector(".submit").disabled = true;
  }
  if (post) {
    let schoolText = document.createElement("p");
    schoolText.textContent = post.school;
    let icon = document.createElement("i");
    icon.classList.add("bi-person-circle");
    document.querySelector(".originator").append(icon, schoolText);
    //時間
    const postTime = document.createElement("p");
    postTime.textContent = post.time;
    postTime.classList.add("post__time");
    //標題
    let titleDiv = document.createElement("div");
    titleDiv.textContent = post.title;
    titleDiv.classList.add("post_title");
    //文章
    let articleDiv = document.createElement("div");
    articleDiv.innerHTML = post.content;
    let postCard = document.querySelector(".post__card");
    postCard.append(titleDiv, postTime, articleDiv);
    if (post["gender"] == "F") {
      icon.classList.add("women");
      document.querySelector(".women").style.display = "block";
    } else {
      icon.classList.add("man");
      document.querySelector(".man").style.display = "block";
    }
    //顯示讚數及留言數
    comment.textContent = post.comment_count;
    document.querySelector(".like").textContent = post.like_count;
    if (post.like_post) {
      let like = document.querySelector(".bi-heart-fill");
      like.classList.add("active");
    }
  }
};
post();
//文章按讚功能
async function likePost() {
  const res = await fetch(`/api${url.pathname}/like`, { method: "PATCH" });
  const data = await res.json();
  if (data.error) {
    window.location.href = "/login";
    return;
  }
  console.log(data);
  document.querySelector(".like").textContent = data.like_count;
  let like = document.querySelector(".bi-heart-fill");
  like.classList.toggle("active");
}

//新增留言
const postComment = async () => {
  let contenteditable = document.querySelector("[contenteditable]");
  let commentText = contenteditable.innerHTML;
  if (commentText === "") {
    return false;
  }
  let message = commentText.replace(/<\/?span.*?>/g, "");
  const comment = {
    postId: url.pathname.split("/")[2],
    comment: message,
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
    let commentCard = document.querySelector(".comment_card");
    commentCard.style.background = "rgb(245, 245, 245)";
    let commentDiv = document.createElement("div");
    commentDiv.classList.add("comment_div");
    let comContainer = document.querySelector(".comment__container");
    comContainer.append(commentCard);
    //學校
    let icon = document.createElement("i");
    icon.classList.add("bi-person-circle");
    if (document.querySelector(".women")) {
      icon.classList.add("women");
      icon.style.display = "block";
    } else {
      icon.classList.add("man");
      icon.style.display = "block";
    }
    let schoolName = document.querySelector(".post__school").textContent;
    let school = document.createElement("p");
    school.textContent = schoolName;
    school.classList.add("school");
    let text = document.createElement("p");
    text.innerHTML = message;
    let createtime = document.createElement("p");
    createtime.textContent = now;
    createtime.classList.add("createtime");
    let content = document.createElement("div");
    content.append(school, text, createtime);
    commentDiv.append(icon, content);
    commentCard.append(commentDiv);
    hideMessage();

    //下滑到留言
    let commentCon = document.querySelector(".comment_div");
    commentCon.scrollIntoView();
    //清除欄位value
    document.querySelector(".comment__box").textContent = "";
  } else {
    document.querySelector(".comment_warning").textContent = "請先登入";
    document.querySelector(".comment_btn").disabled = true;
  }
};

//取得留言
const getComment = async () => {
  const result = await fetch(`/api/comment/${url.pathname.split("/")[2]}`);
  const data = await result.json();
  const res = data.data;

  if (res) {
    let commentCard = document.querySelector(".comment_card");
    commentCard.style.background = "rgb(245, 245, 245)";
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
async function checkVal() {
  const result = await fetch("/api/validation");
  const data = await result.json();
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
}
checkVal();
//上傳圖片
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
async function showmessage() {
  const result = await fetch("/api/validation");
  const data = await result.json();
  if (data.data) {
    document.querySelector(".full__comment").style.display = "block";
  }
}
function hideMessage() {
  document.querySelector(".full__comment").style.display = "none";
}
function expandComment() {
  document.querySelector(".full__comment").style.height = "93%";
  const commentBox = document.querySelector(".comment__box");
  commentBox.style.height = "inherit";
  const expandArrow = document.querySelector(".bi-arrows-angle-expand");
  expandArrow.className = "bi-arrows-angle-contract";
  expandArrow.onclick = contractComment;
}
function contractComment() {
  document.querySelector(".full__comment").style.height = "";
  const commentBox = document.querySelector(".comment__box");
  commentBox.style.height = "190px";
  const contractArrow = document.querySelector(".bi-arrows-angle-contract");
  contractArrow.className = "bi-arrows-angle-expand";
  contractArrow.onclick = expandComment;
}
