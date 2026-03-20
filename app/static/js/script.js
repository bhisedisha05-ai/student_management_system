// ============================================
//  EduTrack — Main JavaScript
// ============================================

// ── Toast notification ──
function showToast(msg, type = 'success') {
    const box = document.getElementById('toastBox');
    const icon = document.getElementById('toastIcon');
    const msgEl = document.getElementById('toastMsg');
    if (!box) return;
    box.className = 'toast-box ' + type;
    icon.className = type === 'success' ? 'bi bi-check-circle-fill' : 'bi bi-exclamation-circle-fill';
    msgEl.textContent = msg;
    box.classList.add('show');
    setTimeout(() => box.classList.remove('show'), 3500);
}

// ── Sidebar toggle ──
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}

// ── Date in topbar ──
function setTopbarDate() {
    const el = document.getElementById('topbarDate');
    if (!el) return;
    const d = new Date();
    el.textContent = d.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
}

// ── Avatar color from name ──
function avatarColor(name) {
    const colors = ['#4f8ef7','#7c5af0','#2ed8a8','#f7a24f','#f75f5f','#54b8e4'];
    let h = 0;
    for (let i = 0; i < name.length; i++) h = name.charCodeAt(i) + ((h << 5) - h);
    return colors[Math.abs(h) % colors.length];
}

function avatarInitials(name) {
    return name.trim().split(' ').map(p => p[0]).slice(0, 2).join('').toUpperCase();
}

// ── Marks color class ──
function marksClass(m) {
    if (m >= 80) return 'marks-high';
    if (m >= 60) return 'marks-mid';
    if (m >= 40) return 'marks-low';
    return 'marks-fail';
}

function marksBarClass(m) {
    if (m >= 80) return 'bar-high';
    if (m >= 60) return 'bar-mid';
    if (m >= 40) return 'bar-low';
    return 'bar-fail';
}

function divClass(d) {
    const map = { 'A': 'div-a', 'B': 'div-b', 'C': 'div-c' };
    return map[d] || 'div-a';
}

// ── Fetch wrapper ──
async function api(url, opts = {}) {
    const res = await fetch(url, {
        headers: { 'Content-Type': 'application/json' },
        ...opts,
        body: opts.body ? JSON.stringify(opts.body) : undefined
    });
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'Request failed');
    }
    return res.json();
}

// ── Confirm delete helper ──
function confirmDelete(msg) {
    return confirm(msg || 'Are you sure you want to delete this?');
}

// ── Init ──
document.addEventListener('DOMContentLoaded', setTopbarDate);