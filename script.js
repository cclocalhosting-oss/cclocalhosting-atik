async function download() {
  const url = document.getElementById("url").value;

  const res = await fetch("http://localhost:5000/api/download", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url })
  });

  const data = await res.json();

  let html = `<h3>${data.title}</h3>`;
  html += `<img src="${data.thumbnail}" width="200">`;

  data.formats.forEach(f => {
    html += `<p>
      <a href="${f.url}" target="_blank">Download ${f.format_note || "video"}</a>
    </p>`;
  });

  document.getElementById("result").innerHTML = html;
}
