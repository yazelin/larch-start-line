// 線上預覽：打開一張插件卡，確認卡片真的有執行（看得到 #msg 文字）。node tests/online_card.mjs <預覽網址>
import { open, sleep } from './lib.mjs';
const ui = await open(process.argv[2].replace(/\/$/, '').replace(/\/?$/, ''));
try {
  await sleep(6000);
  for (let i = 0; i < 6; i++) {
    const f = await ui.frameWith('#msg');
    if (f) { console.log('卡片在跑，#msg =', await f.locator('#msg').innerText()); break; }
    console.log('畫面：', (await ui.text()).slice(0, 300)); await ui.clickText('開始', 3000).catch(() => {}); await sleep(3000);
  }
  await ui.page.screenshot({ path: 'dist/shots/online-start.png' });
} finally { await ui.close(); }
