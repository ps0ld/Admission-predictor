// dashboard.js
// Handles the prediction form: submits the profile to the backend,
// animates the probability gauge, and renders the feature importance
// breakdown returned by the trained model.

const GAUGE_CIRCUMFERENCE = 283; // approximate arc length of the gauge path

async function loadStats() {
    const res = await fetch('/api/stats');
    const stats = await res.json();
    document.getElementById('statTotal').textContent = stats.total_predictions;
    document.getElementById('statAvg').textContent =
        stats.total_predictions > 0 ? `${stats.average_probability}%` : '—';
}

function animateGauge(probability) {
    const arc = document.getElementById('gaugeArc');
    const offset = GAUGE_CIRCUMFERENCE - (GAUGE_CIRCUMFERENCE * probability) / 100;
    arc.style.transition = 'stroke-dashoffset 0.9s ease, stroke 0.4s ease';
    arc.style.strokeDashoffset = offset;
    arc.style.stroke = probability >= 50 ? '#2FE6C6' : '#FF6B7A';

    let current = 0;
    const target = Math.round(probability);
    const valueEl = document.getElementById('gaugeValue');
    const timer = setInterval(() => {
        current += Math.max(1, Math.round(target / 30));
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        valueEl.textContent = `${current}%`;
    }, 20);
}

function renderFactorBars() {
    const container = document.getElementById('factorBars');
    const items = window.FEATURE_IMPORTANCE || [];
    container.innerHTML = items.map(item => `
        <div class="factor-row">
            <div class="factor-label"><span>${item.label}</span><span>${item.value}%</span></div>
            <div class="factor-track">
                <div class="factor-fill" style="width: ${item.value}%;"></div>
            </div>
        </div>
    `).join('');
}

document.getElementById('predictForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
        tenth_percent: document.getElementById('tenth').value,
        twelfth_percent: document.getElementById('twelfth').value,
        entrance_score: document.getElementById('entrance').value,
        category: document.getElementById('category').value,
        previous_year_cutoff: document.getElementById('cutoff').value
    };

    const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    const data = await res.json();

    document.getElementById('resultEmpty').style.display = 'none';
    document.getElementById('resultContent').style.display = 'block';

    animateGauge(data.probability);
    renderFactorBars();

    const tag = document.getElementById('resultTag');
    tag.textContent = data.prediction;
    tag.className = 'result-tag ' + (data.prediction === 'High Chance' ? 'high' : 'low');

    loadStats();
});

renderFactorBars();
loadStats();
