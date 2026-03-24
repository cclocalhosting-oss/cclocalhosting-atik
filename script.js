function downloadVideo() {
  let url = document.getElementById("videoUrl").value;
  let message = document.getElementById("message");

  if (url === "") {
    message.innerText = "Please enter a video URL!";
    return;
  }

  try {
    let a = document.createElement("a");
    a.href = url;
    a.download = "video.mp4";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    message.style.color = "green";
    message.innerText = "Download started!";
  } catch (error) {
    message.style.color = "red";
    message.innerText = "Invalid URL or download failed!";
  }
}
