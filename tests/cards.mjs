// 逐張插件卡測試：node tests/cards.mjs [卡片 id ...]
// 每張卡由 `python3 src/plugin.py --test <id>` 產生只含「這張卡 → 結果卡」的測試專案；
// 結果卡把卡片寫回的變數印成「RESULT k=v ...」，從那行讀值。
import { execFileSync } from 'node:child_process';
import { serve, open, assert, sleep } from './lib.mjs';

async function card(id, play) {
  execFileSync('python3', ['src/plugin.py', '--test', id], { stdio: 'inherit' });
  const s = await serve(`dist/test-${id}.json`);
  const ui = await open(s.base);
  try {
    await ui.clickText('開始遊戲');
    await ui.waitText(/測試：/);
    await sleep(800); await ui.page.keyboard.press('Enter');
    const f = await waitFrame(ui, '#tap');
    await play(ui, f);
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
};
const expect = {
  'start-gun': v => { assert(v.fouls === '5', 'start-gun：fouls=5（' + v.fouls + '）'); assert(v.bpm === '150', 'start-gun：bpm=150'); assert(v.thought === '3', 'start-gun：thought=3'); },
};

const ids = process.argv.slice(2).length ? process.argv.slice(2) : Object.keys(CARDS);
for (const id of ids) { const { vals } = await card(id, CARDS[id]); expect[id](vals); }
