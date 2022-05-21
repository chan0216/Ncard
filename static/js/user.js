fetch("/api/user")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    if (data.ok) {
      document.querySelector(".nav-stranger").style.display = "none";
      document.querySelector(".nav-user").style.visibility = "visible";
    } else {
      document.querySelector(".nav-stranger").style.display = "block";
      document.querySelector(".nav-user").style.display = "none";
    }
  });
