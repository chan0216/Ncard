document.querySelector(".submit").addEventListener("click", () => {
  let contenteditable = document.querySelector("[contenteditable]");
  let postText = contenteditable.innerHTML;
  let postTitle = document.querySelector(".newpost__title").value;
  // console.log(postTitle, postText);
  // contenteditable.innerHTML = postText;
  //文章列表顯示
  //   const text = postText
  //   .replace(/<div>/g, "\n")
  //   .replace(/<\/div>/g, "")
  //   .replace(/<br>/g, "\n");
  //   contenteditable.innerHTML = text;
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
      let newpost__content = document.querySelector(".newpost__content");
      newpost__content.append(imageDiv);
    });
});
