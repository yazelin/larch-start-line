import { open, sleep } from './lib.mjs';
const ui = await open(process.argv[2]); await sleep(4000);
await ui.page.screenshot({ path: 'dist/shots/title.png' }); await ui.close();
