async function fetchData() {
    try {
        const [whalesRes, historyRes, configRes, oppsRes] = await Promise.all([
            fetch('/api/whales'),
            fetch('/api/history'),
            fetch('/api/config'),
            fetch('/api/opportunities')
        ]);

        const whales = await whalesRes.json();
        const history = await historyRes.json();
        const config = await configRes.json();
        const opportunities = await oppsRes.json();

        updateDashboard(whales, history, config, opportunities);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateDashboard(whales, history, config, opportunities) {
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

    // Update Settings (populate input fields)
    document.getElementById('setting-mode').textContent = config.paper_trading ? 'Paper Trading' : 'Real Trading';
    document.getElementById('setting-capital').textContent = `$${balance.toFixed(2)}`;

    document.getElementById('input-max-position').value = config.max_position_size;
    document.getElementById('input-stop-loss').value = (config.stop_loss * 100).toFixed(0);
    document.getElementById('input-take-profit').value = (config.take_profit * 100).toFixed(0);
    document.getElementById('input-max-positions').value = config.max_positions;
    document.getElementById('input-min-score').value = config.min_whale_score;
    document.getElementById('input-scan-interval').value = config.scan_interval;

    // Update Opportunities
    // Trending Markets
    const trendingHtml = (opportunities.trending || []).map(m => `
        <tr>
            <td>${m.question}</td>
            <td>$${Math.round(m.volume).toLocaleString()}</td>
            <td><a href="https://polymarket.com/event/${m.slug}" target="_blank">Voir</a></td>
        </tr>
    `).join('');
    document.getElementById('trending-table').innerHTML = trendingHtml || '<tr><td colspan="3">Aucune donnée</td></tr>';

    // Price Movements
    const movementsHtml = (opportunities.price_movements || []).map(m => `
        <tr>
            <td>${m.market_id.substring(0, 10)}...</td>
            <td>${m.direction} ${m.change}</td>
            <td>${new Date(m.detected_at).toLocaleTimeString()}</td>
        </tr>
    `).join('');
    document.getElementById('movements-table').innerHTML = movementsHtml || '<tr><td colspan="3">Aucun mouvement détecté</td></tr>';

    // Keywords
    const keywordsHtml = (opportunities.keywords || []).map(k => `
        <div class="keyword-card">
            <div class="category">${k.category}</div>
            <div class="question">${k.question}</div>
            <div class="volume">Volume: $${Math.round(k.volume).toLocaleString()}</div>
        </div>
    `).join('');
    document.getElementById('keywords-grid').innerHTML = keywordsHtml || '<p>Aucune alerte</p>';

    // News
    const newsHtml = (opportunities.news || []).map(n => `
        <div class="news-item">
            <div class="news-source">${n.source} • ${new Date(n.published_at).toLocaleTimeString()}</div>
            <div class="news-title"><a href="${n.url}" target="_blank">${n.title}</a></div>
        </div>
    `).join('');
    document.getElementById('news-list').innerHTML = newsHtml || '<p>Aucune actualité récente</p>';
}

async function saveSettings() {
    const settings = {
        max_position_size: parseFloat(document.getElementById('input-max-position').value),
        stop_loss: parseFloat(document.getElementById('input-stop-loss').value) / 100,
        take_profit: parseFloat(document.getElementById('input-take-profit').value) / 100,
        max_positions: parseInt(document.getElementById('input-max-positions').value),
        min_whale_score: parseInt(document.getElementById('input-min-score').value),
        scan_interval: parseInt(document.getElementById('input-scan-interval').value)
    };

    try {
        const response = await fetch('/api/config/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(settings)
        });

        if (response.ok) {
            alert('✅ Paramètres sauvegardés ! Redémarrez le bot pour appliquer les changements.');
        } else {
            alert('❌ Erreur lors de la sauvegarde');
        }
    } catch (error) {
        alert('❌ Erreur: ' + error.message);
    }
}

// Refresh every 5 seconds
fetchData();
setInterval(fetchData, 5000);
