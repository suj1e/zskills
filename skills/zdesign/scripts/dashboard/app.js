/* zdesign dashboard 前端逻辑 */
'use strict';

const GROUPS = [
  { key: 'page', label: '页面' },
  { key: 'component', label: '组件' },
  { key: 'icon', label: '图标' },
  { key: 'token', label: 'Tokens' },
  { key: 'other', label: '其他' },
];

const THEME_ICO = {
  light: '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
  dark: '<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4.5"/><line x1="12" y1="1.5" x2="12" y2="3.5"/><line x1="12" y1="20.5" x2="12" y2="22.5"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1.5" y1="12" x2="3.5" y2="12"/><line x1="20.5" y1="12" x2="22.5" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
};

const $ = (id) => document.getElementById(id);
const treeInner = $('treeInner');
const frame = $('frame');
const device = $('device');
const special = $('special');
const empty = $('empty');
const currentFile = $('currentFile');
const vpLabel = $('vpLabel');
const dot = $('dot');
const statusText = $('statusText');
const vpWidth = $('vpWidth');
const vpHeight = $('vpHeight');

let current = null;
let customMode = false;
let stopped = false;

/* ── 文件树 ── */
async function loadFiles() {
  let data;
  try {
    const r = await fetch('/__files', { cache: 'no-store' });
    data = await r.json();
  } catch (e) {
    treeInner.innerHTML = '<p class="muted pad">读取资产失败</p>';
    return;
  }
  let total = 0;
  for (const k of Object.keys(data)) total += data[k].length;
  $('meta').textContent = total + ' 个资产';
  treeInner.innerHTML = '';
  let any = false;
  for (const g of GROUPS) {
    const items = data[g.key] || [];
    if (!items.length) continue;
    any = true;
    const sec = document.createElement('div');
    sec.className = 'group';
    sec.innerHTML = '<div class="group-h">' + g.label + '<span class="count">' + items.length + '</span></div>';
    for (const it of items) {
      const el = document.createElement('div');
      el.className = 'file';
      el.dataset.path = it.path;
      el.innerHTML = '<span>' + it.name + '</span><span class="tag">' + (it.ext || '') + '</span>';
      el.addEventListener('click', () => selectFile(it.path, it.type));
      sec.appendChild(el);
    }
    treeInner.appendChild(sec);
  }
  if (!any) treeInner.innerHTML = '<p class="muted pad">空目录。把设计文件放进输出目录即可。</p>';
  highlight(current);
}
function highlight(p) {
  treeInner.querySelectorAll('.file').forEach((el) => el.classList.toggle('active', el.dataset.path === p));
}

/* ── 预览(按类型:page→iframe,icon→图标展示,token→色板)── */
function selectFile(p, type) {
  current = p;
  currentFile.textContent = p;
  empty.hidden = true;
  device.hidden = true;
  special.hidden = true;
  if (type === 'icon') showIcon(p);
  else if (type === 'token') showToken(p);
  else { device.hidden = false; frame.src = '/' + encodeURI(p); }
  highlight(p);
  closeTreeOnNarrow();
}
frame.addEventListener('load', () => {
  if (device.hidden) return;
  try {
    const loc = frame.contentWindow && frame.contentWindow.location;
    if (loc && loc.pathname) {
      let p = decodeURIComponent(loc.pathname).replace(/^\/+/, '');
      if (p && p !== current) { current = p; currentFile.textContent = p; highlight(p); }
    }
  } catch (e) {}
});

/* 图标专属预览 */
function showIcon(p) {
  special.hidden = false;
  const name = p.split('/').pop();
  special.innerHTML =
    '<div class="icon-preview"><div class="icon-canvas"><img id="iconImg" src="/' + encodeURI(p) + '" alt="" /></div>' +
    '<div class="icon-meta"><div class="icon-name">' + name + '</div><div class="muted small" id="iconDim">—</div></div></div>';
  const img = $('iconImg');
  img.onload = () => { $('iconDim').textContent = img.naturalWidth + ' × ' + img.naturalHeight + ' px'; };
  img.onerror = () => { $('iconDim').textContent = '该格式无法预览'; };
}

/* token 专属预览:解析 CSS 变量 → 配色色板 + 字体样例 + 其他 */
async function showToken(p) {
  special.hidden = false;
  special.innerHTML = '<p class="muted pad">解析中…</p>';
  let text;
  try {
    text = await (await fetch('/' + encodeURI(p), { cache: 'no-store' })).text();
  } catch (e) {
    special.innerHTML = '<p class="muted pad">读取失败</p>';
    return;
  }
  const vars = parseCssVars(text);
  if (!vars.length) {
    special.innerHTML = '<div class="icon-preview"><div class="icon-name">' + p.split('/').pop() + '</div><p class="muted small">未发现 CSS 变量(非 token 文件)</p></div>';
    return;
  }
  const colors = [], fonts = [], radii = [], spaces = [], others = [];
  for (const v of vars) {
    const n = v.name.toLowerCase();
    if (isColor(v.value)) colors.push(v);
    else if (/font|family|type/.test(n)) fonts.push(v);
    else if (/radius|round|corner/.test(n)) radii.push(v);
    else if (/space|gap|pad|margin|inset/.test(n)) spaces.push(v);
    else others.push(v);
  }
  special.innerHTML = renderToken(colors, fonts, radii, spaces, others);
}
function parseCssVars(text) {
  const out = [];
  const re = /(--[A-Za-z0-9_-]+)\s*:\s*([^;}\n]+)/g;
  let m;
  while ((m = re.exec(text))) {
    const val = m[2].trim();
    if (val) out.push({ name: m[1].trim(), value: val });
  }
  return out;
}
function isColor(v) {
  return /^(#([0-9a-fA-F]{3,8})\b|rgb|rgba|hsl|hsla|oklch|oklab|color\()/i.test(v.trim());
}
function renderToken(colors, fonts, radii, spaces, others) {
  let h = '';
  if (colors.length) {
    h += '<div class="tk-section"><div class="tk-h">配色 · ' + colors.length + '</div><div class="palette">';
    for (const c of colors) {
      h += '<div class="swatch"><div class="sw" style="background:' + c.value + '"></div><div class="sw-name">' + c.name + '</div><div class="sw-val muted small">' + c.value + '</div></div>';
    }
    h += '</div></div>';
  }
  if (fonts.length) {
    h += '<div class="tk-section"><div class="tk-h">字体 · ' + fonts.length + '</div><div class="palette">';
    for (const f of fonts) {
      const fam = f.value.split(',')[0].replace(/['"]/g, '');
      h += '<div class="swatch"><div class="fw-sample" style="font-family:' + f.value + '">Aa</div><div class="sw-name">' + f.name + '</div><div class="sw-val muted small">' + fam + '</div></div>';
    }
    h += '</div></div>';
  }
  const rest = [].concat(radii, spaces, others);
  if (rest.length) {
    h += '<div class="tk-section"><div class="tk-h">其他 · ' + rest.length + '</div><div class="kv">';
    for (const r of rest) h += '<div class="kv-row"><span class="sw-name">' + r.name + '</span><span class="muted">' + r.value + '</span></div>';
    h += '</div></div>';
  }
  return h || '<p class="muted pad">无</p>';
}

/* ── 视口:0=桌面占满,768/375=预设,custom=自定义档位 ── */
function setViewport(mode, opts) {
  opts = opts || {};
  if (mode === 0) {
    device.style.maxWidth = 'none';
    device.style.height = '';
    vpLabel.textContent = '桌面';
    customMode = false;
    markActive(0);
    return;
  }
  if (mode === 'custom') {
    customMode = true;
    const w = opts.width, h = opts.height;
    device.style.maxWidth = w + 'px';
    if (h && h >= 400) { device.style.height = h + 'px'; vpLabel.textContent = w + ' × ' + h; }
    else { device.style.height = ''; vpLabel.textContent = w + 'px'; }
    markActive('custom');
    return;
  }
  device.style.maxWidth = mode + 'px';
  device.style.height = '';
  vpLabel.textContent = mode + 'px';
  customMode = false;
  markActive(mode);
}
function markActive(v) {
  document.querySelectorAll('.vp-seg .vp-btn').forEach((b) => b.classList.toggle('active', b.dataset.vw === String(v)));
}
document.querySelectorAll('.vp-seg .vp-btn').forEach((b) =>
  b.addEventListener('click', () => {
    const bw = b.dataset.vw;
    if (bw === 'custom') setViewport('custom', { width: Number(vpWidth.value) || 1024, height: Number(vpHeight.value) || 768 });
    else setViewport(Number(bw));
  })
);
function onCustomInput() {
  if (!customMode) return;
  const w = Number(vpWidth.value), h = Number(vpHeight.value);
  if (!w || w < 280) return;
  setViewport('custom', { width: Math.min(3000, Math.round(w)), height: h });
}
vpWidth.addEventListener('input', onCustomInput);
vpHeight.addEventListener('input', onCustomInput);

/* ── 主题 ── */
function currentTheme() { return document.documentElement.getAttribute('data-theme') || 'light'; }
function applyTheme(t) {
  document.documentElement.setAttribute('data-theme', t);
  $('themeIco').innerHTML = THEME_ICO[t];
  try { localStorage.setItem('zdesign-theme', t); } catch (e) {}
}
$('themeBtn').addEventListener('click', () => applyTheme(currentTheme() === 'dark' ? 'light' : 'dark'));
applyTheme(currentTheme());

/* ── SSE ── */
function connect() {
  const es = new EventSource('/__reload');
  es.addEventListener('reload', () => { try { if (!device.hidden) frame.contentWindow && frame.contentWindow.location.reload(); } catch (e) {} });
  es.addEventListener('files', () => { loadFiles(); });
  es.onopen = () => { dot.className = 'dot live'; statusText.textContent = '实时'; };
  es.onerror = () => { dot.className = 'dot lost'; es.close(); if (stopped) { statusText.textContent = '已停止'; return; } statusText.textContent = '已断开'; setTimeout(connect, 1500); };
}

/* ── 侧栏折叠 ── */
$('treeToggle').addEventListener('click', () => {
  document.body.dataset.tree = document.body.dataset.tree === 'open' ? 'closed' : 'open';
});
$('scrim').addEventListener('click', () => { document.body.dataset.tree = 'closed'; });
function closeTreeOnNarrow() { if (window.matchMedia('(max-width: 760px)').matches) document.body.dataset.tree = 'closed'; }

/* ── 停止服务 ── */
$('stopBtn').addEventListener('click', async () => {
  if (!confirm('停止预览服务?停止后需重新启动才能继续预览。')) return;
  stopped = true;
  try { await fetch('/__stop', { method: 'POST', headers: { 'x-stop-token': window.__ZD_STOP || '' } }); } catch (e) {}
  showStopped();
});
function showStopped() {
  dot.className = 'dot lost';
  statusText.textContent = '已停止';
  const ov = document.createElement('div');
  ov.className = 'stopped-overlay';
  ov.innerHTML = '<div class="stopped-card"><div class="empty-logo">z</div><p>预览服务已停止</p><p class="muted small">关闭此页,或在终端重新启动 node scripts/preview-server.js</p></div>';
  document.body.appendChild(ov);
}

/* ── 启动 ── */
setViewport(0);
loadFiles();
connect();
