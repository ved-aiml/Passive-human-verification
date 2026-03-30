/**
 * PassiveGuard SDK — Demo Page UI Logic
 * app.js
 *
 * This file powers the demo page only.
 * The actual SDK is tracker.js — that's the embeddable script.
 */

// ── Floating Particles ────────────────────────────────────
console.log("app.js loaded");
(function spawnParticles() {
    const container = document.getElementById('particles');
    if (!container) return;
    for (let i = 0; i < 18; i++) {
        const p = document.createElement('div');
        p.className = 'particle';
        p.style.left = Math.random() * 100 + 'vw';
        p.style.width = p.style.height = (Math.random() * 2 + 1) + 'px';
        const dur   = (Math.random() * 18 + 12) + 's';
        const delay = (Math.random() * 15) + 's';
        p.style.animation = `particleFloat ${dur} ${delay} linear infinite`;
        container.appendChild(p);
    }
})();

// ── Behavior Signal Indicators ──────────────────────────────
let dataScore = 0;
const signals = { mouse: false, type: false, click: false, scroll: false };

function activateSignal(id, monId) {
    if (signals[id]) return;
    signals[id] = true;
    const el = document.getElementById(monId);
    if (!el) return;
    el.classList.add('active');
    el.querySelector('.monitor-icon').classList.add('active');
    updateScore();
}

function updateScore() {
    let s = 0;
    if (signals.mouse)  s += 30;
    if (signals.type)   s += 30;
    if (signals.click)  s += 20;
    if (signals.scroll) s += 20;
    // small natural jitter
    s = Math.min(s + Math.floor(Math.random() * 5), 100);
    dataScore = s;
    const bar = document.getElementById('scoreBar');
    const val = document.getElementById('scoreVal');
    if (bar) bar.style.width = s + '%';
    if (val) val.textContent = s + '%';
}

document.addEventListener('mousemove', () => activateSignal('mouse',  'monMouse'));
document.addEventListener('keydown',   () => activateSignal('type',   'monType'));
document.addEventListener('click',     () => activateSignal('click',  'monClick'));
document.addEventListener('scroll',    () => activateSignal('scroll', 'monScroll'));

// Tick score slightly over time to feel alive
setInterval(() => { if (dataScore > 0 && dataScore < 99) updateScore(); }, 3000);

// ── Login Handler ───────────────────────────────────────────
async function handleLogin() {
    const btn = document.getElementById('loginBtn');
    btn.classList.add('loading');

    try {
        const features = calculateFeatures(); // from tracker.js
        const response  = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(features)
        });
        const result = await response.json();
        console.log('Features sent:', features);
        console.log('Prediction:', result);
        showResult(result, features);
        // Reset tracker data so the next attempt uses fresh behaviour
        if (typeof resetTracking === 'function') resetTracking();
    } catch (err) {
        console.error('API error:', err);
        showResult({ prediction: -1, result: 'error' }, {});
    } finally {
        btn.classList.remove('loading');
    }
}

// ── Result Overlay ──────────────────────────────────────────
function showResult(result, features) {
    const isHuman = result.confidence > 0.6;
    const isSuspicious = result.confidence >= 0.3 && result.confidence <= 0.6;
    const isBot = result.confidence < 0.3;
    const isError = result.prediction === -1;

    const overlay   = document.getElementById('resultOverlay');
    const iconWrap  = document.getElementById('resultIcon');
    const iconSvg   = document.getElementById('resultIconSvg');
    const statusEl  = document.getElementById('resultStatus');
    const messageEl = document.getElementById('resultMessage');
    const metricsEl = document.getElementById('resultMetrics');

    overlay.classList.remove('human', 'suspicious', 'bot');
    iconWrap.classList.remove('human', 'suspicious', 'bot');
    statusEl.classList.remove('human', 'suspicious', 'bot');

    if (isError) {
        overlay.classList.add('bot');
        iconWrap.classList.add('bot');
        iconSvg.innerHTML = '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>';
        statusEl.classList.add('bot');
        statusEl.textContent = 'Connection Error';
        messageEl.textContent = 'Could not reach the verification server. Ensure the FastAPI backend is running on port 8000.';
        metricsEl.innerHTML = '';
    } else if (isHuman) {
        overlay.classList.add('human');
        iconWrap.classList.add('human');
        iconSvg.innerHTML = '<polyline points="20 6 9 17 4 12"/>';
        statusEl.classList.add('human');
        statusEl.textContent = '✓ Human Verified';
        messageEl.textContent = 'Your behavioral patterns match human interaction. Access granted — no CAPTCHA required.';
    } 
    else if(isSuspicious){
        overlay.classList.add('suspicious');
        iconWrap.classList.add('suspicious');
        iconSvg.innerHTML = '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>';
        statusEl.classList.add('suspicious');
        statusEl.textContent = '⚠ Suspicious';
        messageEl.textContent = 'Suspicious behavioral patterns detected. Your interaction did not match typical human behavior profiles.';
    }
    else {
        overlay.classList.add('bot');
        iconWrap.classList.add('bot');
        iconSvg.innerHTML = '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>';
        statusEl.classList.add('bot');
        statusEl.textContent = '⚠ Bot Detected';
        messageEl.textContent = 'Suspicious behavioral patterns detected. Your interaction did not match typical human behavior profiles.';
    }

    if (!isError && features) {
        const speed     = (features.avg_mouse_speed   || 0).toFixed(2);
        const typing    = (features.typing_avg_delay  || 0).toFixed(2);
        const curvature = (features.curvature_score   || 0).toFixed(2);
        metricsEl.innerHTML = `
            <div class="result-metric">
                <div class="result-metric-val">${speed}</div>
                <div class="result-metric-label">Mouse Speed</div>
            </div>
            <div class="result-metric">
                <div class="result-metric-val">${typing}s</div>
                <div class="result-metric-label">Typing Delay</div>
            </div>
            <div class="result-metric">
                <div class="result-metric-val">${curvature}</div>
                <div class="result-metric-label">Curvature</div>
            </div>`;
    }

    overlay.classList.add('show');
}

function resetOverlay() {
    document.getElementById('resultOverlay').classList.remove('show');
}
