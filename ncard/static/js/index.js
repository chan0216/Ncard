let newTitle = document.querySelector("#newTitle");
let hotTitle = document.querySelector("#hotTitle");
let LoadIcon = document.querySelector(".bi-arrow-clockwise");
let indexArticles = document.querySelector(".index__articles");

//顯示頁面
function renderPage(res) {
  // index__articles.innerHTML = "";
  for (const obj of res) {
    //發文人學校
    let userschool = document.createElement("p");
    userschool.classList.add("userschool");
    userschool.textContent = obj["school"];
    let contentDiv = document.createElement("div");
    contentDiv.classList.add("content_div");
    let icon = document.createElement("i");
    icon.classList.add("bi-person-circle");
    let icondiv = document.createElement("div");
    icondiv.classList.add("icondiv");
    icondiv.append(icon, userschool);
    let articleDiv = document.createElement("div");

    //標題
    let title = document.createElement("p");
    title.classList.add("articles__title");
    title.textContent = obj["title"];
    //文章內容
    let content = document.createElement("p");
    let textDiv = document.createElement("div");
    textDiv.classList.add("text_div");
    const text = obj["content"]
      .replace(/<div>/g, "\n")
      .replace(/<\/div>/g, "")
      .replace(/<br>/g, "\n")
      .replace(/<img[^>]*>/g, "")
      .replace(/<div[^>]*>/g, "")
      .replace(/\&nbsp;/g, "")
      .replace(/<p>/g, "")
      .replace(/<\/p>/g, ",")
      .replace(/<\/?span.*?>/g, "");

    content.innerText = text;
    textDiv.append(text);
    //呈現讚數及留言數
    let likeIcon = document.createElement("i");
    likeIcon.classList.add("bi-suit-heart");
    let commentIcon = document.createElement("i");
    commentIcon.classList.add("bi-chat-dots");

    let likeContainer = document.createElement("div");
    likeContainer.classList.add("like__container");
    let likeNums = document.createElement("p");
    likeNums.textContent = obj["like_count"];
    let commentNums = document.createElement("p");
    commentNums.textContent = obj["comment_count"];
    likeContainer.append(likeIcon, likeNums, commentIcon, commentNums);
    //呈現第一張圖片
    if (obj["first_img"]) {
      let image = document.createElement("img");
      image.src = obj["first_img"];
      image.classList.add("first_img");
      articleDiv.append(icondiv, title, textDiv, likeContainer);
      contentDiv.append(articleDiv, image);
    } else {
      articleDiv.append(icondiv, title, textDiv, likeContainer);
      contentDiv.append(articleDiv);
    }
    indexArticles.append(contentDiv);
    contentDiv.setAttribute("id", obj.id);
    contentDiv.setAttribute("onclick", "selectid(this.id)");
    if (obj["gender"] == "F") {
      icon.classList.add("women");
    } else {
      icon.classList.add("man");
    }
  }
}
//取得最新文章
let page = 0;
const getNewpost = async () => {
  const result = await fetch(`/api/newpost?page=${page}`);
  const data = await result.json();
  const res = data.data;
  hotTitle.classList.remove("active");
  newTitle.classList.add("active");
  page = data["nextPage"];
  if (page == null) {
    observer.unobserve(LoadIcon);
    LoadIcon.style.display = "None";
  }
  renderPage(res);
};
let options = { threshold: 0.5 };
let renderNextPages = (entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      getNewpost();
    }
  });
};
let observer = new IntersectionObserver(renderNextPages, options);
observer.observe(LoadIcon);

//顯示文章
const getHotpost = async () => {
  const result = await fetch(`/api/articles`);
  const data = await result.json();
  const res = data.data;
  newTitle.classList.remove("active");
  hotTitle.classList.add("active");
  observer.unobserve(LoadIcon);
  indexArticles.innerHTML = "";
  LoadIcon.style.display = "None";
  renderPage(res);
};
function selectid(checkid) {
  window.location.href = `/post/${checkid}`;
}
fetch("/api/user")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    let res = data;
    if (res.ok) {
      document.querySelector(".member__tag").style.display = "block";
    } else {
      document.querySelector(".visitor__tag").style.display = "block";
    }
  });
