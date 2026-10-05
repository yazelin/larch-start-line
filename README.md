# 起跑總在開始前

Larch 第三屆創作者挑戰《自由與限制》投稿作品。程徹與林向晚的田徑愛情短篇，改成 RPG＋自製插件的互動作品。

- 原文：`canon/原文.md`（不改字）；新寫文字：`canon/新寫.md`
- 規格：`docs/specs/2026-10-05-design.md`；計畫：`docs/plans/2026-10-05-start-line.md`

## 產生與預覽

    python3 src/build.py                                  # 產出 dist/project.json
    python3 ~/larch-preview/serve.py dist/project.json    # 本機播放
    node tests/smoke.mjs                                  # 冒煙測試
