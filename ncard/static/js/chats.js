const socket = io();
function hidemessage() {
  document.querySelector(".full__content").style.display = "none";
}
function showmessage() {
  fetch("/api/verify")
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data.data) {
        document.querySelector(".full__content").style.display = "block";
      }
    });
}

fetch("/api/friends")
  .then((res) => res.json())
  .then((data) => {
    let res = data.data;
    res.forEach((friend) => {
      renderFriends(friend);
    });
  });
function renderFriends(friend) {
  const friendList = document.querySelector(".friend__list");
  const msgDiv = document.createElement("div");
  //顯示朋友名字
  const friendName = document.createElement("h6");
  friendName.textContent = friend.name;
  friendName.classList.add("friend__name");
  //顯示最新訊息
  const friendMsg = document.createElement("p");
  friendMsg.textContent = friend.message;
  friendMsg.classList.add("friend__msg");
  msgDiv.classList.add("msg__div");
  msgDiv.append(friendName, friendMsg);
  //顯示頭像
  const imgDiv = document.createElement("div");
  const friendImage = document.createElement("img");
  friendImage.src = friend.image;
  imgDiv.classList.add("img__div");
  friendImage.classList.add("friend__image");
  imgDiv.append(friendImage);
  //外框連結
  const friendFrame = document.createElement("a");
  friendFrame.classList.add("friend__frame");
  friendFrame.append(imgDiv, msgDiv);
  friendList.append(friendFrame);
  const chatsHref = `/chats/${friend.room_id}`;
  friendFrame.href = chatsHref;
}
//得到聊天訊息
const msgRoomId = location.pathname.split("/").pop();
const chatsAPI = `/api/chats/${msgRoomId}?page=`;
let chastPage = 0;
let options = { threshold: 0.1 };
// let renderNextPage = (entries) => {
//   entries.forEach((entry) => {
//     if (entry.isIntersecting) {
//       renderMessages();
//     }
//   });
// };
let userId, userName, userImg, friendId, friendName, friendImg;
async function renderMessages() {
  const res = await fetch(chatsAPI + chastPage);
  const data = await res.json();
  if (data.error) {
    console.log(data.message);
    const msgDiv = document.querySelector(".messages__div");
    msgDiv.textContent = data.message;
    document.querySelector(".submit").disabled = true;
    return;
  }
  if (data.data) {
    const info = data.data;
    const user = info.user;
    const friend = info.friend;
    userId = user.user_id;
    userName = user.name;
    userImg = user.image;
    friendId = friend.friend_id;
    friendName = friend.name;
    friendImg = friend.image;
    //render聊天室nav
    const friendNav = document.querySelector(".friend__nav");
    const friendInner = document.createElement("div");
    friendInner.classList.add("friend__inner");
    let h6 = document.createElement("h6");
    h6.textContent = friendName;
    let photoDiv = document.createElement("div");
    photoDiv.classList.add("photo__div");
    let photo = document.createElement("img");
    photo.classList.add("profile__photo");
    photo.src = friendImg;
    photoDiv.append(photo);
    friendInner.append(photoDiv, h6);
    friendNav.append(friendInner);
    //render訊息
    info.messages.forEach((message) => {
      let messagesDiv = document.querySelector(".messages__div");
      //render發送者照片
      const profilePicture = document.createElement("img");
      profilePicture.classList.add("profile__photo");
      profilePicture.src = message.userId === userId ? userImg : friendImg;
      let photoDiv = document.createElement("div");
      photoDiv.classList.add("photo__div");
      photoDiv.append(profilePicture);
      //render訊息傳送人
      const messageUser = document.createElement("h6");
      messageUser.textContent =
        message.userId === userId ? userName : friendName;
      messageUser.classList.add("message__user");
      //render 訊息
      const msgText = document.createElement("p");
      msgText.textContent = message.message;
      msgText.classList.add("msg__text");
      const contentDiv = document.createElement("div");
      contentDiv.append(messageUser, msgText);
      const talkDiv = document.createElement("div");
      talkDiv.classList.add("talk__div");
      //render時間
      const createTime = document.createElement("p");
      createTime.textContent = message.time;
      createTime.classList.add("create__time");
      //render聊天外框
      const rightDiv = document.createElement("div");
      rightDiv.append(createTime);
      const leftDiv = document.createElement("div");
      leftDiv.classList.add("left__div");
      leftDiv.append(photoDiv, contentDiv);
      talkDiv.append(leftDiv, rightDiv);
      messagesDiv.append(talkDiv);
    });
  }
}
renderMessages();
socket.on("connect", function () {
  fetch("/api/chats")
    .then((res) => res.json())
    .then((data) => {
      if (data.data == null) {
        console.log("null");
        document.querySelector(".messages__div").textContent =
          "你還沒有聊天室喔";
        document.querySelector(".submit").disabled = true;
        return;
      }
      if (data.data) {
        data.data.forEach((roomId) => {
          socket.emit("join_room", roomId.toString());
        });
      }
    });
});

function sendMessage() {
  const messageText = document.querySelector("#messageText");
  socket.emit("send_message", {
    userId: userId,
    name: userName,
    userImg: userImg,
    room: msgRoomId,
    message: messageText.value,
  });
  hidemessage();
}
socket.on("receive_message", (data) => {
  if (data.room == msgRoomId) {
    receiveMessage(data);
  }
  updatefriend(data);
});
function receiveMessage(data) {
  let messagesDiv = document.querySelector(".messages__div");
  //render發送者照片
  const profilePicture = document.createElement("img");
  profilePicture.classList.add("profile__photo");
  profilePicture.src = data.userImg;
  let photoDiv = document.createElement("div");
  photoDiv.classList.add("photo__div");
  photoDiv.append(profilePicture);
  //render訊息傳送人
  const messageUser = document.createElement("h6");
  messageUser.textContent = data.name;
  messageUser.classList.add("message__user");
  //render 訊息
  const msgText = document.createElement("p");
  msgText.textContent = data.message;
  msgText.classList.add("msg__text");
  const contentDiv = document.createElement("div");
  contentDiv.append(messageUser, msgText);
  const talkDiv = document.createElement("div");
  talkDiv.classList.add("talk__div");
  //render時間
  const createTime = document.createElement("p");
  createTime.textContent = data.time;
  createTime.classList.add("create__time");
  //render聊天外框
  const rightDiv = document.createElement("div");
  rightDiv.append(createTime);
  const leftDiv = document.createElement("div");
  leftDiv.classList.add("left__div");
  leftDiv.append(photoDiv, contentDiv);
  talkDiv.append(leftDiv, rightDiv);
  messagesDiv.append(talkDiv);
}
function updatefriend(data) {
  const updatemsg = document.querySelector(`a[href='/chats/${data.room}']`);
  const updateText = updatemsg.querySelector(".friend__msg");
  updateText.textContent = data.message;
  document.querySelector(".friend__list").prepend(updatemsg);
}
