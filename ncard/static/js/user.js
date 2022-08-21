async function checkUserStatus() {
  const response = await fetch("/api/user");
  const data = await response.json();
  if (data.ok) {
    document.querySelector(".nav-stranger").style.display = "none";
    document.querySelector(".nav-user").style.visibility = "visible";
  } else {
    document.querySelector(".nav-stranger").style.display = "block";
    document.querySelector(".nav-user").style.display = "none";
  }
}
checkUserStatus();

async function deleteUser() {
  const response = await fetch("/api/user", { method: "DELETE" });
  const data = await response.json();
  if (data["ok"]) {
    location.reload();
  }
}
