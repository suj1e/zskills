#!/usr/bin/env node
'use strict';
/**
 * zdesign · 设计资产 dashboard 服务器(零依赖,纯 Node 内置模块)
 *
 * 职责:
 *   1. 扫描 --dir 下设计资产 → GET /__files 返回分组清单 JSON
 *   2. GET /            → dashboard 前端(本文件同目录 dashboard/index.html)
 *   3. GET /__app/<f>   → dashboard 静态资源(style.css / app.js)
 *   4. GET /__reload    → SSE:文件变更推 `reload`(刷新当前预览)+ `files`(刷新文件树)
 *   5. GET /<file>      → serve --dir 下文件;HTML 注入 reload + 防跳出脚本
 *
 * 用法: node preview-server.js --dir ./out --port 4173 --open
 * 平台:fs.watch recursive 在 macOS/Windows 原生支持;Linux 不支持时静默降级(仅静态)。
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const args = parseArgs(process.argv.slice(2));
const ROOT = path.resolve(args.dir || './out');
const PORT0 = parseInt(args.port || '4173', 10);
const OPEN = !!args.open;
const APP_DIR = path.join(__dirname, 'dashboard');
if (!fs.existsSync(ROOT)) fs.mkdirSync(ROOT, { recursive: true });

const MIME = {
  '.html': 'text/html; charset=utf-8', '.htm': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8', '.mjs': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
  '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf',
  '.map': 'application/json; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
};

// 注入到被预览的 HTML:① SSE reload 监听 ② 防 iframe 跳出(把 target=_top/_blank 改成 _self)
const INJECT = `<script>(function(){
  try{var es=new EventSource('/__reload');es.addEventListener('reload',function(){location.reload();});es.onerror=function(){es.close();};}catch(e){}
  document.addEventListener('click',function(e){var t=e.target;if(t&&t.closest){var a=t.closest('a[target]');if(a&&a.target!=='_self'){a.target='_self';}}},true);
})();</script>`;

function parseArgs(a) {
  const o = {};
  for (let i = 0; i < a.length; i++) {
    if (a[i].indexOf('--') === 0) {
      const n = a[i + 1];
      o[a[i].slice(2)] = n && n.indexOf('--') !== 0 ? a[++i] : true;
    }
  }
  return o;
}

// 资产分类
const PAGE_EXTS = ['.html', '.htm'];
const ICON_EXTS = ['.svg', '.png', '.ico', '.jpg', '.jpeg', '.gif', '.webp'];
const TOKEN_RE = /token|theme|design|color|palette|typograph/i;

function categorize(rel, ext) {
  if (rel.indexOf('components/') === 0) return 'component';
  if (rel.indexOf('icons/') === 0 || ICON_EXTS.indexOf(ext) >= 0) return 'icon';
  if (PAGE_EXTS.indexOf(ext) >= 0) return 'page';
  if (ext === '.css' || ext === '.json') return TOKEN_RE.test(rel) ? 'token' : 'other';
  return 'other';
}

const GROUPS = [
  { key: 'page', label: '页面' },
  { key: 'component', label: '组件' },
  { key: 'icon', label: '图标' },
  { key: 'token', label: 'Tokens' },
  { key: 'other', label: '其他' },
];

function scanAssets() {
  const out = { page: [], component: [], icon: [], token: [], other: [] };
  function walk(dir, rel) {
    let ents;
    try { ents = fs.readdirSync(dir, { withFileTypes: true }); } catch (e) { return; }
    for (const ent of ents) {
      if (ent.name.charAt(0) === '.') continue;
      const r = rel ? rel + '/' + ent.name : ent.name;
      if (ent.isDirectory()) { walk(path.join(dir, ent.name), r); continue; }
      const ext = path.extname(ent.name).toLowerCase();
      out[categorize(r, ext)].push({ path: r, name: ent.name, ext, type: categorize(r, ext) });
    }
  }
  walk(ROOT, '');
  return out;
}

const clients = new Set();
function broadcast(ev, data) {
  const payload = 'event: ' + ev + '\ndata: ' + JSON.stringify(data == null ? '' : data) + '\n\n';
  for (const c of clients) c.write(payload);
}

function serveFile(filePath, res, injectHtml) {
  fs.readFile(filePath, (err, data) => {
    if (err) { res.writeHead(404); return res.end('Not found'); }
    const ext = path.extname(filePath).toLowerCase();
    const ct = MIME[ext] || 'application/octet-stream';
    let body = data;
    if (injectHtml && ext === '.html') {
      const s = data.toString('utf8');
      body = Buffer.from(s.indexOf('</body>') >= 0 ? s.replace('</body>', INJECT + '</body>') : s + INJECT);
    }
    res.writeHead(200, { 'Content-Type': ct, 'Cache-Control': 'no-cache' });
    res.end(body);
  });
}

function handler(req, res) {
  const url = req.url.split('?')[0];

  if (url === '/__reload') {
    res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
    res.write(': connected\n\n');
    clients.add(res);
    req.on('close', () => clients.delete(res));
    return;
  }
  if (url === '/__files') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-cache' });
    return res.end(JSON.stringify(scanAssets()));
  }
  // dashboard 前端(只有根路径 / 是入口;/index.html 等都归资产路由,避免和用户 ROOT 的 index.html 冲突)
  if (url === '/') return serveFile(path.join(APP_DIR, 'index.html'), res, false);
  if (url.indexOf('/__app/') === 0) {
    const fp = path.join(APP_DIR, url.slice(7));
    if (fp !== APP_DIR && fp.indexOf(APP_DIR + path.sep) !== 0) { res.writeHead(403); return res.end('Forbidden'); }
    return serveFile(fp, res, false);
  }
  // 资产文件(serve ROOT,HTML 注入)
  let urlPath = decodeURIComponent(url);
  if (urlPath === '/') urlPath = '/index.html';
  const fp = path.join(ROOT, urlPath);
  if (fp !== ROOT && fp.indexOf(ROOT + path.sep) !== 0) { res.writeHead(403); return res.end('Forbidden'); }
  return serveFile(fp, res, true);
}

function start(port) {
  const server = http.createServer(handler);
  server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') { console.log('[zdesign] port ' + port + ' busy, trying ' + (port + 1)); start(port + 1); }
    else throw err;
  });
  server.listen(port, () => {
    const u = 'http://localhost:' + port;
    console.log('[zdesign] dashboard → ' + u);
    console.log('[zdesign] assets    → ' + ROOT);
    if (OPEN) exec(process.platform === 'darwin' ? 'open ' + u : 'xdg-open ' + u + ' 2>/dev/null');
  });
}

let debounce;
try {
  fs.watch(ROOT, { recursive: true }, () => {
    clearTimeout(debounce);
    debounce = setTimeout(() => {
      broadcast('reload');
      broadcast('files');
      console.log('[zdesign] change → reload + refresh tree (' + clients.size + ' client' + (clients.size === 1 ? '' : 's') + ')');
    }, 150);
  });
} catch (e) {
  console.log('[zdesign] watch unavailable on this platform — static only.');
}

start(PORT0);
