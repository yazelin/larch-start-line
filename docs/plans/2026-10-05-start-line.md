# 《起跑總在開始前》實作計畫（一日版）

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 2026-10-05 當天做出可以從頭玩到兩個結局的 Larch RPG 作品，推上作者的 Larch 專案，由作者在網頁按發佈。

**Architecture:** 全部內容由本機 Python 腳本從原始檔產生一份專案 JSON：劇情文字（canon）→ 對話卡；地圖（Python 描述事件）→ RPG 地圖卡；插件（每張卡一份 HTML）→ 卡片節點的 `pluginHtml` 與 `settings.plugins`。本機用 larch-preview 播放與自動測試，最後整份推上 Larch。美術先用暫代圖，生成好再替換檔案，不改程式。

**Tech Stack:** Python 3（產生 JSON）、單檔 HTML＋原生 JS（插件卡，無外部依賴）、Node＋playwright-core（`~/larch-preview` 已裝）做自動測試、larch-preview 本機播放器、Larch MCP／REST（建專案、推專案、上傳素材）、codex imagegen（生圖）、cutout skill（去背）。

**Spec:** `docs/specs/2026-10-05-design.md`

## Global Constraints

- 原文不改字：遊戲內原文段落一律從 `canon/原文.md` 讀，不在程式裡手打。
- 新寫文字只在 `canon/新寫.md`，由作者定稿；作者未回覆前用草稿，標記 `（草稿）` 只在檔案裡，不進遊戲。
- 正體中文、全形標點、不用 emoji；寫任何新文字前先讀 `~/mori-universe/yaze-journal/blog-post-style.md`，寫完跑 speak-tw。
- 所有地圖 `combat:"none"`；不用 Kenney 素材；畫風柔和水彩。
- 每個事件都要有 `sprite`；`screen` 參數包在 `screen:{}`；`guidance` 用 `[]` 不用 null；平行事件改觸發條件的變數步驟放最後。
- 插件卡：`larch:set` 的每個名字都要在該卡 `pluginWriteVars`；一定送 `larch:complete`；手機觸控＋鍵盤都能玩；失敗可重來。
- 生圖只用本機 codex imagegen／Larch／.11 codex-image；產圖前先縮小再 commit。
- Larch 寫入：新專案用整份推送前先抓快照；不准用寫入型 API 探測；發佈由作者在網頁按。
- 時程：今天。順序固定為「能玩的暫代版 → 推上平台作者試玩 → 換美術」，任何一步卡超過 30 分鐘就回報作者決定砍或改。

## Review Focus

1. 小遊戲卡進行中存檔、讀檔：讀回後應回到卡片開頭或卡片前的地圖格，不該卡死 → Task 8 全路徑測試加一段「起跑卡中存檔→讀檔」。
2. 玩家在地圖上亂走（沒拿號碼布先去起跑線、沒蒐集線索先去販賣機）：應該被提示引導，不該觸發後段劇情 → Task 6、7 的事件條件與 Task 8 測試。
3. 手機直向：插件卡按鈕夠大、HUD 不擋住對話框 → Task 8 用 Playwright iPhone 視窗各截一張。
4. 偷跑或答錯連續很多次：每次都能重來，計數不溢出、不卡 → Task 4、5 卡片測試各重來 5 次。
5. 從結局 B 回到販賣機再選 A：變數 `ending` 要改成 A、零錢卡要能再玩 → Task 8 測試走 B→A。

---

## 檔案結構

```
larch-start-line/
  canon/原文.md            原文（已存在）
  canon/新寫.md            新寫文字（Task 2）
  src/text.py              讀 canon，切段，回傳各段文字
  src/cards.py             對話卡、場景卡節點
  src/mapkit.py            地圖事件與步驟的產生函式（A()、ev()、cond() 等）
  src/map_stadium.py       田徑場地圖（兩輪）
  src/map_kitchen.py       台北廚房地圖
  src/plugin/common.js     插件卡共用（ready/init/set/complete、按鍵與觸控）
  src/plugin/heart.html    心跳 HUD
  src/plugin/start-gun.html  起跑卡
  src/plugin/pace.html     配速卡
  src/plugin/notebook.html 筆記卡
  src/plugin/drafts.html   草稿卡
  src/plugin/coin-drop.html  零錢卡
  src/plugin.py            把 HTML 內嵌 common.js、產生插件節點與 settings.plugins
  src/build.py             組出 dist/project.json
  src/push.py              推到 Larch（快照→推→讀回比對）
  assets/                  圖（先放暫代圖，Task 11 換正式）
  tests/check_static.py    靜態檢查：變數閘門、事件格式、原文一致
  tests/cards.mjs          逐張插件卡自動測試
  tests/play_all.mjs       全路徑自動走一遍
  dist/                    產出（.gitignore）
```

---

### Task 1：專案骨架與 Larch 專案

**Files:**
- Create: `src/build.py`、`.gitignore`、`README.md`
- Create（下載）：`skeleton/project.json`

**Interfaces:**
- Produces: `build.load_skeleton() -> dict`（完整 Larch 專案 dict）；`build.main()` 寫 `dist/project.json`；`PROJECT_ID` 常數存在 `src/build.py`。

- [ ] **Step 1：在 Larch 建新專案**（MCP `larch_create_project`，名稱「起跑總在開始前」），記下專案 id。
- [ ] **Step 2：抓回骨架**：`python3 ~/larch-preview/serve.py --project <id>` 會存一份 JSON，複製成 `skeleton/project.json`，關掉那個 serve。
- [ ] **Step 3：在專案啟用 RPG 系統**：骨架的 `settings.plugins` 要有 `larch-rpg-system: {enabled:true, settings:{}}`；若沒有，照《雲之王國》範例補上。
- [ ] **Step 4：寫 `src/build.py`**

```python
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT_ID = '<Step 1 的 id>'

def load_skeleton():
    return json.loads((ROOT / 'skeleton/project.json').read_text())

def assemble():
    p = load_skeleton()
    p = p.get('project', p)
    board = p['boards'][0]
    board['nodes'], board['edges'] = [], []
    return p, board

def main():
    p, board = assemble()
    out = ROOT / 'dist/project.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(p, ensure_ascii=False))
    print('wrote', out, len(board['nodes']), 'nodes')

if __name__ == '__main__':
    main()
```

- [ ] **Step 5：跑 `python3 src/build.py`**，再用 `serve.py dist/project.json --port 0` 開，確認播放器不報錯（空專案也要能開）。
- [ ] **Step 6：commit**（`.gitignore` 放 `dist/`）。

### Task 2：新寫文字草稿

**Files:**
- Create: `canon/新寫.md`

- [ ] **Step 1：讀 `~/mori-universe/yaze-journal/blog-post-style.md` 與 `canon/原文.md`，對照原文語氣。**
- [ ] **Step 2：寫以下各段，每段用 `## 標題` 分開（`src/text.py` 靠標題取段）：**
  - `## 換人提示`（一行）
  - `## 結局B`（150～250 字，扣回「沒有人替你喊開始」，不說教）
  - `## 備用鑰匙說明`：「把自己的門，交給另一個人。」
  - `## 想法選項`：三行「我要贏／配速／等跑完，我要去認識她」，以及前兩項散掉時的旁白（用原文「腦袋裡沒有秒數、沒有配速」）
  - `## 草稿`：三則被刪掉的訊息與第四次送出的那句
  - `## 線索`：秩序冊公告、隊友台詞、她自己走一趟的旁白
  - `## 筆記提示`：答錯時的兩句提示
  - `## 零錢`：太早、太晚各一句
  - `## 路人`：裁判、檢錄、隊友各 1～2 句
- [ ] **Step 3：跑 speak-tw 檢查器**，修到零錯。
- [ ] **Step 4：commit，並把整份貼給作者審**（不等回覆，先往下做；作者改了再重產）。

### Task 3：文字切段與對話卡

**Files:**
- Create: `src/text.py`、`src/cards.py`、`tests/check_static.py`
- Modify: `src/build.py`

**Interfaces:**
- Produces: `text.para(start: str, end: str) -> list[str]`（回傳 `原文.md` 從含 `start` 的段落到含 `end` 的段落，含頭尾；找不到就 raise）；`text.new(section: str) -> str`（`新寫.md` 該標題下的內容）；`cards.scene(id, title, lines: list[str], bg='') -> node`；`cards.link(board, a, b)`。

- [ ] **Step 1：寫測試 `tests/check_static.py`**

```python
import sys; sys.path.insert(0, 'src')
import text
def test_para():
    ps = text.para('在槍響之前', '所謂的起跑')
    assert len(ps) == 2 and ps[0].startswith('在槍響之前')
def test_every_original_para_used_once():
    import build
    p = build.build()
    blob = json.dumps(p, ensure_ascii=False)
    for s in text.all_paras():
        assert s[:20] in blob, s[:20]
if __name__ == '__main__':
    import json
    for k, f in list(globals().items()):
        if k.startswith('test_'): f(); print('ok', k)
```

- [ ] **Step 2：跑，確認失敗**（`text` 不存在）。
- [ ] **Step 3：實作 `text.py`**：讀 `原文.md`，略過第一個標題與說明段（第一個 `## ` 之前或第一個空行前的說明），其餘以空行切段；`all_paras()` 回傳全部段落。
- [ ] **Step 4：實作 `cards.py`**：對話卡節點照 larch-vn skill 的格式（`{id, position, data:{type:'dialogue', title, text, dialogueLines:[{id,speaker,text}], background}}`），旁白 speaker 留空；`build.py` 改成 `build() -> dict` 回傳專案、`main()` 寫檔。
- [ ] **Step 5：先做序章卡與中章卡**（序章：`para('在槍響之前','所謂的起跑')`；中章前段：`para('後來他們真的在一起了','但林向晚後來告訴程徹')`；防波堤：`para('大三那年夏天','程徹愣住了')`＋`new('換人提示')`；防波堤後半：`para('那天我早就在看台後面','起跑總在開始前，如同')`；結局 B：`new('結局B')`）。`test_every_original_para_used_once` 這時還會失敗，到 Task 7 完成才全過。
- [ ] **Step 6：本機預覽看序章能播。commit。**

### Task 4：插件共用層、心跳 HUD、起跑卡

**Files:**
- Create: `src/plugin/common.js`、`src/plugin/heart.html`、`src/plugin/start-gun.html`、`src/plugin.py`、`tests/cards.mjs`
- Modify: `src/build.py`

**Interfaces:**
- Produces（common.js，全域）：`L.onInit(fn(values, vars, assets))`、`L.set(name, value)`、`L.done()`、`L.press(fn)`（空白鍵、Enter、點擊、觸控都觸發）。
- Produces（plugin.py）：`CARDS = {card_id: {'file', 'read': [...], 'write': [...], 'presentation'}}`；`plugin.card_node(card_id, node_id, values={}) -> node`；`plugin.settings_entry() -> dict`（給 `settings.plugins['start-line']`，含 `enabled:true` 與 `playback.huds`）。
- 起跑卡：read `bpm`、`fouls`；write `bpm`、`fouls`、`thought`。結束時 `bpm=150`。
- HUD：readVariables `['bpm']`，`bpm<=0` 時隱藏。

- [ ] **Step 1：寫 `tests/cards.mjs` 的框架與起跑卡測試**：用 larch-preview 開一份只有「起跑卡」的測試專案（`plugin.py --test start-gun` 產生 `dist/test-start-gun.json`），Playwright 操作：
  1. 選「我要贏」→ 應出現散掉的旁白，選項少一個；選第三項。
  2. 「預備」後立刻按空白鍵 → 頁面出現「偷跑」；重複 5 次。
  3. 不按，等到槍響 → 出現「早了整整兩個心跳」→ 按繼續 → 卡片 complete。
  4. 斷言專案變數 `fouls == 5`、`bpm == 150`（從播放器下一張測試對話卡的 `{{fouls}}` 文字讀出）。
- [ ] **Step 2：跑，確認失敗。**
- [ ] **Step 3：實作 `common.js`**

```js
var L = (function () {
  var initFns = [], vars = {};
  addEventListener('message', function (e) {
    var d = e.data; if (!d || d.type !== 'larch:init') return;
    vars = d.variables || {};
    initFns.forEach(function (f) { f(d.values || {}, vars, d.assets || []); });
  });
  parent.postMessage({ type: 'larch:ready' }, '*');
  return {
    onInit: function (f) { initFns.push(f); },
    set: function (n, v) { vars[n] = v; parent.postMessage({ type: 'larch:set', name: n, value: v }, '*'); },
    get: function (n, dflt) { return n in vars ? vars[n] : dflt; },
    done: function () { parent.postMessage({ type: 'larch:complete' }, '*'); },
    press: function (fn) {
      addEventListener('keydown', function (e) { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); fn(); } });
      addEventListener('pointerdown', function () { fn(); });
    }
  };
})();
```

- [ ] **Step 4：實作 `heart.html`**（照 spec §5.1；收 `larch:hud:init/update`，依 `bpm` 設 CSS 動畫週期 `60/bpm` 秒；`bpm<=0` 時 `body.hidden=true`）。
- [ ] **Step 5：實作 `start-gun.html`**：狀態機 `think → onyourmarks → set → (foul | gun) → done`。`set` 狀態每拍把 `bpm` 從 110 往上加 6，槍在 1500～3000ms 隨機時間響；`set` 狀態收到 `L.press` 就是偷跑（`fouls+1`，閃紅，「偷跑。回到起跑線。」，1.5 秒後回 `onyourmarks`）。文字從卡片欄位 `values` 傳入（`plugin.py` 把 `新寫.md` 的想法選項放進 values），原文句子也從 values 傳入。
- [ ] **Step 6：實作 `plugin.py`**：讀 HTML，把 `<script src="common.js"></script>` 換成內嵌內容；`card_node()` 產生節點（欄位照 §9 驗證過的格式：`type:'plugin'`、`pluginId:'start-line'`、`pluginCardId`、`pluginHtml`、`pluginPresentation`、`pluginReadVars`、`pluginWriteVars`、`pluginValues`、`pluginFrame:{showTitle:false, showButton:false}`）。
- [ ] **Step 7：在 `check_static.py` 加變數閘門檢查**：用正規式抓每份 HTML 裡 `L.set('名字'` 的名字，斷言都在該卡 `write` 名單；抓 `L.get('名字'` 斷言在 `read` 名單。
- [ ] **Step 8：跑 `check_static.py` 與 `cards.mjs start-gun`，全過。commit。**

### Task 5：配速卡、筆記卡、草稿卡、零錢卡

**Files:**
- Create: `src/plugin/pace.html`、`notebook.html`、`drafts.html`、`coin-drop.html`
- Modify: `src/plugin.py`（CARDS 加四張）、`tests/cards.mjs`

**Interfaces:**
- 配速卡：read `bpm`；write `bpm`、`pace_score`。
- 筆記卡：read `clue_order`、`clue_mate`、`clue_walk`；write `calc_ok`、`calc_tries`。正確答案從 values `answer` 傳入（`HH:MM`），三條線索文字也從 values 傳入。
- 草稿卡：write `drafted`（true）。三則草稿與最後一句從 values 傳入。
- 零錢卡：read `bpm`；write `coin_ok`、`coin_tries`、`bpm`。

- [ ] **Step 1：在 `cards.mjs` 寫四張卡的測試**
  - 配速：全部不按也能結束（complete），`pace_score` 有寫入；照節拍按，`pace_score` 較高。
  - 筆記：輸入錯的時間 5 次，每次出提示，`calc_tries==5`；輸入正確答案 → `calc_ok==true` → complete。
  - 草稿：按三次「送出」都被刪掉，第四次送出 → `drafted==true` → complete。
  - 零錢：在他出現前按 → 「太早」重來；等他走到面前才按 → 「太晚」重來；在時機窗內按 → `coin_ok==true` → complete。各重來 5 次不出錯。
- [ ] **Step 2：跑，確認失敗。**
- [ ] **Step 3：實作 `pace.html`**：約 25 秒。節拍點從右往左移，`L.press` 時與最近節拍的差 < 120ms 記一分；第 8 秒與第 16 秒浮出她的眼神圖（values `eyesUrl`，暫代時用文字），節拍間隔隨機亂 400ms 持續 3 秒；最後 5 秒變衝刺連打。結束顯示一句回饋（原文已定拿小組第一，這裡不寫名次），`bpm` 設 170。
- [ ] **Step 4：實作 `notebook.html`**：左頁列出已蒐集的線索（`clue_*` 為 true 的才顯示文字），右頁兩個上下撥的數字（時、分，分鐘以 1 為單位）＋「就這個時間」按鈕；錯了在筆記上畫掉該時間並顯示提示（第一次錯給提示一、之後給提示二）。
- [ ] **Step 5：實作 `drafts.html`**：手機畫面，輸入框自動打出第 n 則草稿（打字效果），「送出」鈕；按下後停 0.8 秒、文字逐字刪除；第四次打出最後一句，按送出變成已送出泡泡，1.2 秒後 complete。
- [ ] **Step 6：實作 `coin-drop.html`**：他從畫面右側轉角走進來（約 6 秒走到販賣機前），時機窗是他從轉角出現後 1.0～3.0 秒；`bpm` 隨他接近從 120 加到 160；成功時零錢落地滾向他、畫面停住、complete。
- [ ] **Step 7：跑 `check_static.py` 與 `cards.mjs` 全部，全過。commit。**

### Task 6：田徑場地圖：第一輪

**Files:**
- Create: `src/mapkit.py`、`src/map_stadium.py`、`assets/placeholder/stadium.png`
- Modify: `src/build.py`

**Interfaces:**
- Produces（mapkit）：`A(kind, **kw)`（自動編 id、補齊九欄）、`say(text, speaker='narrator')`、`setv(name, value)`、`cond(name, value, op='eq')`、`ev(id, x, y, **kw)`（補 sprite 等預設）、`INVISIBLE` sprite、`map_node(id, title, map_dict, start=False)`。
- Produces（map_stadium）：`build_stadium(board) -> map_node`；地點常數 `START_LINE=(x,y)`、`FINISH=(x,y)`、`TENT=(x,y)`、`VENDING=(x,y)`、`STANDS_BACK=(x,y)`、`BOARD=(x,y)`（秩序冊）。

- [ ] **Step 1：暫代底圖**：Python（PIL）畫 40×30 格、每格 32px 的平面圖：綠底、紅色跑道橢圓、白線、灰色看台、帳篷、販賣機方塊，並把同一份配置輸出成碰撞格（`#` 不能走）。這份配置就是之後生正式水彩底圖的構圖依據。
- [ ] **Step 2：在 `check_static.py` 加地圖檢查**：每個事件有 sprite；沒有兩個事件同格；所有事件格不在碰撞格；從主角起點用 BFS 走得到每個事件格（或其相鄰格）；`guidance` 每條的 `eventId` 存在。
- [ ] **Step 3：跑，確認失敗。**
- [ ] **Step 4：實作第一輪事件**（條件都帶 `round=1`）：
  - `hero`（起點在檢錄處附近）、`judge`、`tent`（拿號碼布、別針，`phase=bib→start`）、`gaze`（終點線後方 touch，`phase=start` 時：心跳 120、CG 對話卡、原文第 3 段與「沒有任何對白。」）、`startline`（`phase=start` 且有號碼布：`jump` 起跑卡；沒號碼布：「先去檢錄。」）
  - 起跑卡 → 配速卡 → 連線回地圖；地圖上 condition 事件 `race_done`（條件 `pace_score` 已寫入且 `phase=start`）：主角移到終點、鏡頭移到看台她的位置、原文「那場比賽他拿了小組第一……」、`phase=vending`。
  - `vending_r1`（`phase=vending`）：林向晚 NPC 在販賣機前、零錢掉落、拿到十塊錢、「妳的十塊錢。」→ `jump` 中章卡。
  - `guidance`：依 `phase` 顯示「去檢錄處拿號碼布」「到八百公尺起跑線」「去體育館後門的販賣機」。
  - 天氣：`environment` 午後光、`ambience.particles:"motes"`。
- [ ] **Step 5：跑 `check_static.py` 全過；本機預覽用鍵盤走一遍第一輪。commit。**

### Task 7：田徑場第二輪、廚房地圖、結局

**Files:**
- Modify: `src/map_stadium.py`、`src/build.py`
- Create: `src/map_kitchen.py`、`assets/placeholder/kitchen.png`

**Interfaces:**
- 中章卡（Task 3）結尾連到草稿卡，草稿卡連到防波堤卡，防波堤卡連到田徑場地圖；進地圖前一張變數卡設 `round=2`、`phase=watch`、`bpm=100`。
- RPG 資料庫兩個角色：`chengche`、`xiangwan`（Task 10 換圖）；第二輪開頭 auto 事件用 `{kind:'hero', value:'xiangwan'}`。
- Produces：`build_kitchen(board) -> map_node`。

- [ ] **Step 1：在 `check_static.py` 加流程檢查**：白板上每張卡從起點走得到；結局 A、B 卡存在；`test_every_original_para_used_once` 應該全過。
- [ ] **Step 2：跑，確認失敗。**
- [ ] **Step 3：第二輪事件**（條件帶 `round=2`，同一格的第一輪事件用 `pages` 切換）：
  - 開場 auto：`hero` 換林向晚、主角放到四百終點、「去看台後面」。
  - 看台邊緣 touch 事件一排（`phase=watch`）：程徹頭上驚嘆號、`bpm=150`、「差點被看到。」、主角移回看台後、`bpm=110`。
  - 線索三個：秩序冊（`clue_order=true`）、隊友 NPC（`clue_mate=true`）、自己走到販賣機前的 touch（`clue_walk=true`，第一次走到時旁白）。三個都有了 → condition 事件 `jump` 筆記卡；筆記卡連回地圖。
  - `calc_ok=true` → 看比賽：鏡頭移到跑道、程徹 NPC 跑一段 `move`、衝線後轉向看台、`balloon` 愛心、`phase=vending2`。
  - `vending_r2`：買寶礦力（拿道具）→ `choice`「讓零錢掉下去／轉身離開」：前者 `jump` 零錢卡（連到防波堤後半→廚房地圖），後者 `jump` 結局 B 卡。
  - 結局 B 卡最後一張是 `choice` 卡「回到販賣機前」→ 連回田徑場地圖（主角留原格，`phase=vending2` 仍成立）。
- [ ] **Step 4：廚房地圖**：12×9 暫代圖；`environment.weather:"rain"`、`darkness:0.4`、`fog`；主角程徹（`hero` 換回 `chengche`）；`lin` NPC 在爐前；走到她身後 action 事件：原文「幾年後的一個冬夜」到「好啊。」、`bpm=72`、原文最後三段、`item` 備用鑰匙（說明用 `new('備用鑰匙說明')`）、結束（`jump` 片尾卡）。
- [ ] **Step 5：跑 `check_static.py` 全過。commit。**

### Task 8：全路徑自動測試

**Files:**
- Create: `tests/play_all.mjs`

- [ ] **Step 1：寫 `play_all.mjs`**（Playwright，從標題「開始」）：讀畫面座標（HUD 的「x, y」文字）用 BFS 路徑走到目標格（地圖碰撞格由 `build.py` 另外輸出 `dist/stadium.grid.json`）；插件卡用 `cards.mjs` 的同一套操作函式；涵蓋：
  1. 第一輪：先不拿號碼布去起跑線 → 看到「先去檢錄」；拿號碼布 → 起跑卡偷跑 2 次再成功 → 配速 → 販賣機 → 中章 → 草稿 → 防波堤。
  2. 第二輪：走出看台被抓 2 次；直接去販賣機（線索沒齊）→ 看到引導；蒐集三條線索 → 筆記錯 1 次再對 → 看比賽 → 販賣機選「轉身離開」→ 結局 B → 回販賣機 → 選「讓零錢掉下去」→ 零錢太早 1 次再成功 → 防波堤後半 → 廚房 → 結局 A，背包有備用鑰匙，HUD 顯示 72。
  3. 起跑卡進行中按存檔、讀檔 → 能繼續玩到配速卡。
  4. iPhone 視窗：每張插件卡各截一張到 `dist/shots/`，人工看一次。
  5. 記錄總時長（不算自動測試的等待），印出來。
- [ ] **Step 2：跑，修到全過。commit。**

### Task 9：推上 Larch，作者第一次試玩

**Files:**
- Create: `src/push.py`

- [ ] **Step 1：`push.py`**：先 `GET` 線上專案存到 `snapshots/<時間>.json`；圖片素材（`assets/` 底下被引用的檔）用 Larch 上傳換成線上網址（新檔才傳，記在 `assets/uploaded.json` 避免重傳）；`PUT` 整份專案；再 `GET` 回來比對節點數、地圖事件數、`settings.plugins['start-line']` 存在。
- [ ] **Step 2：確認插件卡在平台上能跑**：線上預覽連結（`larch_preview_project`）實際打開起跑卡。若平台要求插件必須存在於市集／私人草稿才執行，就用 `larch_save_plugin_draft` 存一份私人的 `start-line` manifest（內容與本機一致），再測一次。
- [ ] **Step 3：把預覽連結給作者試玩**，同時繼續 Task 10（美術）。

### Task 10：正式美術

（可以在 Task 4 開始時就派背景工作線同時進行；每項產完先縮小、檢查，再放進 `assets/`。）

**Files:**
- Create: `assets/art/*`、`art/prompts.md`（每張圖的提示詞與參考圖紀錄）

- [ ] **Step 1：畫風錨**：一張柔和水彩的田徑場午後場景，作者確認後當所有生成的參考圖。
- [ ] **Step 2：角色定錨**：程徹、林向晚高中版正面全身各一張（水彩），作者確認。
- [ ] **Step 3：地圖底圖**：田徑場俯視水彩（照 `assets/placeholder/stadium.png` 的配置，同比例 1280×960），廚房俯視水彩。產完把碰撞格疊上去檢查有沒有對歪。
- [ ] **Step 4：走路圖**：兩位主角各 3×4 格（每格 48×64），用角色定錨當參考；裁判、隊友、路人各一套。放進地圖實走檢查不跳格、不變臉；產不穩超過 30 分鐘就回報作者。
- [ ] **Step 5：立繪**：兩人高中版各 3 種表情、成年版各 2 種，去背（cutout）。
- [ ] **Step 6：CG 5 張**（16:9，下方三分之一留給對話框）：四目相對、衝線望向看台、販賣機前、防波堤、廚房擁抱。給作者看之前先過 CG 檢查清單（手指、衣服、連貫）。
- [ ] **Step 7：插件卡用圖**：起跑第一人稱、她的眼神、筆記本頁、手機外框、零錢特寫、水彩心形。
- [ ] **Step 8：替換**：`build.py` 的圖片路徑從 `assets/placeholder/` 換成 `assets/art/`，重跑 `check_static.py`、`play_all.mjs`，推上 Larch。commit。

### Task 11：收尾

- [ ] **Step 1：標題畫面**：`settings.titleCoverImage`（封面 CG）、專案縮圖、簡介（只講劇情）。
- [ ] **Step 2：作者定稿的 `新寫.md` 重產、重推。**
- [ ] **Step 3：README**：怎麼產、怎麼測、怎麼推。
- [ ] **Step 4：最後一次 `play_all.mjs` 全過，推上 Larch，通知作者在網頁按「發佈作品」並勾第三屆挑戰、標示 AI 使用範圍。**
