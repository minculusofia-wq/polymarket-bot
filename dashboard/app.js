async function fetchData() {
    try {
        const [whalesRes, historyRes, configRes, oppsRes, whitelistRes, signalsRes] = await Promise.all([
            fetch('/api/whales'),
            fetch('/api/history'),
            fetch('/api/config'),
            fetch('/api/opportunities'),
            fetch('/api/whitelist'),
            fetch('/api/signals')
        ]);

        const whales = await whalesRes.json();
        const history = await historyRes.json();
        const config = await configRes.json();
        const opportunities = await oppsRes.json();
        const whitelist = await whitelistRes.json();
        const signals = await signalsRes.json();

        updateDashboard(whales, history, config, opportunities, whitelist, signals);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function updateDashboard(whales, history, config, opportunities, whitelist, signals) {
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
            <td>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <code style="font-size: 0.85em;">${w.addr}</code>
                    <button onclick="copyAddress('${w.addr}')" style="padding: 4px 8px; font-size: 0.8em; cursor: pointer;">📋</button>
                </div>
            </td>
            <td>${w.score || '-'}</td>
            <td>$${Math.round(w.total_volume).toLocaleString()}</td>
            <td>${(w.tags || []).map(t => `<span class="tag">${t}</span>`).join('')}</td>
        </tr>
    `).join('');
    document.getElementById('whales-table').innerHTML = whalesHtml;

    // Render Followed Traders
    renderFollowedTraders(whales, positions);

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

    const autoCopyCheckbox = document.getElementById('auto-copy-sells');
    if (autoCopyCheckbox) {
        autoCopyCheckbox.checked = config.auto_copy_sells || false;
    }

    // Update trading mode display
    const isPaperTrading = config.paper_trading;
    const modeLabel = document.getElementById('mode-label');
    const toggleBtn = document.getElementById('toggle-mode-btn');

    if (isPaperTrading) {
        modeLabel.textContent = '📝 Paper Trading';
        modeLabel.style.color = '#667eea';
        toggleBtn.textContent = '🔄 Passer au Real Trading';
        toggleBtn.classList.remove('real-mode');
    } else {
        modeLabel.textContent = '💰 Real Trading';
        modeLabel.style.color = '#f5576c';
        toggleBtn.textContent = '🔄 Passer au Paper Trading';
        toggleBtn.classList.add('real-mode');
    }

    // Opportunities
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

    // Reddit
    const redditHtml = (opportunities.reddit || []).map(r => `
        <div class="news-item" style="border-left-color: #FF4500;">
            <div class="news-source">${r.source} • ${r.score} ⬆️ • ${r.comments} 💬</div>
            <div class="news-title"><a href="${r.url}" target="_blank">${r.title}</a></div>
        </div>
    `).join('');
    document.getElementById('reddit-list').innerHTML = redditHtml || '<p>Aucune discussion récente</p>';

    // Events
    const eventsHtml = (opportunities.events || []).map(e => `
        <div class="news-item" style="border-left-color: #8DC351;">
            <div class="news-source">📅 ${e.date}</div>
            <div class="news-title"><a href="${e.url}" target="_blank">${e.title}</a></div>
            <div class="news-source">${e.description.substring(0, 100)}...</div>
        </div>
    `).join('');
    document.getElementById('events-list').innerHTML = eventsHtml || '<p>Aucun événement à venir</p>';

    // Sentiment
    const sentimentHtml = (opportunities.sentiment || []).map(s => `
        <div class="keyword-card">
            <div class="category">${s.symbol}</div>
            <div class="question">${s.name}</div>
            <div class="volume">Galaxy Score: ${s.galaxy_score} 🚀</div>
        </div>
    `).join('');
    document.getElementById('sentiment-grid').innerHTML = sentimentHtml || '<p>Aucune donnée sentiment</p>';

    // Videos
    const videosHtml = (opportunities.videos || []).map(v => `
        <div class="news-item" style="border-left-color: #FF0000;">
            <div class="news-source">🎥 ${v.channel} • ${v.published}</div>
            <div class="news-title"><a href="${v.link}" target="_blank">${v.title}</a></div>
        </div>
    `).join('');
    document.getElementById('videos-list').innerHTML = videosHtml || '<p>Aucune vidéo récente</p>';

    // Whitelist
    const whitelistHtml = (whitelist || []).map(addr => `
        <tr>
            <td>${addr}</td>
            <td><button class="delete-btn" onclick="removeFromWhitelist('${addr}')">🗑️ Supprimer</button></td>
        </tr>
    `).join('');
    document.getElementById('whitelist-table').innerHTML = whitelistHtml || '<tr><td colspan="2">Aucun wallet whitelisté</td></tr>';

    // Store signals globally for filtering
    window.allSignals = signals || [];
    renderFilteredSignals();
}

function renderFollowedTraders(whales, positions) {
    const whaleList = Object.entries(whales).map(([addr, data]) => ({ addr, ...data }));
    const positionsList = Object.values(positions || {});

    // Get unique whale addresses from open positions
    const activeWhales = [...new Set(positionsList.filter(p => p.status === 'OPEN').map(p => p.whale))];

    // Filter whales that have active positions
    const followedWhales = whaleList.filter(w => activeWhales.includes(w.addr));

    const followedHtml = followedWhales.map(w => {
        const posCount = positionsList.filter(p => p.whale === w.addr && p.status === 'OPEN').length;
        return `
            <tr>
                <td>
                    <code>${w.addr}</code>
                    <button class="action-btn btn-copy" onclick="copyAddress('${w.addr}')">📋</button>
                </td>
                <td><strong>${w.score}</strong></td>
                <td>$${Math.round(w.volume).toLocaleString()}</td>
                <td><span class="tag">${posCount}</span></td>
                <td>
                    <button class="action-btn btn-view" onclick="viewWhaleActivity('${w.addr}')">👁️ Voir</button>
                </td>
            </tr>
        `;
    }).join('');

    document.getElementById('followed-traders-table').innerHTML = followedHtml || '<tr><td colspan="5">Aucun trader suivi actuellement (pas de positions ouvertes)</td></tr>';
}

function viewWhaleActivity(address) {
    alert(`Fonctionnalité à venir : Voir l'activité de ${address.substring(0, 10)}...`);
}

function renderFilteredSignals() {
    const minWhales = parseInt(document.getElementById('min-whales-slider').value);
    const minSources = parseInt(document.getElementById('min-sources-slider').value);

    // Filter signals based on current slider values
    const filteredSignals = (window.allSignals || []).filter(s =>
        s.nb_whales >= minWhales && s.nb_sources >= minSources
    );

    const signalsHtml = filteredSignals.map((s, idx) => `
        <tr>
            <td>${s.market_question}</td>
            <td><strong>${s.nb_whales}</strong> 🐋</td>
            <td><strong>${s.nb_sources}</strong> 📊</td>
            <td><span class="tag">${s.confidence_score}</span></td>
            <td>
                <button class="action-btn btn-details" onclick="showSignalDetails(${idx})">📊 Détails</button>
                <button class="action-btn btn-copy" onclick="copyWhaleFromSignal('${s.whales[0]?.address || ''}')">✅ Copier</button>
                <button class="action-btn btn-view" onclick="viewMarket('${s.market_id}')">🔗 Voir Bet</button>
            </td>
        </tr>
    `).join('');

    document.getElementById('signals-table').innerHTML = signalsHtml || '<tr><td colspan="5">Aucun signal ne correspond aux seuils actuels</td></tr>';
}

function showSignalDetails(index) {
    const minWhales = parseInt(document.getElementById('min-whales-slider').value);
    const minSources = parseInt(document.getElementById('min-sources-slider').value);

    // Get the same filtered array
    const filteredSignals = (window.allSignals || []).filter(s =>
        s.nb_whales >= minWhales && s.nb_sources >= minSources
    );

    const signal = filteredSignals[index];
    if (!signal) {
        alert('Signal introuvable');
        return;
    }

    const modalBody = document.getElementById('modal-body');
    modalBody.innerHTML = `
        <h4>Marché: ${signal.market_question}</h4>
        <p><strong>Market ID:</strong> <code>${signal.market_id}</code></p>
        <p><strong>Score de Confiance:</strong> ${signal.confidence_score}</p>
        <hr>
        <h5>🐋 Whales (${signal.nb_whales}):</h5>
        <ul>
            ${signal.whales.map(w => `
                <li>
                    <code>${w.address}</code> 
                    (Score: ${w.score}, Volume: $${Math.round(w.volume || 0)})
                    <button class="action-btn btn-copy" onclick="copyWhaleFromSignal('${w.address}')">➕ Copier</button>
                </li>
            `).join('')}
        </ul>
        <hr>
        <h5>📊 Sources (${signal.nb_sources}):</h5>
        <ul>
            ${signal.sources.map(s => `<li>${s}</li>`).join('')}
        </ul>
    `;

    document.getElementById('signal-modal').style.display = 'block';
}

function closeSignalModal() {
    document.getElementById('signal-modal').style.display = 'none';
}

async function copyWhaleFromSignal(address) {
    if (!address) {
        alert('❌ Adresse invalide');
        return;
    }

    try {
        await fetch('/api/whitelist', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address })
        });
        alert(`✅ Whale ${address.substring(0, 10)}... ajouté à la whitelist !`);
        fetchData(); // Refresh
    } catch (error) {
        alert('❌ Erreur: ' + error.message);
    }
}

function viewMarket(marketId) {
    // Polymarket uses conditionId to identify markets
    // We'll use the markets endpoint to find the correct event page
    // Format: https://polymarket.com/event/[slug]?tid=[tokenId]
    // Since we only have conditionId, we'll use a direct link that works
    const polymarketUrl = `https://polymarket.com/markets?_c=${marketId}`;
    window.open(polymarketUrl, '_blank');
}

async function addToWhitelist() {
    const input = document.getElementById('whitelist-input');
    const address = input.value.trim();
    if (!address) return;

    try {
        await fetch('/api/whitelist', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address })
        });
        input.value = '';
        fetchData(); // Refresh
    } catch (error) {
        alert('Erreur: ' + error.message);
    }
}

async function removeFromWhitelist(address) {
    if (!confirm(`Supprimer ${address} de la whitelist ?`)) return;

    try {
        await fetch('/api/whitelist', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ address })
        });
        fetchData(); // Refresh
    } catch (error) {
        alert('Erreur: ' + error.message);
    }
}

async function saveSettings() {
    const settings = {
        max_position_size: parseFloat(document.getElementById('input-max-position').value),
        stop_loss: parseFloat(document.getElementById('input-stop-loss').value) / 100,
        take_profit: parseFloat(document.getElementById('input-take-profit').value) / 100,
        max_positions: parseInt(document.getElementById('input-max-positions').value),
        max_traders: parseInt(document.getElementById('input-max-traders').value),
        min_whale_score: parseInt(document.getElementById('input-min-score').value),
        scan_interval: parseInt(document.getElementById('input-scan-interval').value),
        auto_copy_sells: document.getElementById('auto-copy-sells').checked
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

async function toggleTradingMode() {
    // Get current mode from config
    const response = await fetch('/api/config');
    const config = await response.json();
    const currentMode = config.paper_trading;
    const newMode = !currentMode;

    const modeText = newMode ? "Paper Trading" : "Real Trading";

    if (!newMode) {
        // Switching to Real Trading - show strong warning
        const confirmed = confirm(
            '⚠️ ATTENTION ⚠️\n\n' +
            'Vous êtes sur le point d\'activer le REAL TRADING.\n\n' +
            'Cela signifie que le bot utilisera de VRAIS FONDS.\n\n' +
            'Assurez-vous que:\n' +
            '1. Votre wallet est configuré\n' +
            '2. Vous comprenez les risques\n' +
            '3. Vous avez testé en Paper Trading\n\n' +
            'Voulez-vous vraiment continuer ?'
        );

        if (!confirmed) return;
    }

    try {
        const res = await fetch('/api/config/toggle-mode', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paper_trading: newMode })
        });

        const result = await res.json();

        if (result.status === 'success') {
            alert(`✅ ${result.message}`);
            fetchData(); // Refresh to update UI
        } else {
            alert('❌ Erreur: ' + result.message);
        }
    } catch (error) {
        alert('❌ Erreur: ' + error.message);
    }
}

function copyAddress(address) {
    navigator.clipboard.writeText(address).then(() => {
        alert('✅ Adresse copiée: ' + address);
    }).catch(err => {
        alert('❌ Erreur de copie: ' + err);
    });
}

function updateSignalConfig() {
    const minWhales = document.getElementById('min-whales-slider').value;
    const minSources = document.getElementById('min-sources-slider').value;

    document.getElementById('min-whales-value').textContent = minWhales;
    document.getElementById('min-sources-value').textContent = minSources;

    // Re-render signals with new filters
    if (window.allSignals) {
        renderFilteredSignals();
    }
}

async function saveSignalConfig() {
    const minWhales = parseInt(document.getElementById('min-whales-slider').value);
    const minSources = parseInt(document.getElementById('min-sources-slider').value);

    try {
        await fetch('/api/config/signals', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ min_whales: minWhales, min_sources: minSources })
        });
        alert('✅ Seuils sauvegardés ! Redémarrez le scanner pour appliquer.');
    } catch (error) {
        alert('❌ Erreur: ' + error.message);
    }
}

// Auto-refresh every 5 seconds
fetchData();
setInterval(fetchData, 5000);
