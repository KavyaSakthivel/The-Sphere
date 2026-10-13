// A tiny static file server for dist/, using only Node's built-in modules (no dependencies to patch).
// Used by `npm start`. Hosts that simply publish the dist/ folder do not need it.
const http = require('http');
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, 'dist');
const port = process.env.PORT || 3000;
const types = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.xml': 'application/xml; charset=utf-8', '.txt': 'text/plain; charset=utf-8',
  '.svg': 'image/svg+xml', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
  '.ico': 'image/x-icon', '.mp4': 'video/mp4', '.webm': 'video/webm', '.woff': 'font/woff', '.woff2': 'font/woff2',
};

function send(res, status, body, headers = {}) {
  res.writeHead(status, { 'Content-Type': 'text/plain; charset=utf-8', 'X-Content-Type-Options': 'nosniff', ...headers });
  res.end(body);
}

const server = http.createServer((req, res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') return send(res, 405, 'Method not allowed', { Allow: 'GET, HEAD' });
  let pathname;
  try { pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname); } catch { return send(res, 400, 'Bad request'); }
  let file = path.join(root, path.normalize(pathname));
  if (file !== root && !file.startsWith(root + path.sep)) return send(res, 403, 'Forbidden');
  fs.stat(file, (err, stat) => {
    if (!err && stat.isDirectory()) { file = path.join(file, 'index.html'); return fs.stat(file, (e, s) => (e ? notFound(res) : serve(req, res, file, s))); }
    if (err) return notFound(res);
    serve(req, res, file, stat);
  });
});

function notFound(res) {
  const page = path.join(root, '404.html');
  if (fs.existsSync(page)) return res.writeHead(404, { 'Content-Type': types['.html'] }), fs.createReadStream(page).pipe(res);
  send(res, 404, 'Not found');
}

function serve(req, res, file, stat) {
  const ext = path.extname(file).toLowerCase();
  const headers = {
    'Content-Type': types[ext] || 'application/octet-stream',
    'Accept-Ranges': 'bytes',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Cache-Control': ext === '.html' ? 'no-cache' : 'public, max-age=86400',
  };
  let start = 0, end = stat.size - 1, status = 200;
  const range = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range || '');
  if (range && (range[1] || range[2])) {
    // Browsers ask for the films in pieces; honour that so playback and seeking work.
    start = range[1] ? Number(range[1]) : Math.max(stat.size - Number(range[2]), 0);
    end = range[1] && range[2] ? Math.min(Number(range[2]), stat.size - 1) : stat.size - 1;
    if (start > end || start >= stat.size) return send(res, 416, 'Range not satisfiable', { 'Content-Range': `bytes */${stat.size}` });
    status = 206;
    headers['Content-Range'] = `bytes ${start}-${end}/${stat.size}`;
  }
  headers['Content-Length'] = end - start + 1;
  res.writeHead(status, headers);
  if (req.method === 'HEAD') return res.end();
  fs.createReadStream(file, { start, end }).pipe(res);
}

server.listen(port, () => console.log(`The Sphere is running at http://localhost:${port}`));
