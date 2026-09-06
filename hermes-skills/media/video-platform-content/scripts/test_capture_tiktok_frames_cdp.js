#!/usr/bin/env node
// Offline tests: import must not connect; fetch is always a local stub.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { parseArgs, main } = require('./capture_tiktok_frames_cdp.js');
const args = ['video-id', '/tmp/output with spaces', '2.0=cover'];
let checks = 0;
function check(fn) { fn(); checks++; }
check(() => assert.equal(parseArgs(args, {}).cdpUrl, 'http://127.0.0.1:9222'));
check(() => assert.equal(parseArgs(args, { SKILLS_CDP_URL: '' }).cdpUrl, 'http://127.0.0.1:9222'));
check(() => assert.equal(parseArgs(args, { SKILLS_CDP_URL: 'http://localhost:9444/proxy/' }).cdpUrl, 'http://localhost:9444/proxy'));
check(() => assert.equal(parseArgs(['--cdp-url', 'https://localhost:9555', ...args], { SKILLS_CDP_URL: 'invalid' }).cdpUrl, 'https://localhost:9555'));
check(() => assert.equal(parseArgs(args, {}).outDir, '/tmp/output with spaces'));
for (const value of ['invalid', 'file:///tmp/cdp', 'http://user:secret@localhost', 'http://localhost/?token=secret', 'http://localhost/#x', ' http://localhost']) {
  check(() => assert.throws(() => parseArgs(args, { SKILLS_CDP_URL: value }), /CDP URL/));
}
for (const bad of [['--cdp-url'], ['--cdp-url', '', ...args], ['--unknown', ...args], ['id', 'out', 'NaN=label'], ['id', 'out', '-1=label'], ['id', 'out', '1='], []]) {
  check(() => assert.throws(() => parseArgs(bad, {})));
}
(async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tiktok portability '));
  const saved = { fetch: global.fetch, WebSocket: global.WebSocket, env: process.env.SKILLS_CDP_URL };
  try {
    global.WebSocket = class { constructor() { throw new Error('Browser access forbidden in offline test'); } };
    const output = path.join(tmp, 'output with spaces');
    let calls = 0;
    let observed;
    global.fetch = async url => { calls++; observed = url; return { ok: true, json: async () => [] }; };
    process.env.SKILLS_CDP_URL = 'http://localhost:9444/proxy/';
    await assert.rejects(main(['id', output, '1=label']), /target not found/);
    check(() => assert.equal(observed, 'http://localhost:9444/proxy/json/list'));
    check(() => assert.ok(fs.statSync(output).isDirectory()));
    await assert.rejects(main(['--cdp-url', 'http://localhost:9555', 'id', output, '1=label']), /target not found/);
    check(() => assert.equal(observed, 'http://localhost:9555/json/list'));
    const before = calls;
    const invalidOutput = path.join(tmp, 'must not exist');
    await assert.rejects(main(['--cdp-url', 'file:///tmp/no', 'id', invalidOutput, '1=label']), /CDP URL/);
    check(() => assert.equal(calls, before));
    check(() => assert.equal(fs.existsSync(invalidOutput), false));
    console.log(`PASS ${checks} offline portability checks; no browser/network used`);
  } finally {
    global.fetch = saved.fetch;
    global.WebSocket = saved.WebSocket;
    if (saved.env === undefined) delete process.env.SKILLS_CDP_URL;
    else process.env.SKILLS_CDP_URL = saved.env;
    fs.rmSync(tmp, { recursive: true, force: true });
  }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
