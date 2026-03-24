function downloadVideo() {
  var url = document.getElementById("link").value;

  if (url === "") {
    alert("Please enter a link!");
  } else {
    document.getElementById("result").innerHTML =
      "Download link: <a href='" + url + "' target='_blank'>Click Here</a>";
  }
}
