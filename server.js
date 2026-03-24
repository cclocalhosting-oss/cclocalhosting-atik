const express = require("express");
const multer = require("multer");
const path = require("path");

const app = express();

// storage setup
const storage = multer.diskStorage({
  destination: "./uploads/",
  filename: function (req, file, cb) {
    cb(null, Date.now() + path.extname(file.originalname));
  },
});

const upload = multer({ storage: storage });

// serve static files
app.use(express.static("public"));
app.use("/uploads", express.static("uploads"));

// upload route
app.post("/upload", upload.single("video"), (req, res) => {
  res.send("Video uploaded successfully!");
});

// get videos
const fs = require("fs");
app.get("/videos", (req, res) => {
  const files = fs.readdirSync("./uploads");
  res.json(files);
});

app.listen(3000, () => console.log("Server running on port 3000"));
