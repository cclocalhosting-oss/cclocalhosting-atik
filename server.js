const express = require("express");
const cors = require("cors");
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

const app = express();
app.use(cors());
app.use(express.json());

app.post("/download", async (req, res) => {
  const { url } = req.body;

  try {
    // Example free API (change if needed)
    const api = `https://api.vevioz.com/api/button/mp4?url=${url}`;

    res.json({
      download_url: api
    });

  } catch (err) {
    res.status(500).json({ error: "Failed" });
  }
});

app.listen(3000, () => console.log("Server running"));
