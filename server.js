const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.static("public")); // serve frontend

// API route
app.post("/download", (req, res) => {
  const { url } = req.body;

  if (!url) {
    return res.json({ error: "No URL provided" });
  }

  const command = `yt-dlp -f best -g "${url}" --no-warnings`;

  exec(command, (error, stdout, stderr) => {
    if (error || !stdout) {
      console.log(stderr);
      return res.json({ error: "Download failed" });
    }

    const link = stdout.toString().trim();

    res.json({ link });
  });
});

// test route
app.get("/", (req, res) => {
  res.send("Server Running 🚀");
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => {
  console.log("Server running on port " + PORT);
});
