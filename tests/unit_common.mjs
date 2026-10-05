// common.js 單元測試（不開瀏覽器）：node tests/unit_common.mjs
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
const src = readFileSync('src/plugin/common.js', 'utf8');
function load() {
  const posts = [], listeners = {};
  const ctx = { posts, parent: { postMessage: m => posts.push(m) }, document: { getElementById: () => null },
    addEventListener: (t, f) => (listeners[t] = listeners[t] || []).push(f), JSON };
  vm.createContext(ctx); vm.runInContext(src + ';this.L=L;', ctx);
  ctx.fire = (t, e) => (listeners[t] || []).forEach(f => f(e));
  return ctx;
}
let bad = 0;
const t = (name, fn) => { try { fn(); console.log('ok  ', name); } catch (e) { bad++; console.log('FAIL', name, '-', e.message); } };
t('done 只送一次 larch:complete', () => {
  const c = load(); c.L.done(); c.L.done(); c.L.done();
  const n = c.posts.filter(m => m.type === 'larch:complete').length;
  if (n !== 1) throw new Error('送了 ' + n + ' 次');
});
t('焦點在按鈕上按 Enter，不攔截也不算一次「按」', () => {
  const c = load(); let pressed = 0, prevented = false; c.L.press(() => pressed++);
  const btn = { closest: s => /button/.test(s) ? btn : null };
  c.fire('keydown', { key: 'Enter', target: btn, preventDefault: () => { prevented = true; } });
  if (pressed || prevented) throw new Error(`pressed=${pressed} prevented=${prevented}`);
});
t('焦點不在按鈕上按空白鍵，算一次「按」', () => {
  const c = load(); let pressed = 0; c.L.press(() => pressed++);
  c.fire('keydown', { key: ' ', target: { closest: () => null }, preventDefault() {} });
  if (pressed !== 1) throw new Error('pressed=' + pressed);
});
process.exit(bad ? 1 : 0);
