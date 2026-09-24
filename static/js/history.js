// history.js
// Fetches the logged predictions from the backend and renders them into
// the history table.

async function loadHistory() {
    const res = await fetch('/api/history');
    const rows = await res.json();

    const tbody = document.getElementById('historyBody');
    const emptyState = document.getElementById('emptyState');

    if (rows.length === 0) {
        emptyState.style.display = 'block';
        return;
    }

    tbody.innerHTML = rows.map(r => `
        <tr>
            <td>${r.created_at}</td>
            <td>${r.tenth_percent}</td>
            <td>${r.twelfth_percent}</td>
            <td>${r.entrance_score}</td>
            <td>${r.category}</td>
            <td>${r.probability}%</td>
            <td><span class="badge ${r.prediction === 'High Chance' ? 'high' : 'low'}">${r.prediction}</span></td>
        </tr>
    `).join('');
}

loadHistory();
