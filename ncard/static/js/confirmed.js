fetch("/api/unconfirmed")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    if (data.data) {
      document.querySelector("body").style.visibility = "visible";
    } else {
      window.location.replace("/");
    }
  });
