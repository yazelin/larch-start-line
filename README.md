# 起跑總在開始前

Larch 第三屆創作者挑戰《自由與限制》投稿作品。程徹與林向晚的田徑愛情短篇，改成 RPG 地圖＋自製插件卡的互動作品：同一個下午玩兩次（先程徹、再林向晚），販賣機前分支成兩個結局。

- 原文：`canon/原文.md`（不改字，遊戲內原文一律從這裡讀）
- 新寫文字：`canon/新寫.md`（結局 B、草稿、線索、簡介…，每段的 `##` 標題是程式取用的鍵）
- 規格：`docs/specs/2026-10-05-design.md`；計畫：`docs/plans/2026-10-05-start-line.md`
- Larch 專案：`project-c0f31c1f-2b06-44d8-a62e-374bff81fd60`
- 遊玩：https://larch.ink/play/market/yaze/start-line （公開站「在 Larch 上遊玩」按鈕讀 `docs/site.json` 的 `playUrl`）
- 公開站：https://yazelin.github.io/larch-start-line/

## 結構

| 檔案 | 內容 |
|---|---|
| `src/build.py` | 組出 `dist/project.json`（劇情卡、地圖、插件、變數、RPG 角色） |
| `src/map_stadium.py`、`src/map_kitchen.py` | 兩張地圖：配置（`cell()`）、事件、任務提示 |
| `src/plugin.py`、`src/plugin/*.html` | 自製插件 `start-line`：心跳 HUD＋起跑、配速、筆記、草稿、零錢五張卡 |
| `src/variables.py` | 全部變數只在這裡定義 |
| `src/art.py` | 美術路徑（正式圖不在就退回 `assets/placeholder/`） |
| `src/push.py` | 推上 Larch：快照→上傳圖→換網址→整包 PUT→讀回比對 |

## 指令

    python3 src/build.py                                  # 產出 dist/project.json
    python3 ~/larch-preview/serve.py dist/project.json    # 本機播放
    python3 tests/check_static.py                         # 靜態檢查（原文全用上、變數閘門、地圖格式、流程走得到）
    node tests/smoke.mjs                                  # 冒煙
    node tests/cards.mjs [卡片 id]                        # 逐張插件卡
    node tests/play_all.mjs                               # 全路徑：兩個結局（約 6 分鐘）
    python3 src/push.py "改了什麼"                         # 推上 Larch（發佈要作者在網頁按）

改了 `canon/新寫.md` 或任何 src 之後：跑 `check_static.py`、`play_all.mjs`，再 `push.py`。
