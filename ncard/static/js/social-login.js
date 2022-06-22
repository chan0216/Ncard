function handleCredentialResponse(response) {
  fetch(`/api/user`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_token: response.credential,
      signintype: "Google",
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data["ok"]) {
        window.location.replace("/");
      }
    });
}
