const http = require('http');
const fs = require('fs');
const path = require('path');

const GATEWAY = process.env.JARVIS_GATEWAY_URL || 'http://127.0.0.1:18789';
const PORT = Number(process.env.JARVIS_PROXY_PORT || 18790);
const CONFIG_PATH = process.env.JARVIS_CONFIG_PATH || path.join(process.env.HOME || '/home/csmith', '.openclaw/private/jarvis-voice-config.json');

const server = http.createServer((req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, x-openclaw-agent-id, x-openclaw-session-key');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  if (req.method === 'GET' && req.url === '/jarvis-voice-config.json') {
    fs.readFile(CONFIG_PATH, (err, data) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Config file missing', details: err.message }));
        return;
      }
      res.writeHead(200, {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store',
      });
      res.end(data);
    });
    return;
  }

  const chunks = [];
  req.on('data', chunk => chunks.push(chunk));
  req.on('end', () => {
    const target = new URL(req.url, GATEWAY);
    const proxyReq = http.request(target, {
      method: req.method,
      headers: { ...req.headers, host: target.host },
    }, proxyRes => {
      res.writeHead(proxyRes.statusCode, proxyRes.headers);
      proxyRes.pipe(res);
    });
    proxyReq.on('error', e => {
      res.writeHead(502);
      res.end('Gateway error: ' + e.message);
    });
    if (chunks.length) proxyReq.write(Buffer.concat(chunks));
    proxyReq.end();
  });
});

server.listen(PORT, '0.0.0.0', () => console.log(`CORS proxy on :${PORT} → ${GATEWAY}`));
