async function fetchData() {
    try {
        const [whalesRes, historyRes, configRes] = await Promise.all([
            fetch('/api/whales'),
            fetch('/api/history'),
            fetch('/api/config')
        ]);

        const whales = await whalesRes.json();
        const history = await historyRes.json();
        const config = await configRes.json();

        updateDashboard(whales, history, config);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateDashboard(whales, history, config) {
    // Update Stats
    const whaleList = Object.entries(whales).map(([addr, data]) => ({ addr, ...data }));
    document.getElementById('total-whales').textContent = whaleList.length;

    const positions = history.positions || {};
    const activePositions = Object.values(positions).filter(p => p.status === 'OPEN').length;
    document.getElementById('active-positions').textContent = activePositions;

    const balance = history.balance || 0;
    document.getElementById('balance').textContent = `$${balance.toFixed(2)}`;

    // Update Whales Table
    const sortedWhales = whaleList.sort((a, b) => (b.score || 0) - (a.score || 0)).slice(0, 10);
    const whalesHtml = sortedWhales.map((w, i) => `
        <tr>
            <td>#${i + 1}</td>
            <td>${w.addr.substring(0, 8)}...</td>
            <td>${w.score || '-'}</td>
            <td>$${Math.round(w.total_volume).toLocaleString()}</td>
            <td>${(w.tags || []).map(t => `<span class="tag">${t}</span>`).join('')}</td>
        </tr>
    `).join('');
    document.getElementById('whales-table').innerHTML = whalesHtml;

    // Update History Table
    const trades = Object.values(positions).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 10);
    const historyHtml = trades.map(t => `
        <tr>
            <td>${new Date(t.timestamp).toLocaleTimeString()}</td>
            <td>${t.market_id.substring(0, 8)}...</td>
            <td>${t.outcome}</td>
            <td>$${t.amount_invested.toFixed(2)}</td>
            <td>${t.whale.substring(0, 8)}...</td>
        </tr>
    `).join('');
    document.getElementById('history-table').innerHTML = historyHtml;

    // Update Settings
    document.getElementById('setting-mode').textContent = config.paper_trading ? 'Paper Trading' : 'Real Trading';
    document.getElementById('setting-capital').textContent = `$${balance.toFixed(2)}`;
    document.getElementById('setting-max-position').textContent = `$${config.max_position_size}`;
    const percentPerTrade = (config.max_position_size / 1000 * 100).toFixed(1);
    document.getElementById('setting-percent').textContent = `${percentPerTrade}%`;
    document.getElementById('setting-stop-loss').textContent = `${(config.stop_loss * 100).toFixed(0)}%`;
    document.getElementById('setting-take-profit').textContent = `${(config.take_profit * 100).toFixed(0)}%`;
    document.getElementById('setting-max-positions').textContent = config.max_positions;
    document.getElementById('setting-min-score').textContent = config.min_whale_score;
}

// Refresh every 5 seconds
fetchData();
setInterval(fetchData, 5000);
