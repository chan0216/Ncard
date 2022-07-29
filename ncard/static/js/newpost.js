async function newPost() {
  let contenteditable = document.querySelector("[contenteditable]");
  let postText = contenteditable.innerHTML;
  let postTitle = document.querySelector(".newpost__title").value;
  if (postText == "" || postTitle == "") {
    document.querySelector(".warning").textContent = "請輸入完整";
    return;
  }

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
  const newPost = {
    postTitle: document.querySelector(".newpost__title").value,
    postText: contenteditable.innerHTML.replace(/<\/?span.*?>/g, ""),
    timenow: now,
  };
  const config = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(newPost),
  };
  const response = await fetch("/api/post", config);
  const data = await response.json();
  if (data.error) {
    document.querySelector(".warning").textContent = "請先登入";
    document.querySelector(".submit").disabled = true;
    return;
  }
  if (data.ok) {
    window.location.replace("/");
  }
}

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
      let newpostContent = document.querySelector(".newpost__content");
      newpostContent.append(imageDiv);
    });
});
fetch("/api/validation")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    if (data.error) {
      document.querySelector(".submit").disabled = true;
      document.querySelector(".Prompt ").textContent = "請先登入才能發文喔！";
      return;
    }
    if (data.data) {
      if (data.data.gender == "F") {
        let newpostData = document.querySelector(".newpost__data");
        let women = document.querySelector(".women");
        women.style.display = "block";
        let school = document.createElement("p");
        school.textContent = data.data.school;
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
        newpostData.append(school, now);
      } else if (data.data.gender == "M") {
        let newpostData = document.querySelector(".newpost__data");
        let man = document.querySelector(".man");
        man.style.display = "block";
        let school = document.createElement("p");
        school.textContent = data.data.school;
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
        newpostData.append(school, now);
      }
    } else {
      document.querySelector(".submit").disabled = true;
      document.querySelector(".Prompt ").textContent =
        "請先填基本資料才能發文喔！";
    }
  });
