const express = require("express");
const ytdlp = require("yt-dlp-exec");

const app = express();

app.get("/download", async (req, res) => {
  const url = req.query.url;

  try {
    const output = "video.mp4";
    await ytdlp(url, { output });

    res.download(output);
  } catch (err) {
    res.send("Error downloading video");
  }
});

app.listen(3000, () => console.log("Server running"));
