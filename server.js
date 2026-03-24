const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

app.post("/download", async (req, res) => {
  const { url } = req.body;

  // ⚠️ এখানে real API call হবে
  // Example (fake API)
  const api = `https://example-api.com/download?url=${url}`;

  try {
    const response = await fetch(api);
    const data = await response.json();

    res.json({
      download_url: data.link
    });

  } catch (error) {
    res.status(500).json({ error: "Download failed" });
  }
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
