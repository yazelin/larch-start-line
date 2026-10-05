// 播放器能開、沒有「這個畫面壞掉了」
import { serve, open, assert } from './lib.mjs';
const s = await serve(process.argv[2] || 'dist/project.json');
const ui = await open(s.base);
try {
  const t = await ui.text();
  assert(!/這個畫面壞掉了|專案 JSON 有錯|無法開啟遊戲/.test(t), '播放器沒有壞掉：' + t.slice(0, 120));
  assert(ui.errors.length === 0, '沒有頁面例外 ' + ui.errors.join(';'));
} finally { await ui.close(); s.kill(); }
