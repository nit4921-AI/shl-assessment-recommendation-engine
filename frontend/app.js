const API = "";

function apiUrl(path) {
  return `${API}${path}`;
}

function createCard(rec) {
  const name = rec.assessment_name || "Unknown";
  const url = rec.url || "#";
  const type = rec.test_type || "K";
  const score = rec.score ? rec.score.toFixed(3) : "-";
  const badgeClass = type.toUpperCase() === "P" ? "badge p" : "badge k";
  return `
    <div class="card">
      <div class="title"><a href="${url}" target="_blank">${name}</a></div>
      <div class="meta">
        <span class="${badgeClass}">${type}</span>
        <span>Score: ${score}</span>
      </div>
    </div>
  `;
}

async function checkAPI() {
  const statusEl = document.getElementById("apiStatus");
  try {
    const res = await fetch(apiUrl("/health"));
    if (res.ok) {
      statusEl.textContent = "API: OK";
      statusEl.style.color = "green";
    } else {
      statusEl.textContent = "API Unavailable";
      statusEl.style.color = "red";
    }
  } catch (err) {
    statusEl.textContent = "Cannot reach API";
    statusEl.style.color = "red";
  }
}

async function getRecommendations() {
  const query = document.getElementById("query").value.trim();
  const btn = document.getElementById("btn");
  const resultBox = document.getElementById("results");
  const topk = parseInt(document.getElementById("topk").value, 10);
  const balance = document.getElementById("balance").checked;

  if (!query) {
    alert("Please enter a query.");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Loading...";
  resultBox.innerHTML = "";

  try {
    const res = await fetch(apiUrl("/recommend"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, top_k: topk, balance }),
    });

    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    const items = data.recommendations || [];
    resultBox.innerHTML = items.length
      ? items.map(createCard).join("")
      : "<p>No recommendations found.</p>";
  } catch (err) {
    alert("Error: " + err.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "Get Recommendations";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("btn").addEventListener("click", getRecommendations);
  document.getElementById("query").addEventListener("keydown", e => {
    if (e.key === "Enter") getRecommendations();
  });
  checkAPI();
});
