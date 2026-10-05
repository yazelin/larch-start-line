// 全路徑：從標題玩到結局 B，再回販賣機玩到結局 A。node tests/play_all.mjs
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { serve, open, assert, sleep } from './lib.mjs';
import { waitMsg, tap, tapUntil } from './cards.mjs';

execFileSync('python3', ['src/build.py'], { stdio: 'ignore' });
const proj = JSON.parse(readFileSync('dist/project.json', 'utf8'));
const maps = Object.fromEntries(proj.boards[0].nodes.filter(n => n.data.pluginCardId === 'map').map(n => {
  const m = JSON.parse(n.data.pluginValues.map); const walls = new Set();
  m.layers.filter(l => l.collision).forEach(l => l.tiles.forEach((t, i) => t && walls.add(`${i % m.width},${Math.floor(i / m.width)}`)));
  return [m.name, { m, walls }];
}));
const T0 = Date.now();
const s = process.env.ONLINE ? { base: process.env.ONLINE, kill() {} } : await serve('dist/project.json');
const ui = await open(s.base);
console.log(process.env.ONLINE ? '對線上預覽跑' : '對本機跑');
const page = ui.page;
const shot = n => page.screenshot({ path: `dist/shots/${n}.png` });
const log = (...a) => console.log(`[${((Date.now() - T0) / 1000).toFixed(0)}s]`, ...a);

async function pos() {
  const t = await ui.text(); const m = t.match(/HP \d+ \/ \d+ · (\d+), (\d+)/);
  const name = Object.keys(maps).find(k => t.includes(k));
  return m ? { x: +m[1], y: +m[2], map: name } : null;
}
// 有對話就一直翻，直到畫面符合 re（或沒有對話可翻）
async function drainUntil(re, max = 60) {
  for (let i = 0; i < max; i++) {
    const t = await ui.text();
    if (re && re.test(t)) return t;
    await ui.advance(); await sleep(700);
  }
  throw new Error('翻不到 ' + re + '：' + (await ui.text()).slice(-300));
}
const DIR = { '1,0': 'ArrowRight', '-1,0': 'ArrowLeft', '0,1': 'ArrowDown', '0,-1': 'ArrowUp' };
async function step(key) { await page.keyboard.down(key); await sleep(90); await page.keyboard.up(key); await sleep(380); }
function bfs(mapName, from, to, avoid) {
  const { m, walls } = maps[mapName];
  const solid = new Set(m.events.filter(e => e.actor === 'npc' && e.solid).map(e => `${e.x},${e.y}`));
  const key = (x, y) => `${x},${y}`, prev = new Map([[key(from.x, from.y), null]]), q = [from];
  while (q.length) {
    const c = q.shift();
    if (c.x === to.x && c.y === to.y) break;
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const n = { x: c.x + dx, y: c.y + dy }, k = key(n.x, n.y);
      if (n.x < 0 || n.y < 0 || n.x >= m.width || n.y >= m.height || prev.has(k) || walls.has(k)) continue;
      if ((solid.has(k) || avoid.has(k)) && !(n.x === to.x && n.y === to.y)) continue;
      prev.set(k, c); q.push(n);
    }
  }
  if (!prev.has(key(to.x, to.y))) throw new Error(`算不出路 ${JSON.stringify(from)} → ${JSON.stringify(to)}`);
  const path = []; for (let c = to; c && !(c.x === from.x && c.y === from.y); c = prev.get(key(c.x, c.y))) path.unshift(c);
  return path;
}
// 走到 (x,y)。avoid：不想踩到的格子（觸碰事件）。到了就回傳；中途被對話打斷就交給 onInterrupt
async function goto(x, y, avoid = []) {
  const av = new Set(avoid.map(([a, b]) => `${a},${b}`));
  for (let tries = 0; tries < 200; tries++) {
    const p = await pos();
    if (!p) { if (await ui.frameWith('#tap') || await ui.frameWith('.vn2-box')) return null; throw new Error('讀不到座標：' + (await ui.text()).slice(-200)); }
    if (p.x === x && p.y === y) return p;
    const [n] = bfs(p.map, p, { x, y }, av);
    await step(DIR[`${n.x - p.x},${n.y - p.y}`]);
  }
  throw new Error(`走不到 ${x},${y}`);
}
async function face(dir) { await page.keyboard.down(dir); await sleep(40); await page.keyboard.up(dir); await sleep(200); }
async function interact(x, y, from, dirKey) { await goto(...from); await face(dirKey); await page.keyboard.press('Enter'); await sleep(800); }
async function cardFrame(sel = '#tap', ms = 20000) {
  const end = Date.now() + ms;
  while (Date.now() < end) { const f = await ui.frameWith(sel); if (f) return f; await sleep(250); }
  throw new Error('等不到插件卡 ' + sel);
}
async function hud() { const m = (await ui.text()).match(/♥ (\d+)/); return m ? +m[1] : null; }

try {
  await ui.clickText('開始遊戲');
  await drainUntil(/去檢錄處拿號碼布/);
  log('進到田徑場');
  const GAZE = [[13, 25], [14, 25], [15, 25]];

  // 沒拿號碼布先去起跑線
  await goto(24, 22, GAZE);
  await ui.waitText(/號碼布還沒拿/); await sleep(1500); await shot('00a-narrator'); await drainUntil(/去檢錄處拿號碼布/);
  assert(true, '沒拿號碼布去起跑線 → 被引導回檢錄');

  await interact(6, 25, [6, 26], 'ArrowUp');
  await ui.waitText(/號碼布跟別針/); await sleep(1500); await shot('00b-clerk'); await drainUntil(/到終點線那邊/);
  assert(true, '檢錄拿到號碼布');

  await goto(14, 25);
  await ui.waitText(/程徹第一次見到林向晚/); await sleep(1500); await shot('01-gaze'); await drainUntil(/到八百公尺起跑線/);
  assert(await hud() === 120, '四目相對後心跳 120');

  await goto(20, 23, GAZE); await sleep(800); await shot('01b-lines');
  await goto(24, 22, GAZE);
  let f = await cardFrame();
  await tapUntil(f, /各就位/); await tap(f); await sleep(300); await shot('02-start');
  await f.locator('#choices button', { hasText: '認識她' }).click();
  for (let i = 0; i < 2; i++) { await waitMsg(f, /預備/); await tap(f); await waitMsg(f, /偷跑/); await tapUntil(f, /預備/); }
  await waitMsg(f, /砰/, 6000); await tapUntil(f, /兩個心跳/); await tap(f);
  assert(true, '起跑卡：偷跑兩次後起跑');
  f = await cardFrame('#ring');
  await tapUntil(f, /節拍/); await tap(f); await sleep(8500); await shot('03-pace'); await waitMsg(f, /終點/, 60000); await tap(f);
  assert(true, '配速卡跑完');
  await drainUntil(/去體育館後門的販賣機/);
  assert(true, '回到地圖、看到小組第一、任務指向販賣機');

  await interact(32, 26, [32, 27], 'ArrowUp');
  await ui.waitText(/妳的十塊錢/); await sleep(1200); await shot('04-vending');
  f = null;
  for (let i = 0; i < 40 && !(f = await ui.frameWith('#send')); i++) { await ui.advance(); await sleep(700); }
  assert(!!f, '中章之後進到草稿卡');
  await shot('05-drafts');
  for (let i = 0; i < 4; i++) await f.locator('#send:not([disabled])').click({ timeout: 20000 });
  await drainUntil(/去看台後面/); await sleep(1500); await shot('06-round2');
  assert(true, '防波堤之後換成林向晚，任務：去看台後面');

  // 第二輪：被看到兩次
  for (let i = 0; i < 2; i++) {
    await goto(15 + i * 3, 5).catch(() => {});
    await ui.waitText(/差點被看到/); await drainUntil(/去看台後面/);
  }
  assert(true, '走出看台遮蔽被發現兩次，都被拉回');
  const SEEN = Array.from({ length: 28 }, (_, k) => [k + 6, 5]).filter(([x]) => x !== 10 && x !== 29);
  await goto(19, 1, SEEN); await goto(20, 1, SEEN);
  await ui.waitText(/拉筋/); await drainUntil(/看看秩序冊|問問他的隊友|自己走一趟/);
  assert(true, '在看台後面偷看他熱身');

  await goto(32, 26, SEEN); await ui.waitText(/三分鐘/); await drainUntil(/看看秩序冊/);
  await interact(32, 26, [32, 27], 'ArrowUp'); await ui.waitText(/還不知道他什麼時候會來/); await drainUntil(/看看秩序冊/);
  assert(true, '線索沒齊就去販賣機 → 被擋下');
  await interact(8, 27, [8, 28], 'ArrowUp'); await ui.waitText(/十五點四十分/); await drainUntil(/問問他的隊友/);
  await interact(10, 13, [10, 14], 'ArrowUp'); await ui.waitText(/阿徹喔/);
  f = null;
  for (let i = 0; i < 20 && !(f = await ui.frameWith('#hh')); i++) { await ui.advance(); await sleep(700); }
  assert(!!f, '三條線索齊了 → 筆記卡'); await shot('07-notebook'); await f.locator('#begin').click();
  await f.locator('#hh').fill('15'); await f.locator('#mm').fill('47'); await f.locator('#submit').click(); await waitMsg(f, /馬上去買水/);
  await f.locator('#mm').fill('44'); await f.locator('#submit').click(); await waitMsg(f, /算了你的時間/); await f.locator('#submit').click();
  for (const t of [4000, 9000, 16000]) { await sleep(t === 4000 ? 4000 : t === 9000 ? 5000 : 7000); await shot('07c-race-' + t); }
  await drainUntil(/去體育館後門的販賣機/);
  assert(await hud() === 140, '看完他比賽，心跳 140');

  // 結局 B，再回來選 A
  await interact(32, 26, [32, 27], 'ArrowUp');
  await drainUntil(/轉身離開/); await ui.clickText('轉身離開');
  await ui.waitText(/她沒有繞過去/); await drainUntil(/回到販賣機前/);
  assert(true, '結局 B 走完，出現「回到販賣機前」');
  await ui.clickText('回到販賣機前'); await sleep(800);
  await drainUntil(/去體育館後門的販賣機/);
  await interact(32, 26, [32, 27], 'ArrowUp');
  await drainUntil(/讓零錢掉下去/); await ui.clickText('讓零錢掉下去');
  f = await cardFrame('#machine'); await sleep(3500); await shot('08-coin');
  await tapUntil(f, /他快來了/); await tap(f);
  await f.waitForFunction(() => document.body.dataset.state === 'wait'); await tap(f); await waitMsg(f, /還在遠處/); await tap(f);
  await f.waitForFunction(() => document.body.dataset.state === 'window', null, { timeout: 15000 }); await tap(f);
  await ui.waitText(/那天我早就在看台後面/, 20000);
  assert(true, '零錢卡：太早一次，再成功');
  await drainUntil(/把備用鑰匙掛到門邊/); await sleep(1500); await shot('08b-kitchen-map');
  await interact(10, 6, [9, 6], 'ArrowRight');
  await ui.waitText(/多了一副鑰匙/); await drainUntil(/把自己的門，交給另一個人/); await drainUntil(/走到她身後/);
  assert(true, '廚房：把備用鑰匙掛到門邊，才能去她身後');
  await goto(6, 4);
  await ui.waitText(/幾年後的一個冬夜/); await sleep(1500); await shot('09-kitchen'); await drainUntil(/我們結婚吧/);
  assert(await hud() === 72, '廚房：心跳平穩 72');
  await drainUntil(/起跑總在開始前　完|開始遊戲/);
  assert(true, '結局 A 走到底');
  assert(ui.errors.length === 0, '全程沒有頁面例外 ' + ui.errors.join(';'));
  log('自動測試總時間', ((Date.now() - T0) / 1000).toFixed(0), '秒');
} catch (e) {
  await page.screenshot({ path: 'dist/shots/play_all-fail.png' });
  throw e;
} finally { await ui.close(); s.kill(); }
