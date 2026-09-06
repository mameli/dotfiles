#!/usr/bin/env node
/*
Capture still frames from the active TikTok video in the persistent Chrome CDP browser.

Usage:
  node /path/to/capture_tiktok_frames_cdp.js [--cdp-url URL] <url-fragment-or-video-id> <out-dir> <time=label> [<time=label>...]

Example:
  node scripts/capture_tiktok_frames_cdp.js 7381016307422186785 /tmp/tiktok_frames \
    2.0=best_restaurant 14.0=coffee 64.0=burger

Notes:
- Requires Chrome CDP at SKILLS_CDP_URL (default http://127.0.0.1:9222) and the TikTok page already loaded.
- Writes JPEG files to <out-dir>; analyze them with vision/OCR.
- This avoids returning giant base64 screenshots through browser_cdp/tool output.
*/
const fs = require('fs');
const path = require('path');

function parseArgs(argv, env = process.env) {
  const positional = [];
  let explicitUrl;
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--cdp-url') {
      if (explicitUrl !== undefined || !argv[i + 1] || argv[i + 1].startsWith('--')) {
        throw new Error('Supply --cdp-url once with an HTTP(S) CDP base URL.');
      }
      explicitUrl = argv[++i];
    } else if (argv[i].startsWith('--')) {
      throw new Error('Unknown option; supported option: --cdp-url URL.');
    } else positional.push(argv[i]);
  }
  const rawUrl = explicitUrl !== undefined ? explicitUrl : (env.SKILLS_CDP_URL || 'http://127.0.0.1:9222');
  let url;
  try { url = new URL(rawUrl); } catch {
    throw new Error('Invalid CDP URL; set SKILLS_CDP_URL or pass --cdp-url with an HTTP(S) base URL.');
  }
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash || /\s/.test(rawUrl)) {
    throw new Error('CDP URL must be HTTP(S), without credentials, whitespace, query or fragment.');
  }
  const [fragment, outDir, ...pairs] = positional;
  if (!fragment || !outDir || pairs.length === 0) {
    throw new Error('Usage: node capture_tiktok_frames_cdp.js [--cdp-url URL] <url-fragment-or-video-id> <out-dir> <time=label> [...]');
  }
  const captures = pairs.map(pair => {
    const match = /^(\d+(?:\.\d+)?)=(.+)$/.exec(pair);
    if (!match || !Number.isFinite(Number(match[1]))) throw new Error('Use finite nonnegative seconds and a label: 2.0=cover.');
    return [Number(match[1]), match[2]];
  });
  return { fragment, outDir, captures, cdpUrl: url.href.replace(/\/+$/, '') };
}

async function main(argv = process.argv.slice(2)) {
  const { fragment, outDir, captures, cdpUrl } = parseArgs(argv);
  if (typeof fetch !== 'function' || typeof WebSocket !== 'function') {
    throw new Error('Use Node.js 22+ with global fetch and WebSocket support.');
  }
  let targets;
  try {
    const response = await fetch(`${cdpUrl}/json/list`, { signal: AbortSignal.timeout(10000) });
    if (!response.ok) throw new Error('HTTP error');
    targets = await response.json();
    if (!Array.isArray(targets)) throw new Error('Invalid target list');
  } catch {
    throw new Error('Cannot read CDP targets; verify --cdp-url / SKILLS_CDP_URL and the existing browser readiness.');
  }
  fs.mkdirSync(outDir, { recursive: true });
  const target = targets.find(t => t.url && t.url.includes(fragment));
  if (!target) throw new Error(`TikTok target not found for fragment: ${fragment}`);

  const ws = new WebSocket(target.webSocketDebuggerUrl);
  let nextId = 1;
  const pending = new Map();
  ws.onmessage = ev => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      pending.get(msg.id)(msg);
      pending.delete(msg.id);
    }
  };
  await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });

  function send(method, params = {}) {
    const id = nextId++;
    ws.send(JSON.stringify({ id, method, params }));
    return new Promise(resolve => pending.set(id, resolve));
  }

  async function capture(timeSeconds, label) {
    const safeLabel = label.replace(/[^a-zA-Z0-9._-]+/g, '_').replace(/^_+|_+$/g, '') || `t${timeSeconds}`;
    const expression = `(() => new Promise(resolve => {
      const v = document.querySelector('video');
      if (!v) return resolve({ error: 'No <video> element found' });
      v.pause();
      const grab = () => {
        const c = document.createElement('canvas');
        c.width = v.videoWidth || 576;
        c.height = v.videoHeight || 1024;
        c.getContext('2d').drawImage(v, 0, 0, c.width, c.height);
        resolve({ t: v.currentTime, data: c.toDataURL('image/jpeg', 0.85) });
      };
      const done = () => { v.removeEventListener('seeked', done); setTimeout(grab, 450); };
      v.addEventListener('seeked', done);
      v.currentTime = ${Number(timeSeconds)};
      setTimeout(grab, 2200);
    }))()`;
    const res = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (res.error) throw new Error(JSON.stringify(res.error));
    const value = res.result?.result?.value;
    if (!value || value.error) throw new Error(value?.error || `No capture value for ${timeSeconds}`);
    const outPath = path.join(outDir, `tiktok_${safeLabel}.jpg`);
    fs.writeFileSync(outPath, Buffer.from(value.data.split(',')[1], 'base64'));
    console.log(`${outPath} t=${value.t}`);
  }

  for (const [time, label] of captures) {
    await capture(time, label);
  }
  ws.close();
}

module.exports = { parseArgs, main };
if (require.main === module) {
  main().catch(err => { console.error(err.message); process.exit(1); });
}
