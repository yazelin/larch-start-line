// 逐張插件卡測試：node tests/cards.mjs [卡片 id ...]
// 每張卡由 `python3 src/plugin.py --test <id>` 產生只含「這張卡 → 結果卡」的測試專案；
// 結果卡把卡片寫回的變數印成「RESULT k=v ...」，從那行讀值。
import { execFileSync } from 'node:child_process';
import { serve, open, assert, sleep } from './lib.mjs';

async function card(id, play) {
  execFileSync('python3', ['src/plugin.py', '--test', id.replace('-onbeat', '')], { stdio: 'inherit' });
  const s = await serve(`dist/test-${id.replace('-onbeat', '')}.json`);
  const ui = await open(s.base, { mobile: !!process.env.MOBILE });
  try {
    await ui.clickText('開始遊戲');
    await ui.waitText(/測試：/);
    let f = null;   // 開頭對話卡在打字時按 Enter 只會補完文字，所以一直翻到插件卡出現為止
    for (let i = 0; i < 20 && !(f = await ui.frameWith('#tap')); i++) { await sleep(700); await ui.advance(); }
    if (!f) f = await waitFrame(ui, '#tap');
    await play(ui, f);
    await ui.page.screenshot({ path: `dist/shots/card-${id}${process.env.MOBILE ? '-mobile' : ''}.png` }).catch(() => {});
    await ui.waitText(/RESULT/, 20000); await sleep(3500);
    const r = await ui.text();
    console.log('RESULT 畫面：', r.slice(r.indexOf('RESULT'), r.indexOf('RESULT') + 120));
    const vals = Object.fromEntries([...r.matchAll(/(\w+)=([^\s|]*)/g)].map(m => [m[1], m[2]]));
    assert(ui.errors.length === 0, `${id}：沒有頁面例外 ${ui.errors.join(';')}`);
    return { vals, ui };
  } finally { await ui.close(); s.kill(); }
}
async function waitFrame(ui, sel, ms = 15000) {
  const end = Date.now() + ms;
  while (Date.now() < end) { const f = await ui.frameWith(sel); if (f) return f; await sleep(200); }
  throw new Error('等不到卡片 ' + sel);
}
const msg = f => f.locator('#msg').innerText();
async function waitMsg(f, re, ms = 10000) {
  const end = Date.now() + ms;
  while (Date.now() < end) { const t = await msg(f).catch(() => ''); if (re.test(t)) return t; await sleep(100); }
  throw new Error('卡片等不到 ' + re + '，現在是：' + await msg(f).catch(() => '?'));
}
const tap = f => f.locator('#tap').dispatchEvent('pointerdown');
async function tapUntil(f, re, max = 30) { for (let i = 0; i < max; i++) { if (re.test(await msg(f))) return; await tap(f); await sleep(250); } throw new Error('點到底也沒看到 ' + re); }

export const CARDS = {
  'start-gun': async (ui, f) => {
    await tapUntil(f, /各就位/);
    await tap(f); await sleep(300);
    await f.locator('#choices button', { hasText: '我要贏' }).click();
    await waitMsg(f, /散了/);
    assert(await f.locator('#choices button').count() === 2, 'start-gun：選過的想法消失，剩兩個');
    await f.locator('#choices button', { hasText: '認識她' }).click();
    for (let i = 0; i < 5; i++) {
      await waitMsg(f, /預備/);
      await tap(f);
      await waitMsg(f, /偷跑/);
      await tapUntil(f, /預備/);
    }
    assert(true, 'start-gun：偷跑 5 次都能重來');
    await waitMsg(f, /砰/, 6000);
    await tapUntil(f, /兩個心跳/);
    await tap(f);
  },
  // 配速：完全不按也能結束
  'pace': async (ui, f) => {
    await tapUntil(f, /節拍/);
    await tap(f);
    await f.waitForFunction(() => document.getElementById('eyes').classList.contains('on'), null, { timeout: 30000 });
    await sleep(900); await ui.page.screenshot({ path: `dist/shots/card-pace-eyes${process.env.MOBILE ? '-mobile' : ''}.png` });
    const overlap = await f.evaluate(() => { const a = document.querySelector('#eyes img, #eyes p').getBoundingClientRect(), b = document.getElementById('track').getBoundingClientRect(); return a.bottom > b.top; });
    assert(!overlap, 'pace：眼神圖不蓋到節拍線');
    await waitMsg(f, /終點/, 60000);
    await tap(f);
  },
  // 配速：照節拍按（data-onbeat=1 時按），分數要比不按高
  'pace-onbeat': async (ui, f) => {
    await tapUntil(f, /節拍/);
    await tap(f);
    await f.evaluate(() => new Promise(done => {
      const tapEl = document.getElementById('tap'); let last = '0';
      const t = setInterval(() => {
        const ob = document.body.dataset.onbeat || '0';
        if (ob === '1' && last !== '1') tapEl.dispatchEvent(new Event('pointerdown'));
        if (document.body.dataset.phase === 'sprint') tapEl.dispatchEvent(new Event('pointerdown'));
        last = ob;
        if (document.body.dataset.phase === 'end') { clearInterval(t); done(); }
      }, 20);
    }));
    await waitMsg(f, /終點/);
    await tap(f);
  },
  'notebook': async (ui, f) => {
    assert(await f.locator('#clues li').count() === 3, 'notebook：三條線索都列出來');
    for (let i = 0; i < 5; i++) {
      await f.locator('#hh').fill('15'); await f.locator('#mm').fill(String(30 + i));
      await f.locator('#submit').click();
      await waitMsg(f, i === 0 ? /馬上去買水/ : /三分鐘/);
    }
    assert(await f.locator('#crossed li').count() === 5, 'notebook：答錯的時間都被畫掉');
    await f.locator('#hh').fill('15'); await f.locator('#mm').fill('44');
    await f.locator('#submit').click();
    await waitMsg(f, /算了你的時間/);
    await tap(f);
  },
  'drafts': async (ui, f) => {
    for (let i = 0; i < 4; i++) {
      if (i === 0) { await f.locator('#send:not([disabled])').waitFor({ timeout: 15000 }); await f.locator('#head').click(); await ui.page.keyboard.press('Space'); }   // 第一次用鍵盤
      else await f.locator('#send:not([disabled])').click({ timeout: 15000 });
      if (i < 3) { await f.waitForFunction(n => document.querySelectorAll('#sent .bubble').length === 0 && document.body.dataset.round === String(n), i + 1, { timeout: 15000 }); }
    }
    await f.waitForFunction(() => document.querySelectorAll('#sent .bubble').length === 1, null, { timeout: 15000 });
    assert(true, 'drafts：前三次都被刪掉，第四次送出');
  },
  'coin-drop': async (ui, f) => {
    await tapUntil(f, /他快來了|零錢/);
    const g = await f.locator('#guide').boundingBox(); const vw = await f.evaluate(() => innerWidth);
    assert(/讓零錢掉下去/.test(await f.locator('#guide').innerText()) && Math.abs(g.x + g.width / 2 - vw / 2) < vw * 0.05, 'coin-drop：操作說明在畫面正中間');
    await tap(f);
    await f.waitForFunction(() => document.body.dataset.state === 'window', null, { timeout: 15000 }); await sleep(800);
    await ui.page.screenshot({ path: 'dist/shots/card-coin-window.png' });
    await f.waitForFunction(() => document.body.dataset.state === 'late', null, { timeout: 15000 }); await tap(f); await waitMsg(f, /走到面前/); await tap(f);
    const until = st => f.waitForFunction(x => document.body.dataset.state === x, st, { timeout: 15000 });
    for (let i = 0; i < 5; i++) { await until('wait'); await tap(f); await waitMsg(f, /轉角還是空的/); await tap(f); }
    for (let i = 0; i < 5; i++) { await until('late'); await tap(f); await waitMsg(f, /走到面前/); await tap(f); }
    assert(true, 'coin-drop：太早、太晚各 5 次都能重來');
    await until('window'); await sleep(300);
    const inZone = await f.evaluate(() => { const m = document.getElementById('needle').getBoundingClientRect(), z = document.querySelector('#meter .ok').getBoundingClientRect(); const x = m.left + m.width / 2; return x >= z.left && x <= z.right; });
    assert(inZone, 'coin-drop：時機窗內指針在「剛好」那一段');
    assert(/portraits/.test(await f.locator('#him img').getAttribute('src')), 'coin-drop：走進來的是程徹的立繪');
    assert(/portraits/.test(await f.locator('#lin img').getAttribute('src')), 'coin-drop：販賣機旁站著林向晚的立繪');
    await sleep(1200);
    const vis = await f.evaluate(() => ['lin', 'him'].map(id => { const r = document.querySelector('#' + id + ' img').getBoundingClientRect(); return r.height > innerHeight * 0.45 && r.height < innerHeight && r.left < innerWidth - r.width * 0.4 && r.right > 0; }));   // 他至少四成身體入鏡
    assert(vis[0] && vis[1], 'coin-drop：兩人的立繪都看得見、大小正常（' + vis + '）');
    await tap(f);
    await f.waitForFunction(() => document.body.dataset.state === 'ok', null, { timeout: 5000 });
    assert(await f.locator('.coin.drop').count() === 3, 'coin-drop：三枚零錢掉下去');
    assert(/coin\.webp/.test(await f.evaluate(() => getComputedStyle(document.querySelector('.coin')).backgroundImage)), 'coin-drop：零錢用畫好的硬幣圖');
    await sleep(1600);
    const above = await f.evaluate(() => { const p = document.getElementById('panel').getBoundingClientRect(); return [...document.querySelectorAll('.coin')].every(c => c.getBoundingClientRect().bottom <= p.top); });
    assert(above, 'coin-drop：零錢落在對話框上方，看得到');
    const xs = await f.evaluate(() => [...document.querySelectorAll('.coin')].map(c => Math.round(c.getBoundingClientRect().left)));
    assert(Math.max(...xs) - Math.min(...xs) > 40, 'coin-drop：三枚零錢落點分開（' + xs + '）');
    await ui.page.screenshot({ path: `dist/shots/card-coin-ok${process.env.MOBILE ? '-mobile' : ''}.png` });
  },
};
const expect = {
  'start-gun': v => { assert(v.fouls === '5', 'start-gun：fouls=5（' + v.fouls + '）'); assert(v.bpm === '150', 'start-gun：bpm=150'); assert(v.thought === '3', 'start-gun：thought=3'); },
  'pace': v => { assert(v.pace_score === '0', 'pace：不按 → pace_score=0（' + v.pace_score + '）'); assert(v.bpm === '170', 'pace：bpm=170'); },
  'pace-onbeat': v => { assert(Number(v.pace_score) >= 10, 'pace-onbeat：照拍按分數 >= 10（' + v.pace_score + '）'); },
  'notebook': v => { assert(v.calc_ok === 'true', 'notebook：calc_ok=true'); assert(v.calc_tries === '6', 'notebook：calc_tries=6（' + v.calc_tries + '）'); },
  'drafts': v => { assert(v.drafted === 'true', 'drafts：drafted=true'); },
  'coin-drop': v => { assert(v.coin_ok === 'true', 'coin-drop：coin_ok=true'); assert(v.coin_tries === '12', 'coin-drop：coin_tries=12（' + v.coin_tries + '）'); },
};

export { waitMsg, tap, tapUntil };
if (process.argv[1].endsWith('cards.mjs')) {
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(CARDS);
  for (const id of ids) { const { vals } = await card(id, CARDS[id]); expect[id](vals); }
}
