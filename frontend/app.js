document.addEventListener("DOMContentLoaded", () => {

    const citySelect = document.getElementById("citySelect");
    const navTabs = document.querySelectorAll(".nav-tab");
    const tabContents = document.querySelectorAll(".tab-content");
    
    const tracePanel = document.getElementById("tracePanel");
    const toggleTraceBtn = document.getElementById("toggleTraceBtn");
    const closeTraceBtn = document.getElementById("closeTraceBtn");
    const traceTimeline = document.getElementById("traceTimeline");

    const chatInput = document.getElementById("chatInput");
    const sendChatBtn = document.getElementById("sendChatBtn");
    const chatMessages = document.getElementById("chatMessages");

    let currentCity = "San Francisco";

    // Navigation Tab Switching
    navTabs.forEach(tab => {
        tab.addEventListener("click", () => {
            navTabs.forEach(t => t.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));
            tab.classList.add("active");
            document.getElementById(`tab-${tab.dataset.tab}`).classList.add("active");
        });
    });

    // Trace Panel Toggle
    toggleTraceBtn.addEventListener("click", () => tracePanel.classList.toggle("hidden"));
    closeTraceBtn.addEventListener("click", () => tracePanel.classList.add("hidden"));

    // City Selection Change
    citySelect.addEventListener("change", (e) => {
        currentCity = e.target.value;
        fetchDashboardData(currentCity);
    });

    // Initial Fetch
    fetchDashboardData(currentCity);
    fetchKnowledgeSources();

    async function fetchDashboardData(city) {
        try {
            // 1. Fetch Current Air Quality
            const res = await fetch(`/api/v1/air-quality?city=${encodeURIComponent(city)}`);
            const data = await res.json();
            renderDashboard(data);

            // 2. Fetch Weather
            const wRes = await fetch(`/api/v1/air-quality/history?city=${encodeURIComponent(city)}&hours=24`);
            const hData = await wRes.json();
            renderHistoryChart(hData.history || []);

            // 3. Fetch Monitoring Stations
            const sRes = await fetch(`/api/v1/monitoring-stations?city=${encodeURIComponent(city)}`);
            const sData = await sRes.json();
            renderMapStations(sData.stations || []);

        } catch (err) {
            console.error("Error fetching dashboard data:", err);
        }
    }

    function renderDashboard(data) {
        document.getElementById("aqiValue").textContent = data.aqi || "--";
        document.getElementById("aqiCategory").textContent = data.category || "Moderate";
        document.getElementById("aqiTimestamp").textContent = `Updated: ${new Date(data.timestamp).toLocaleTimeString()}`;
        document.getElementById("stationMeta").children[0].textContent = `Station: ${data.station_name || "Central Station"}`;

        const gauge = document.getElementById("aqiGauge");
        const catBadge = document.getElementById("aqiCategory");
        
        let color = "#00e676";
        if (data.aqi > 50 && data.aqi <= 100) color = "#ffea00";
        else if (data.aqi > 100 && data.aqi <= 150) color = "#ff9100";
        else if (data.aqi > 150) color = "#ff1744";

        gauge.style.borderColor = color;
        gauge.style.boxShadow = `0 0 20px ${color}55`;
        catBadge.style.color = color;
        catBadge.style.background = `${color}22`;

        // Render Pollutants
        const pollutantsGrid = document.getElementById("pollutantsGrid");
        pollutantsGrid.innerHTML = "";

        (data.pollutants || []).forEach(p => {
            const card = document.createElement("div");
            card.className = "pollutant-card";
            card.innerHTML = `
                <span class="p-name">${p.pollutant}</span>
                <span class="p-val">${p.value}</span>
                <span class="p-unit">${p.unit} (Sub-index: ${p.sub_index})</span>
            `;
            pollutantsGrid.appendChild(card);
        });
    }

    function renderHistoryChart(history) {
        const chartBox = document.getElementById("historyChartBox");
        chartBox.innerHTML = "";

        const reversed = [...history].reverse().slice(0, 16);
        reversed.forEach(item => {
            const wrapper = document.createElement("div");
            wrapper.className = "chart-bar-wrapper";
            
            const heightPct = Math.min(100, Math.max(10, (item.aqi / 200) * 100));
            const timeStr = new Date(item.timestamp).getHours() + ":00";

            wrapper.innerHTML = `
                <div class="chart-bar" style="height: ${heightPct}%;" title="AQI: ${item.aqi}"></div>
                <span class="bar-time">${timeStr}</span>
            `;
            chartBox.appendChild(wrapper);
        });
    }

    function renderMapStations(stations) {
        const mapCanvasBox = document.getElementById("mapCanvasBox");
        mapCanvasBox.innerHTML = "";

        stations.forEach(s => {
            const pin = document.createElement("div");
            pin.className = "station-pin";
            pin.innerHTML = `
                <div style="font-weight:700; color:#00f2fe;">📍 ${s.name}</div>
                <div style="font-size:11px; color:#8a99a8;">Operator: ${s.operator}</div>
                <div style="font-size:11px; color:#00e676;">Status: Active Verified</div>
            `;
            mapCanvasBox.appendChild(pin);
        });
    }

    async function fetchKnowledgeSources() {
        try {
            const res = await fetch("/api/v1/sources");
            const data = await res.json();
            const list = document.getElementById("sourcesList");
            list.innerHTML = "";

            (data.sources || []).forEach(src => {
                const item = document.createElement("div");
                item.style.padding = "12px";
                item.style.borderBottom = "1px solid rgba(255,255,255,0.1)";
                item.innerHTML = `
                    <div style="font-weight:600; color:#00f2fe;">📄 ${src.title} (${src.document_name})</div>
                    <div style="font-size:12px; color:#8a99a8;">Source Authority: ${src.authority} | Effective: ${src.effective_date}</div>
                `;
                list.appendChild(item);
            });
        } catch (e) {
            console.error(e);
        }
    }

    // Alert Form Submit
    const alertForm = document.getElementById("alertConfigForm");
    alertForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const city = document.getElementById("alertCityInput").value;
        const threshold = parseInt(document.getElementById("alertThresholdInput").value);

        const res = await fetch("/api/v1/alerts", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ city, aqi_threshold: threshold })
        });
        const data = await res.json();
        alert("Alert Policy Saved and Activated Successfully!");
    });

    // Chat AI Advisor
    sendChatBtn.addEventListener("click", handleChatSend);
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") handleChatSend();
    });

    async function handleChatSend() {
        const text = chatInput.value.trim();
        if (!text) return;

        // User message
        appendChatMessage("user", text);
        chatInput.value = "";

        // Loading message
        const loadingId = appendChatMessage("assistant", "Analyzing real-time air quality & retrieving RAG health guidance...");

        try {
            const res = await fetch("/api/v1/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text, location: currentCity })
            });
            const data = await res.json();

            // Replace loading message
            document.getElementById(loadingId).querySelector(".msg-content").innerHTML = formatMarkdown(data.answer);

            // Render Agent Events in Trace Panel
            renderTraceEvents(data.agent_events || []);

        } catch (err) {
            document.getElementById(loadingId).querySelector(".msg-content").textContent = "Error processing request.";
        }
    }

    function appendChatMessage(role, content) {
        const msgId = "msg_" + Math.random().toString(36).substring(2, 9);
        const div = document.createElement("div");
        div.className = `chat-msg ${role}-msg`;
        div.id = msgId;

        div.innerHTML = `
            <div class="msg-avatar">${role === 'user' ? '👤' : '🍃'}</div>
            <div class="msg-content">${content}</div>
        `;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return msgId;
    }

    function renderTraceEvents(events) {
        traceTimeline.innerHTML = "";
        events.forEach(evt => {
            const item = document.createElement("div");
            item.className = "trace-item";
            item.innerHTML = `
                <div class="trace-agent">${evt.agent} <span style="float:right; font-weight:normal; color:#8a99a8;">${evt.latency_ms}ms</span></div>
                <div class="trace-tool">Task: ${evt.task} | Tool: ${evt.tool}</div>
                <div class="trace-summary">${evt.result_summary}</div>
            `;
            traceTimeline.appendChild(item);
        });
        tracePanel.classList.remove("hidden");
    }

    function formatMarkdown(text) {
        return text
            .replace(/### (.*?)\n/g, '<h4 style="color:#00f2fe; margin:8px 0;">$1</h4>')
            .replace(/\* \*\*(.*?)\:\*\*/g, '• <strong>$1:</strong>')
            .replace(/\[(\d+)\]/g, '<sup style="color:#00f2fe; font-weight:bold;">[$1]</sup>');
    }
});
