fetch("/api/newpost")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    let res = data.data;

    for (const obj of res) {
      //發文人學校
      let userschool = document.createElement("p");
      userschool.classList.add("userschool");
      userschool.textContent = obj["school"];
      let index__card = document.querySelector(".index__card");
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
      //呈現第一張圖片
      if (obj["first_img"]) {
        let image = document.createElement("img");
        image.src = obj["first_img"];
        image.classList.add("first_img");
        articleDiv.append(icondiv, title, textDiv);
        contentDiv.append(articleDiv, image);
      } else {
        articleDiv.append(icondiv, title, textDiv);
        contentDiv.append(articleDiv);
      }
      index__card.append(contentDiv);
      contentDiv.setAttribute("id", obj.id);
      contentDiv.setAttribute("onclick", "selectid(this.id)");
      if (obj["gender"] == "F") {
        icon.classList.add("women");
      } else {
        icon.classList.add("man");
      }
    }
  });
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
