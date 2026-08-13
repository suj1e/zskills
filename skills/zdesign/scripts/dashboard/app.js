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
const empty = $('empty');
const currentFile = $('currentFile');
const vpLabel = $('vpLabel');
const dot = $('dot');
const statusText = $('statusText');
const vpWidth = $('vpWidth');
const vpHeight = $('vpHeight');

let current = null;
let customMode = false;

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
      el.addEventListener('click', () => selectFile(it.path));
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

/* ── 预览 ── */
function selectFile(p) {
  current = p;
  currentFile.textContent = p;
  empty.hidden = true;
  device.hidden = false;
  frame.src = '/' + encodeURI(p);
  highlight(p);
  closeTreeOnNarrow();
}
frame.addEventListener('load', () => {
  try {
    const loc = frame.contentWindow && frame.contentWindow.location;
    if (loc && loc.pathname) {
      let p = decodeURIComponent(loc.pathname).replace(/^\/+/, '');
      if (p && p !== current) { current = p; currentFile.textContent = p; highlight(p); }
    }
  } catch (e) {}
});

/* ── 视口:0=桌面占满,768/375=预设,custom=自定义档位(选中后宽高实时驱动)── */
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
  // 数字预设
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
// 自定义档位下,改宽高实时生效;其他档位下输入不驱动
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
  es.addEventListener('reload', () => { try { frame.contentWindow && frame.contentWindow.location.reload(); } catch (e) {} });
  es.addEventListener('files', () => { loadFiles(); });
  es.onopen = () => { dot.className = 'dot live'; statusText.textContent = '实时'; };
  es.onerror = () => { dot.className = 'dot lost'; statusText.textContent = '已断开'; es.close(); setTimeout(connect, 1500); };
}

/* ── 侧栏折叠 ── */
$('treeToggle').addEventListener('click', () => {
  document.body.dataset.tree = document.body.dataset.tree === 'open' ? 'closed' : 'open';
});
$('scrim').addEventListener('click', () => { document.body.dataset.tree = 'closed'; });
function closeTreeOnNarrow() { if (window.matchMedia('(max-width: 760px)').matches) document.body.dataset.tree = 'closed'; }

/* ── 启动 ── */
setViewport(0);
loadFiles();
connect();
