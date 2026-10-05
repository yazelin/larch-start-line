// 播放器能開、沒有「這個畫面壞掉了」
import { serve, open, assert } from './lib.mjs';
const s = await serve(process.argv[2] || 'dist/project.json');
const ui = await open(s.base);
try {
  const t = await ui.text();
  assert(!/這個畫面壞掉了|專案 JSON 有錯|無法開啟遊戲/.test(t), '播放器沒有壞掉：' + t.slice(0, 120));
  await ui.clickText('開始遊戲').catch(() => {});
  await ui.waitText(/在槍響之前/);
  assert(true, '序章第一句出現');
  for (let i = 0; i < 8 && !/去檢錄處拿號碼布/.test(await ui.text()); i++) { await ui.advance(); await new Promise(r => setTimeout(r, 1200)); }
  await ui.waitText(/去檢錄處拿號碼布/);
  assert(true, '進到田徑場，任務提示出現');
  await new Promise(r => setTimeout(r, 1500)); await ui.page.screenshot({ path: 'dist/shots/smoke-map.png' });
  assert(ui.errors.length === 0, '沒有頁面例外 ' + ui.errors.join(';'));
} finally { await ui.close(); s.kill(); }
