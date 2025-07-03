// ✅ Utility: update UI text content
function setText(id, value) {
  document.getElementById(id).textContent = value;
}

// 🌱 Fetch status data from /status/<zone>
async function fetchStatus(zone, mappings = {}) {
  try {
    const res = await fetch(`/status/${zone}`);
    const data = await res.json();
    const container = document.getElementById(`${zone}Status`);
    container.innerHTML = "";

    Object.entries(data.readings).forEach(([key, val]) => {
      const label = mappings[key] || key;
      const card = document.createElement("div");
      card.className = "card";
      card.innerHTML = `<h3>${label}</h3><p>${val}</p>`;
      container.appendChild(card);
    });

    setText("lastSync", new Date().toLocaleTimeString());
  } catch (err) {
    console.error("Status fetch error:", err);
  }
}

// 🕹️ Send control command to /control/relay
async function sendCommand(node, channel, state) {
  const payload = { node, channel, state };
  await fetch("/control/relay", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
}

// 🛏️ Render bed valve buttons
function renderBedControls(beds) {
  const container = document.getElementById("bedValvesControl");
  container.innerHTML = "";
  beds.forEach((bed) => {
    const row = document.createElement("div");
    row.className = "card";
    row.innerHTML = `
      <h3>${bed}</h3>
      <button onclick="sendCommand('bed_valves', '${bed}', 'on')">ON</button>
      <button onclick="sendCommand('bed_valves', '${bed}', 'off')">OFF</button>
    `;
    container.appendChild(row);
  });
}

// 🤖 Get irrigation advice
async function fetchAdvice(zone) {
  try {
    const res = await fetch("/advice", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ zone }),
    });
    const data = await res.json();
    const panel = document.getElementById("advicePanel");
    panel.innerHTML = `
      <p>Zone: ${data.zone}</p>
      <p>→ ${data.recommendation.action} for ${data.recommendation.duration_min || "?"} min</p>
    `;
  } catch (err) {
    console.error("Advice fetch error:", err);
  }
}

// 🔁 Refresh everything
function refreshDashboard() {
  fetchStatus("sourceRouter", {
    source_selector: "Source",
    fertilizer_bypass: "Fertilizer",
    output_selector: "Destination",
    main_garden_flow: "Main Flow
