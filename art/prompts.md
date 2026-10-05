# 美術提示詞紀錄

生圖工具：本機 codex imagegen（codex-imagegen skill）。原圖 PNG 縮成長邊 1600 以內、webp 品質 85。

## style-a.webp

- 參考圖：無（純文字生成）
- 提示詞：

```
Soft watercolor illustration on textured cold-press paper. A Taiwanese high school city athletics meet at a running track in the warm afternoon. Red-orange PU running track with crisp white lane lines curving across the frame, a modest concrete spectator stand on one side, tall green trees in the distance, a pale sky. Light, airy pastel palette, luminous sunlight, soft wet-edge washes, visible paper grain, generous white space and unpainted paper areas. Only a few tiny distant human silhouettes, no close-up people. Wide landscape 16:9 composition. No text, no letters, no numbers, no signage, no watermark.
```

## style-b.webp

- 參考圖：無（純文字生成）
- 提示詞：

```
Delicate transparent watercolor painting with visible paper texture. Low-angle view along a red PU athletics track at a Taiwanese high school city sports meet on a bright afternoon: white lane lines converging toward the far curve, a small grandstand with shade roof, a row of distant trees and light haze. Pale washed colors, glowing backlight, lots of breathing room and white paper left unpainted, loose soft edges. A few very small distant figures only, no close-up people. Wide 16:9 landscape. No text, no letters, no numbers, no watermark.
```

## lin-a.webp

- 參考圖：style-a（畫風錨第一張，image 1）
- 提示詞（lin-a、lin-b 同一段，分兩次生成）：

```
Use image 1 only as the painting style reference: match its soft transparent watercolor technique, paper grain, pale luminous palette and loose wet edges. Do not copy its scenery. A Taiwanese high school girl, 17 years old, women's 400m sprinter. Long straight black hair tied in a low ponytail, fine wispy bangs across the forehead, clear bright eyes with a stubborn, determined look. Slim, athletic build. Wearing the school track team uniform: navy blue sleeveless running singlet with white trim edges, matching navy running shorts with white trim, running shoes. Full-body front view standing pose, head to shoes fully visible and centered, plain flat pale warm-gray / off-white background with only a faint watercolor wash, no scenery. Correct anatomy, five fingers on each hand, natural relaxed arms. Character design reference sheet feel, single figure. No text, no letters, no logos, no watermark. Portrait orientation.
```

## lin-b.webp

- 參考圖：style-a（畫風錨第一張，image 1）
- 提示詞（lin-a、lin-b 同一段，分兩次生成）：

```
Use image 1 only as the painting style reference: match its soft transparent watercolor technique, paper grain, pale luminous palette and loose wet edges. Do not copy its scenery. A Taiwanese high school girl, 17 years old, women's 400m sprinter. Long straight black hair tied in a low ponytail, fine wispy bangs across the forehead, clear bright eyes with a stubborn, determined look. Slim, athletic build. Wearing the school track team uniform: navy blue sleeveless running singlet with white trim edges, matching navy running shorts with white trim, running shoes. Full-body front view standing pose, head to shoes fully visible and centered, plain flat pale warm-gray / off-white background with only a faint watercolor wash, no scenery. Correct anatomy, five fingers on each hand, natural relaxed arms. Character design reference sheet feel, single figure. No text, no letters, no logos, no watermark. Portrait orientation.
```

## cheng-a.webp

- 參考圖：style-a（畫風錨第一張，image 1）
- 提示詞（cheng-a、cheng-b 同一段，分兩次生成）：

```
Use image 1 only as the painting style reference: match its soft transparent watercolor technique, paper grain, pale luminous palette and loose wet edges. Do not copy its scenery. A Taiwanese high school boy, 17 years old, 800m runner. Short neat black hair, clean fresh look, calm quiet expression. Lean runner build. Wearing the school track team uniform: navy blue sleeveless running singlet with white trim edges and a plain white race bib pinned on the chest (the bib is blank, no numbers or letters printed), matching navy running shorts with white trim, running shoes. Full-body front view standing pose, head to shoes fully visible and centered, plain flat pale warm-gray / off-white background with only a faint watercolor wash, no scenery. Correct anatomy, five fingers on each hand, natural relaxed arms. Character design reference sheet feel, single figure. No text, no letters, no logos, no watermark. Portrait orientation.
```

## cheng-b.webp

- 參考圖：style-a（畫風錨第一張，image 1）
- 提示詞（cheng-a、cheng-b 同一段，分兩次生成）：

```
Use image 1 only as the painting style reference: match its soft transparent watercolor technique, paper grain, pale luminous palette and loose wet edges. Do not copy its scenery. A Taiwanese high school boy, 17 years old, 800m runner. Short neat black hair, clean fresh look, calm quiet expression. Lean runner build. Wearing the school track team uniform: navy blue sleeveless running singlet with white trim edges and a plain white race bib pinned on the chest (the bib is blank, no numbers or letters printed), matching navy running shorts with white trim, running shoes. Full-body front view standing pose, head to shoes fully visible and centered, plain flat pale warm-gray / off-white background with only a faint watercolor wash, no scenery. Correct anatomy, five fingers on each hand, natural relaxed arms. Character design reference sheet feel, single figure. No text, no letters, no logos, no watermark. Portrait orientation.
```


## maps/stadium.webp

- 參考圖：image 1 = assets/placeholder/stadium.png（配置色塊圖，構圖依據）；image 2 = style-b（畫風錨）
- 生成 1 次，縮放 1448×1086 → 1920×1440；對位檢查見 maps/check-stadium.jpg
- 提示詞：

```
Image 1 is a flat color-block LAYOUT DIAGRAM of a school athletics stadium seen from directly above; it is the exact composition you must follow. Its colors mean: dark gray outer border = boundary fence / hedge around the whole map; pale beige strip along the very top = a paved walkway behind the grandstand; three taupe/gray-brown blocks in the upper area = covered grandstand seating (the two thin green gaps between them are stair openings, keep them open as narrow stairways); red rectangular ring = red PU running track; the two thin white vertical bars on the bottom straight of the track = the white finish line (left) and start line (right) painted across the lanes; green = grass (both the infield and the surroundings); cream block bottom-left = a white event tent (registration desk) seen from above; light blue-gray block bottom-right = a gymnasium building roof; the small blue square just left of the gymnasium = one drink vending machine at the gym's entrance.
Image 2 is ONLY the painting style reference: match its soft transparent watercolor technique, paper grain, warm afternoon sunlight and luminous palette. Do not copy its camera angle or scenery.
Paint a top-down (straight overhead, orthographic, map view, no perspective, no horizon, no sky) watercolor game map of this stadium in warm afternoon sunlight with soft shadows falling to the lower right. Every element must sit at exactly the same position and size as the matching block in image 1, filling the full frame edge to edge. Red PU running track with thin white lane lines following the ring (corners may be gently rounded), white finish line and start line across the bottom straight where the white bars are, green grass infield and surroundings, the grandstand with a pale canvas shade canopy roof seen from above, the beige walkway behind it, a white tent bottom-left, a gymnasium building roof bottom-right with a single vending machine at its door. No people, no text, no letters, no numbers, no grid lines, no watermark. Landscape 4:3.
```

## maps/kitchen.webp

- 參考圖：image 1 = assets/placeholder/kitchen.png（配置色塊圖，構圖依據）；image 2 = style-b（畫風錨）
- 生成 2 次（第 1 次凳子凸進 x=3 可走格，第 2 次加上餐桌與凳子不可超出色塊的限制後採用），縮放 1448×1086 → 576×432；對位檢查見 maps/check-kitchen.jpg
- 提示詞（採用的第 2 版）：

```
Image 1 is a flat color-block LAYOUT DIAGRAM of a small apartment kitchen seen from directly above; it is the exact composition you must follow. Its colors mean: dark gray outer border = the kitchen walls; brown band across the top = the kitchen counter run along the top wall (sink, a gas stove in the middle with a pot of soup on it, and a window in the top wall above the counter); light cream area = open warm wooden floor; tan block at the lower left = a small dining table; the table and its two little stools must stay completely inside the tan block (stools tucked at the top and bottom ends of the table, nothing sticking out to the right of the tan block).
Image 2 is ONLY the painting style reference: match its soft transparent watercolor technique, paper grain and loose wet edges. Do not copy its scenery, daylight or camera angle.
Paint a top-down (straight overhead, orthographic, map view, no perspective) watercolor game map of this small Taipei kitchen on a winter night. Every element must sit at exactly the same position and size as the matching block in image 1, filling the full frame edge to edge. Along the top: the counter with a sink and a stove where a pot of soup steams gently, and the top wall has a window whose glass is fogged with condensation and streaked with rain from the dark rainy night outside. Warm amber lamp light pools on the wooden floor; the open floor area stays clear and empty. A small wooden dining table at the lower left, filling exactly the tan block, its two stools tucked inside that same block; to the right of the table is only empty floor. Cozy, quiet, warm against the cold blue night. No people, no text, no letters, no grid lines, no watermark. Landscape 4:3.
```

## 立繪與走路圖（2026-10-05）

立繪一律綠幕 #00FF00 生成，cutout skill 去背，premultiplied 縮到高 1400，縮完在邊帶再 despill。表情差分以同角色 calm 綠幕原圖當 image 1。走路圖同樣綠幕。

## portraits/lin-hs-calm.png

- 參考圖：image 1 = lin-b（林向晚定錨）、image 2 = style-b（畫風錨）
- 備註：第 1 次採用。綠幕，cutout 去背，縮到 933×1400。
- 提示詞：

```
Image 1 is the character reference for Lin Xiangwan (林向晚): a Taiwanese 17-year-old high school girl, 400m sprinter. Image 2 is the painting style anchor only (a watercolor running track); do not copy its scenery. Paint Lin Xiangwan exactly as in image 1: same face, same eyes, same long straight black hair tied in a low ponytail with fine wispy bangs, same slim athletic build, same navy blue sleeveless running singlet with white trim edges. Framing: character portrait for a visual novel, from the top of the head down to mid-thigh (navy running shorts with white trim visible at the bottom), body turned slightly to her left (three-quarter front view), face toward the viewer, arms relaxed at her sides. Expression: calm, quiet, slightly stubborn, mouth closed, looking at the viewer. Painting style: match image 2 only for technique: soft transparent watercolor, gentle paper-grain texture inside the figure, pale luminous palette, loose wet edges inside the painting but a clean readable outline against the background. Background: one single flat uniform pure chroma green color (#00FF00) filling the entire background, perfectly even, no gradient, no texture, no paper grain in the background, no shadow, no floor, no vignette, no reflection. The figure must not touch any edge of the image; leave green margin above the head and at both sides. Crisp clean silhouette edges. Correct anatomy, five fingers on each hand. Single figure, no text, no letters, no logos, no watermark. Portrait orientation.
```

## portraits/cheng-hs-calm.png

- 參考圖：image 1 = cheng-a（程徹定錨）、image 2 = style-b
- 備註：第 1 次採用。
- 提示詞：

```
Image 1 is the character reference for Cheng Che (程徹): a Taiwanese 17-year-old high school boy, 800m runner. Image 2 is the painting style anchor only (a watercolor running track); do not copy its scenery. Paint Cheng Che exactly as in image 1: same face, same short slightly messy black hair, same lean runner build, same navy blue sleeveless running singlet with white trim edges and a plain blank white race bib pinned on the chest (the bib is completely blank, no numbers, no letters). Framing: character portrait for a visual novel, from the top of the head down to mid-thigh (navy running shorts with white trim visible at the bottom), body turned slightly to his right (three-quarter front view), face toward the viewer, arms relaxed at his sides. Expression: calm, quiet, composed, mouth closed, looking at the viewer. Painting style: match image 2 only for technique: soft transparent watercolor, gentle paper-grain texture inside the figure, pale luminous palette, loose wet edges inside the painting but a clean readable outline against the background. Background: one single flat uniform pure chroma green color (#00FF00) filling the entire background, perfectly even, no gradient, no texture, no paper grain in the background, no shadow, no floor, no vignette, no reflection. The figure must not touch any edge of the image; leave green margin above the head and at both sides. Crisp clean silhouette edges. Correct anatomy, five fingers on each hand. Single figure, no text, no letters, no logos, no watermark. Portrait orientation.
```

## portraits/lin-adult-calm.png

- 參考圖：image 1 = lin-b（林向晚高中定錨，臉的依據）、image 2 = style-b
- 備註：第 1 次採用。
- 提示詞：

```
Image 1 is the character reference for Lin Xiangwan (林向晚) as a 17-year-old high school girl. Image 2 is the painting style anchor only (a watercolor running track); do not copy its scenery. Paint the same woman a few years later, about 24 years old: clearly the same face as image 1 (same eyes, same face shape, same fine wispy bangs), just a little more mature, long straight black hair now worn in a loose low ponytail. She wears winter casual clothes at home: an oversized cream-white chunky cable-knit sweater with sleeves slightly covering her hands, soft light-beige lounge pants. No sportswear. Framing: character portrait for a visual novel, from the top of the head down to mid-thigh, body turned slightly to her left (three-quarter front view), face toward the viewer, arms relaxed. Expression: calm, gentle, quiet, mouth closed, looking at the viewer. Painting style: match image 2 only for technique: soft transparent watercolor, gentle paper-grain texture inside the figure, pale luminous palette, loose wet edges inside the painting but a clean readable outline against the background. Background: one single flat uniform pure chroma green color (#00FF00) filling the entire background, perfectly even, no gradient, no texture, no paper grain in the background, no shadow, no floor, no vignette, no reflection. The figure must not touch any edge of the image; leave green margin above the head and at both sides. Crisp clean silhouette edges. Correct anatomy, five fingers on each hand. Single figure, no text, no letters, no logos, no watermark. Portrait orientation.
```

## portraits/cheng-adult-calm.png

- 參考圖：image 1 = cheng-a（程徹高中定錨，臉的依據）、image 2 = style-b
- 備註：第 1 次採用。
- 提示詞：

```
Image 1 is the character reference for Cheng Che (程徹) as a 17-year-old high school boy. Image 2 is the painting style anchor only (a watercolor running track); do not copy its scenery. Paint the same man a few years later, about 24 years old: clearly the same face as image 1 (same eyes, same face shape), just a little more mature, short black hair slightly neater. He wears winter casual clothes at home: a charcoal-gray crew-neck knit sweater over a white t-shirt collar, dark gray sweatpants. No sportswear, no race bib. Framing: character portrait for a visual novel, from the top of the head down to mid-thigh, body turned slightly to his right (three-quarter front view), face toward the viewer, arms relaxed. Expression: calm, quiet, composed, mouth closed, looking at the viewer. Painting style: match image 2 only for technique: soft transparent watercolor, gentle paper-grain texture inside the figure, pale luminous palette, loose wet edges inside the painting but a clean readable outline against the background. Background: one single flat uniform pure chroma green color (#00FF00) filling the entire background, perfectly even, no gradient, no texture, no paper grain in the background, no shadow, no floor, no vignette, no reflection. The figure must not touch any edge of the image; leave green margin above the head and at both sides. Crisp clean silhouette edges. Correct anatomy, five fingers on each hand. Single figure, no text, no letters, no logos, no watermark. Portrait orientation.
```

## portraits/lin-hs-smile.png

- 參考圖：image 1 = lin-hs-calm 綠幕原圖（林向晚）、image 2 = style-b
- 備註：第 1 次採用。
- 提示詞：

```
Image 1 is the approved calm portrait of Lin Xiangwan (林向晚), a 17-year-old Taiwanese high school girl sprinter in a navy singlet with white trim, long black hair in a low ponytail with wispy bangs. Image 2 is the painting style anchor only (soft transparent watercolor); do not copy its scenery. Repaint the same character in the same framing, same pose angle, same body, same clothes, same hairstyle, same watercolor technique and the same flat pure chroma green (#00FF00) background as image 1. The face must stay the same person as image 1. Change only the facial expression (and a small natural head tilt or shoulder movement is allowed): a small genuine smile, eyes slightly softened, a little shy but bright, mouth gently curved, teeth barely or not visible. Correct anatomy, five fingers on each hand. Background: one single flat uniform pure chroma green color (#00FF00) filling the entire background, perfectly even, no gradient, no texture, no shadow, no floor, no vignette. The figure must not touch the left, right or top edge. Single figure, no text, no letters, no logos, no watermark. Portrait orientation.
```

## portraits/lin-hs-surprised.png

- 參考圖：image 1 = lin-hs-calm 綠幕原圖（林向晚）、image 2 = style-b
- 備註：第 1 次採用。
- 提示詞：

```
Image 1 is the approved calm portrait of Lin Xiangwan (林向晚), a 17-year-old Taiwanese high school girl sprinter in a navy singlet with white trim, long black hair in a low ponytail with wispy bangs. Image 2 is the painting style anchor only (soft transparent watercolor); do not copy its scenery. Repaint the same character in the same framing, same pose angle, same body, same clothes, same hairstyle, same watercolor technique and the same flat pure chroma green (#00FF00) background as image 1. The face must stay the same person as image 1. Change only the facial expression (and a small natural head tilt or shoulder movement is allowed): surprised: eyes widened, eyebrows raised, lips slightly parted in a small round opening, a faint blush. Correct anatomy, five fingers on each hand. Background: one single flat uniform pure chroma green color (#00FF00) filling the entire background, perfectly even, no gradient, no texture, no shadow, no floor, no vignette. The figure must not touch the left, right or top edge. Single figure, no text, no letters, no logos, no watermark. Portrait orientation.
```

## portraits/lin-adult-smile.png

- 參考圖：image 1 = lin-adult-calm 綠幕原圖（成年林向晚）、image 2 = style-b
- 備註：第 1 次採用。
- 提示詞：

```
Image 1 is the approved calm portrait of Lin Xiangwan (林向晚) as an adult woman around 24, in a cream cable-knit sweater and beige lounge pants at home in winter, black hair in a loose low ponytail. Image 2 is the painting style anchor only (soft transparent watercolor); do not copy its scenery. Repaint the same character in the same framing, same pose angle, same body, same clothes, same hairstyle, same watercolor technique and the same flat pure chroma green (#00FF00) background as image 1. The face must stay the same person as image 1. Change only the facial expression (and a small natural head tilt or shoulder movement is allowed): a soft warm smile, eyes gently curved, relaxed and tender. Correct anatomy, five fingers on each hand. Background: one single flat uniform pure chroma green color (#00FF00) filling the entire background, perfectly even, no gradient, no texture, no shadow, no floor, no vignette. The figure must not touch the left, right or top edge. Single figure, no text, no letters, no logos, no watermark. Portrait orientation.
```

## portraits/cheng-hs-smile.png

- 參考圖：image 1 = cheng-hs-calm 綠幕原圖（程徹）、image 2 = style-b
- 備註：第 1 次採用。
- 提示詞：

```
Image 1 is the approved calm portrait of Cheng Che (程徹), a 17-year-old Taiwanese high school boy 800m runner in a navy singlet with white trim and a completely blank white race bib (no numbers, no letters), short black hair. Image 2 is the painting style anchor only (soft transparent watercolor); do not copy its scenery. Repaint the same character in the same framing, same pose angle, same body, same clothes, same hairstyle, same watercolor technique and the same flat pure chroma green (#00FF00) background as image 1. The face must stay the same person as image 1. Change only the facial expression (and a small natural head tilt or shoulder movement is allowed): a quiet warm smile, eyes slightly softened, mouth gently curved, restrained and gentle. Correct anatomy, five fingers on each hand. Background: one single flat uniform pure chroma green color (#00FF00) filling the entire background, perfectly even, no gradient, no texture, no shadow, no floor, no vignette. The figure must not touch the left, right or top edge. Single figure, no text, no letters, no logos, no watermark. Portrait orientation.
```

## portraits/cheng-hs-surprised.png

- 參考圖：image 1 = cheng-hs-calm 綠幕原圖（程徹）、image 2 = style-b
- 備註：第 1 次採用。
- 提示詞：

```
Image 1 is the approved calm portrait of Cheng Che (程徹), a 17-year-old Taiwanese high school boy 800m runner in a navy singlet with white trim and a completely blank white race bib (no numbers, no letters), short black hair. Image 2 is the painting style anchor only (soft transparent watercolor); do not copy its scenery. Repaint the same character in the same framing, same pose angle, same body, same clothes, same hairstyle, same watercolor technique and the same flat pure chroma green (#00FF00) background as image 1. The face must stay the same person as image 1. Change only the facial expression (and a small natural head tilt or shoulder movement is allowed): surprised: eyes widened, eyebrows raised, lips slightly parted, caught off guard. Correct anatomy, five fingers on each hand. Background: one single flat uniform pure chroma green color (#00FF00) filling the entire background, perfectly even, no gradient, no texture, no shadow, no floor, no vignette. The figure must not touch the left, right or top edge. Single figure, no text, no letters, no logos, no watermark. Portrait orientation.
```

## portraits/cheng-adult-smile.png

- 參考圖：image 1 = cheng-adult-calm 綠幕原圖（成年程徹）、image 2 = style-b
- 備註：第 1 次採用。
- 提示詞：

```
Image 1 is the approved calm portrait of Cheng Che (程徹) as an adult man around 24, in a charcoal-gray knit sweater over a white t-shirt collar and dark gray sweatpants at home in winter, short black hair. Image 2 is the painting style anchor only (soft transparent watercolor); do not copy its scenery. Repaint the same character in the same framing, same pose angle, same body, same clothes, same hairstyle, same watercolor technique and the same flat pure chroma green (#00FF00) background as image 1. The face must stay the same person as image 1. Change only the facial expression (and a small natural head tilt or shoulder movement is allowed): a soft warm smile, eyes gently softened, relaxed and tender. Correct anatomy, five fingers on each hand. Background: one single flat uniform pure chroma green color (#00FF00) filling the entire background, perfectly even, no gradient, no texture, no shadow, no floor, no vignette. The figure must not touch the left, right or top edge. Single figure, no text, no letters, no logos, no watermark. Portrait orientation.
```

## walk/walk-cheng.png

- 參考圖：image 1 = cheng-a（程徹）、image 2 = style-b
- 備註：第 1 次採用。3×4 大圖去背後依連通區塊切出 12 格，同一倍率縮放，頭部置中、腳底貼第 63 列。
- 提示詞：

```
Image 1 is the character reference for Cheng Che (程徹), a Taiwanese 17-year-old high school boy runner: short slightly messy black hair, navy blue sleeveless running singlet with white trim edges, a completely blank white race bib on the chest, navy running shorts with white trim, white running shoes with navy accents. Image 2 is the watercolor painting style anchor only; do not copy its scenery. Draw Cheng Che as a walking sprite sheet, keeping his hair, outfit and colors identical in all 12 figures. Layout (very important): a sprite reference sheet arranged as an exact grid of 3 columns and 4 rows, 12 small full-body figures total, all the same character, same size, evenly spaced, each figure centered in its own equal cell with generous green space around it, figures do not overlap or touch each other or the image edges, no grid lines, no borders, no labels. Row 1 (top): character facing toward the viewer (front view, walking down). Row 2: character facing the viewer's LEFT (side profile, nose pointing to the left edge of the image, walking left). Row 3: character facing the viewer's RIGHT (side profile, nose pointing to the right edge, walking right). Row 4 (bottom): character seen from behind (back view, walking away, face not visible). In every row: left cell = walking step with one leg forward, middle cell = neutral standing pose with both feet together, right cell = walking step with the other leg forward; the arms swing opposite to the legs. Character style: cute chibi, 2 heads tall (big head, small body), soft transparent watercolor coloring like image 2 but with a clear, clean dark outline so it reads at tiny size, simple shapes, full body from head to shoes, all feet at the same baseline within each row. Background: one single flat uniform pure chroma green color (#00FF00) everywhere, no shadow under the feet, no floor, no texture, no gradient. No text, no letters, no numbers, no logos, no watermark. Portrait orientation.
```

## walk/walk-lin.png

- 參考圖：image 1 = lin-b（林向晚）、image 2 = style-b
- 備註：第 1 次採用，處理同上。
- 提示詞：

```
Image 1 is the character reference for Lin Xiangwan (林向晚), a Taiwanese 17-year-old high school girl sprinter: long straight black hair tied in a low ponytail (the ponytail must be clearly visible from the side and back views), wispy bangs, navy blue sleeveless running singlet with white trim edges, navy running shorts with white trim, white running shoes. Image 2 is the watercolor painting style anchor only; do not copy its scenery. Draw Lin Xiangwan as a walking sprite sheet, keeping her hair, outfit and colors identical in all 12 figures. Layout (very important): a sprite reference sheet arranged as an exact grid of 3 columns and 4 rows, 12 small full-body figures total, all the same character, same size, evenly spaced, each figure centered in its own equal cell with generous green space around it, figures do not overlap or touch each other or the image edges, no grid lines, no borders, no labels. Row 1 (top): character facing toward the viewer (front view, walking down). Row 2: character facing the viewer's LEFT (side profile, nose pointing to the left edge of the image, walking left). Row 3: character facing the viewer's RIGHT (side profile, nose pointing to the right edge, walking right). Row 4 (bottom): character seen from behind (back view, walking away, face not visible). In every row: left cell = walking step with one leg forward, middle cell = neutral standing pose with both feet together, right cell = walking step with the other leg forward; the arms swing opposite to the legs. Character style: cute chibi, 2 heads tall (big head, small body), soft transparent watercolor coloring like image 2 but with a clear, clean dark outline so it reads at tiny size, simple shapes, full body from head to shoes, all feet at the same baseline within each row. Background: one single flat uniform pure chroma green color (#00FF00) everywhere, no shadow under the feet, no floor, no texture, no gradient. No text, no letters, no numbers, no logos, no watermark. Portrait orientation.
```

## walk/walk-judge.png

- 參考圖：image 1 = style-b（畫風錨，無角色參考）
- 備註：第 1 次採用，處理同上。
- 提示詞：

```
Image 1 is the watercolor painting style anchor only (a school running track); do not copy its scenery. Draw a track-and-field meet official (referee), a middle-aged Taiwanese man: white short-sleeved polo shirt, dark navy-black long trousers, black shoes, a white bucket-style official's cap with a dark band, short black hair under the cap. He is a walking sprite sheet, identical in all 12 figures. Layout (very important): a sprite reference sheet arranged as an exact grid of 3 columns and 4 rows, 12 small full-body figures total, all the same character, same size, evenly spaced, each figure centered in its own equal cell with generous green space around it, figures do not overlap or touch each other or the image edges, no grid lines, no borders, no labels. Row 1 (top): character facing toward the viewer (front view, walking down). Row 2: character facing the viewer's LEFT (side profile, nose pointing to the left edge of the image, walking left). Row 3: character facing the viewer's RIGHT (side profile, nose pointing to the right edge, walking right). Row 4 (bottom): character seen from behind (back view, walking away, face not visible). In every row: left cell = walking step with one leg forward, middle cell = neutral standing pose with both feet together, right cell = walking step with the other leg forward; the arms swing opposite to the legs. Character style: cute chibi, 2 heads tall (big head, small body), soft transparent watercolor coloring like image 2 but with a clear, clean dark outline so it reads at tiny size, simple shapes, full body from head to shoes, all feet at the same baseline within each row. Background: one single flat uniform pure chroma green color (#00FF00) everywhere, no shadow under the feet, no floor, no texture, no gradient. No text, no letters, no numbers, no logos, no watermark. Portrait orientation.
```

## walk/walk-mate.png（第 1 次，未採用）

- 參考圖：image 1 = cheng-a（只取校隊制服）、image 2 = style-b
- 備註：頭身比約三頭半，跟主角兩張不一致，重產。
- 提示詞：

```
Image 1 is the reference for Cheng Che (程徹), only to show the school track team uniform: navy blue sleeveless running singlet with white trim edges, navy running shorts with white trim, white running shoes. Image 2 is the watercolor painting style anchor only; do not copy its scenery. Draw a DIFFERENT boy, Cheng Che's male teammate from the same school: 17-year-old Taiwanese boy, very short buzz-cut black hair (short flat crew cut), slightly sturdier build, cheerful face, wearing the same school track uniform as image 1 but with NO race bib. He is a walking sprite sheet, identical in all 12 figures. Layout (very important): a sprite reference sheet arranged as an exact grid of 3 columns and 4 rows, 12 small full-body figures total, all the same character, same size, evenly spaced, each figure centered in its own equal cell with generous green space around it, figures do not overlap or touch each other or the image edges, no grid lines, no borders, no labels. Row 1 (top): character facing toward the viewer (front view, walking down). Row 2: character facing the viewer's LEFT (side profile, nose pointing to the left edge of the image, walking left). Row 3: character facing the viewer's RIGHT (side profile, nose pointing to the right edge, walking right). Row 4 (bottom): character seen from behind (back view, walking away, face not visible). In every row: left cell = walking step with one leg forward, middle cell = neutral standing pose with both feet together, right cell = walking step with the other leg forward; the arms swing opposite to the legs. Character style: cute chibi, 2 heads tall (big head, small body), soft transparent watercolor coloring like image 2 but with a clear, clean dark outline so it reads at tiny size, simple shapes, full body from head to shoes, all feet at the same baseline within each row. Background: one single flat uniform pure chroma green color (#00FF00) everywhere, no shadow under the feet, no floor, no texture, no gradient. No text, no letters, no numbers, no logos, no watermark. Portrait orientation.
```

## walk/walk-mate.png

- 參考圖：image 1 = cheng-a（只取校隊制服，畫的是另一個男生）、image 2 = style-b
- 備註：第 2 次採用（第 1 次比例不對），處理同上。
- 提示詞：

```
Image 1 is the reference for Cheng Che (程徹), only to show the school track team uniform: navy blue sleeveless running singlet with white trim edges, navy running shorts with white trim, white running shoes. Image 2 is the watercolor painting style anchor only; do not copy its scenery. Draw a DIFFERENT boy, Cheng Che's male teammate from the same school: 17-year-old Taiwanese boy, very short buzz-cut black hair (short flat crew cut), cheerful round face, wearing the same school track uniform as image 1 but with NO race bib. He is a walking sprite sheet, identical in all 12 figures. Layout (very important): a sprite reference sheet arranged as an exact grid of 3 columns and 4 rows, 12 small full-body figures total, all the same character, same size, evenly spaced, each figure centered in its own equal cell with generous green space around it, figures do not overlap or touch each other or the image edges, no grid lines, no borders, no labels. Row 1 (top): character facing toward the viewer (front view, walking down). Row 2: character facing the viewer's LEFT (side profile, nose pointing to the left edge of the image, walking left). Row 3: character facing the viewer's RIGHT (side profile, nose pointing to the right edge, walking right). Row 4 (bottom): character seen from behind (back view, walking away, face not visible). In every row: left cell = walking step with one leg forward, middle cell = neutral standing pose with both feet together, right cell = walking step with the other leg forward; the arms swing opposite to the legs. Character style: cute super-deformed chibi, EXACTLY 2 heads tall: the head is as tall as the whole body below it, very big round head, short stubby body and short legs (same chibi proportions as a classic RPG walking sprite), soft transparent watercolor coloring like image 2 but with a clear, clean dark outline so it reads at tiny size, simple shapes, full body from head to shoes, all feet at the same baseline within each row. Background: one single flat uniform pure chroma green color (#00FF00) everywhere, no shadow under the feet, no floor, no texture, no gradient. No text, no letters, no numbers, no logos, no watermark. Portrait orientation.
```

## walk/walk-runner.png

- 參考圖：image 1 = style-b（畫風錨，無角色參考）
- 備註：第 1 次採用，處理同上。
- 提示詞：

```
Image 1 is the watercolor painting style anchor only (a school running track); do not copy its scenery. Draw a high school runner from a rival school: 17-year-old Taiwanese boy, short black hair, red sleeveless running singlet with white trim, black running shorts, white running shoes. He is a walking sprite sheet, identical in all 12 figures. Layout (very important): a sprite reference sheet arranged as an exact grid of 3 columns and 4 rows, 12 small full-body figures total, all the same character, same size, evenly spaced, each figure centered in its own equal cell with generous green space around it, figures do not overlap or touch each other or the image edges, no grid lines, no borders, no labels. Row 1 (top): character facing toward the viewer (front view, walking down). Row 2: character facing the viewer's LEFT (side profile, nose pointing to the left edge of the image, walking left). Row 3: character facing the viewer's RIGHT (side profile, nose pointing to the right edge, walking right). Row 4 (bottom): character seen from behind (back view, walking away, face not visible). In every row: left cell = walking step with one leg forward, middle cell = neutral standing pose with both feet together, right cell = walking step with the other leg forward; the arms swing opposite to the legs. Character style: cute chibi, 2 heads tall (big head, small body), soft transparent watercolor coloring like image 2 but with a clear, clean dark outline so it reads at tiny size, simple shapes, full body from head to shoes, all feet at the same baseline within each row. Background: one single flat uniform pure chroma green color (#00FF00) everywhere, no shadow under the feet, no floor, no texture, no gradient. No text, no letters, no numbers, no logos, no watermark. Portrait orientation.
```

## 劇情 CG 與插件卡背景（2026-10-05）

原圖 1672×941 PNG，放大裁成 1920×1080、webp 品質 85。參考圖都是 assets/art/anchors/ 下的定錨圖轉成 PNG 後傳入。

## cg/cg-gaze.webp

- 參考圖：style-b（image 1，畫風錨）、lin-b（image 2，林向晚）、cheng-a（image 3，程徹）
- 生成 1 次，第 1 張採用。
- 提示詞：

```
Image 1 is the painting style reference only (scenery of a red athletics track; do not copy its exact layout). Image 2 is the character design of LIN XIANGWAN, a 17-year-old Taiwanese high school girl sprinter: keep her face, long black hair in a low ponytail with wispy bangs, slim athletic build. Image 3 is the character design of CHENG CHE, a 17-year-old Taiwanese high school boy 800m runner: keep his face and short messy black hair.

Scene: just behind the finish line of a red PU running track at a city high school athletics meet, sunny afternoon. LIN XIANGWAN (from image 2) has just finished the 400m: she is bent forward with both hands braced on her knees, breathing hard, sweat on her jaw and a few drops falling onto the red track making tiny dark spots. At this exact moment she suddenly lifts her head and looks up; the wind blows the wisps of hair on her forehead into disarray. Her eyes are clear and stubborn. She is on the left side of the frame, three-quarter view facing right.
CHENG CHE (from image 3) stands on the right side of the frame at the outer edge of the track, still and upright, holding a blank white race number bib and a few safety pins in his hands (the bib is not yet pinned on, his chest is plain). He is looking at her; their eyes meet across the space between them. Quiet, charged moment, no one else close by; distant spectators and stand tiny and blurred.
Both wear the team uniform exactly as in images 2 and 3: navy blue sleeveless running singlet with white trim edges and navy running shorts with white trim, white running shoes. The bib is blank white with nothing printed.

Painting style: delicate transparent watercolor on textured cold-press paper, exactly like image 1 — pale luminous washes, glowing backlight through trees, dappled leaf shadows, loose soft wet edges, visible paper grain, unpainted white paper areas. Hand-painted watercolor illustration, not anime cel shading, not 3D, not photo.
Wide 16:9 landscape composition. Keep all important subjects and faces in the upper two thirds of the frame; the bottom third should be calm, low-detail ground or background (a dialogue box will cover it). Correct anatomy: each hand has exactly five fingers, left and right hands on the correct sides. No text, no letters, no numbers, no logos, no brand names, no signage, no watermark.
```

## cg/cg-finish.webp

- 參考圖：style-b（image 1，畫風錨）、cheng-a（image 2，程徹）、lin-b（image 3，林向晚）
- 生成 2 次。第 1 次沒有人群、像獨跑，加上「越過人群」那段重產；採用第 2 張，下方為第 2 版提示詞。
- 提示詞：

```
Image 1 is the painting style reference only. Image 2 is the character design of CHENG CHE, a 17-year-old Taiwanese high school boy 800m runner: keep his face, short messy black hair, navy blue sleeveless singlet with white trim and a blank white race bib pinned on the chest, navy shorts with white trim. Image 3 is the character design of LIN XIANGWAN, a 17-year-old Taiwanese high school girl: keep her face and long black hair in a low ponytail.

Scene: high school city athletics meet, bright afternoon. CHENG CHE (from image 2) is the large main figure on the left half of the frame, just crossing the finish line of the red PU track in mid-stride, chest forward, a white finish line under his feet. He is NOT looking at any scoreboard or clock; his head is turned and he looks past the crowd of runners and officials, up toward the spectator stand on the right side of the frame. His race bib is blank white with nothing printed.
On the right side, smaller and further away, up in a concrete spectator stand with a shade roof: LIN XIANGWAN (from image 3), sitting in the stand, still in her navy singlet, hugging a folded navy track jacket against her chest with one arm, drinking water from a plastic bottle held in the other hand. She is clearly recognizable but small in the frame. A few other blurred spectators around her.
Between him and the stand there is a busy crowd: other runners in different colored singlets finishing just behind him, race officials with clipboards at the finish line, and a row of cheering spectators leaning on the stand railing. He looks past and over all of these people. A diagonal line of sight connects him to her. Sense of motion and wind for him, stillness for her.

Painting style: delicate transparent watercolor on textured cold-press paper, exactly like image 1 — pale luminous washes, glowing backlight through trees, dappled leaf shadows, loose soft wet edges, visible paper grain, unpainted white paper areas. Hand-painted watercolor illustration, not anime cel shading, not 3D, not photo.
Wide 16:9 landscape composition. Keep all important subjects and faces in the upper two thirds of the frame; the bottom third should be calm, low-detail ground or background (a dialogue box will cover it). Correct anatomy: each hand has exactly five fingers, left and right hands on the correct sides. No text, no letters, no numbers, no logos, no brand names, no signage, no watermark.
```

## cg/cg-vending.webp

- 參考圖：style-b（image 1，畫風錨）、cheng-a（image 2，程徹）、lin-b（image 3，林向晚）
- 呼叫 2 次：第 1 次 codex 沒產出圖（腳本失敗、無錯誤訊息），第 2 次採用。
- 提示詞：

```
Image 1 is the painting style reference only. Image 2 is the character design of CHENG CHE, a 17-year-old Taiwanese high school boy runner: keep his face, short messy black hair, navy blue sleeveless singlet with white trim with a blank white race bib pinned on the chest, navy shorts with white trim. Image 3 is the character design of LIN XIANGWAN, a 17-year-old Taiwanese high school girl sprinter: keep her face, long black hair in a low ponytail with wispy bangs, navy singlet with white trim and navy shorts with white trim.

Scene: outside the back door of a school gymnasium on a sunny afternoon, a concrete walkway in dappled tree shade. A plain drinks vending machine (its front shows only rows of generic colored drink cans, no words, no brand logos) stands against the pale wall. A few coins are scattered on the concrete ground in front of it.
CHENG CHE (from image 2) is bending down, reaching low, picking up one coin from the ground between his thumb and index finger, glancing up toward her.
LIN XIANGWAN (from image 3) stands next to the vending machine, holding one drink can in one hand: a plain blue-and-white sports drink can (blue and white color bands only, no lettering, no logo). She looks down at him, composed, a very slight secret smile.
Place both people and the machine in the upper two thirds; the coins can be in the middle of the frame.

Painting style: delicate transparent watercolor on textured cold-press paper, exactly like image 1 — pale luminous washes, glowing backlight through trees, dappled leaf shadows, loose soft wet edges, visible paper grain, unpainted white paper areas. Hand-painted watercolor illustration, not anime cel shading, not 3D, not photo.
Wide 16:9 landscape composition. Keep all important subjects and faces in the upper two thirds of the frame; the bottom third should be calm, low-detail ground or background (a dialogue box will cover it). Correct anatomy: each hand has exactly five fingers, left and right hands on the correct sides. No text, no letters, no numbers, no logos, no brand names, no signage, no watermark.
```

## cg/cg-seawall.webp

- 參考圖：style-b（image 1，畫風錨）、lin-b（image 2，林向晚）、cheng-a（image 3，程徹）
- 生成 3 次。第 1 次夕陽落在海上（花蓮面東，不可能），加地理說明重產；第 2 次地理對了但海浪平、紋理像馬賽克；第 3 次加強急浪與水彩質地，採用。下方為第 3 版提示詞。
- 提示詞：

```
Image 1 is the painting style reference only (watercolor technique, paper texture, soft edges; do not copy the track scenery). Image 2 is LIN XIANGWAN: keep her face and long black hair, but she is now a 21-year-old university student, slightly more mature. Image 3 is CHENG CHE: keep his face and short black hair, but he is now a 21-year-old university student, slightly more mature.

Scene: a summer evening at the seaside in Hualien, Taiwan, at dusk. The two sit side by side on top of a concrete seawall / breakwater, seen from a three-quarter side view slightly from below. The sea right below the wall is rough and fast: big dark-blue waves rushing in and crashing against the base of the wall with splashing white foam and spray, clearly painted as moving water. Geography: Hualien is on Taiwan's EAST coast facing the Pacific, so the sun sets BEHIND the mountains on land, never over the sea. There is NO sun visible anywhere and NO sunset glow on the sea horizon. Over the ocean the evening sky is a deepening dusky blue-violet with a few first stars just appearing; only a faint pink afterglow lingers above the dark green coastal mountains on the land side.
LIN XIANGWAN (from image 2) wears casual summer clothes: a light loose shirt and shorts, her long black hair loose and blown by the sea breeze. Her legs dangle over the edge, swinging. She has turned her head toward him with a sly, mischievous, knowing smile in her eyes.
CHENG CHE (from image 3) wears a plain casual T-shirt and pants, sitting beside her, turning toward her, slightly surprised.
Both are casual civilians, no sports uniforms. Figures placed in the upper-middle of the frame, sky and stars above; bottom third is the seawall and dark water.

Painting style: delicate transparent watercolor on textured cold-press paper, exactly like image 1 — pale luminous washes, glowing backlight through trees, dappled leaf shadows, loose soft wet edges, visible paper grain, unpainted white paper areas. Hand-painted watercolor illustration with smooth soft wet washes and gradients (no mosaic, no pixelated or blocky texture), not anime cel shading, not 3D, not photo.
Wide 16:9 landscape composition. Keep all important subjects and faces in the upper two thirds of the frame; the bottom third should be calm, low-detail ground or background (a dialogue box will cover it). Correct anatomy: each hand has exactly five fingers, left and right hands on the correct sides. No text, no letters, no numbers, no logos, no brand names, no signage, no watermark.
```

## cg/cg-kitchen.webp

- 參考圖：style-b（image 1，畫風錨）、lin-b（image 2，林向晚）、cheng-a（image 3，程徹）
- 生成 3 次。第 1 次爐火還亮著（原文是程徹已關火）；第 2 次火關了但窗戶沒起霧；第 3 次加強白霧描述，採用。下方為第 3 版提示詞。
- 提示詞：

```
Image 1 is the painting style reference only (watercolor technique, paper grain, soft edges; do not copy the track scenery, this is an indoor night scene). Image 2 is LIN XIANGWAN: keep her face and black hair, but she is now an adult woman in her late twenties. Image 3 is CHENG CHE: keep his face and short black hair, but he is now an adult man in his late twenties.

Scene: a winter night in a small Taipei apartment kitchen. Warm lamp light inside. The window behind them is COMPLETELY steamed up: the whole glass is an opaque milky-white fog of condensation from the hot soup, so you can barely see outside; only very faint soft smudges of city lights and a few thin trickles of water run down the white fogged glass. It is drizzling outside. On the small gas stove a pot of soup still steams, but the burner has just been TURNED OFF: there is NO flame, no blue fire, no glow under the pot, the burner is dark and cold. A range hood above. A ladle rests on the pot.
CHENG CHE (from image 3) stands holding her, in a comfortable home sweater. LIN XIANGWAN (from image 2), in soft home clothes (a loose knit cardigan), with her long black hair down, has just turned around to face him and hugs him back around his waist with both arms, her cheek pressed against his chest, eyes gently closed, calm and content. He lowers his head toward the top of her head, his arms around her back.
Quiet, tender, intimate but simple. No rings, no jewelry on any hand. Figures in the upper and middle of the frame, faces clearly visible in the upper half.

Painting style: delicate transparent watercolor on textured cold-press paper, exactly like image 1 — pale luminous washes, glowing backlight through trees, dappled leaf shadows, loose soft wet edges, visible paper grain, unpainted white paper areas. Hand-painted watercolor illustration, not anime cel shading, not 3D, not photo.
Wide 16:9 landscape composition. Keep all important subjects and faces in the upper two thirds of the frame; the bottom third should be calm, low-detail ground or background (a dialogue box will cover it). Correct anatomy: each hand has exactly five fingers, left and right hands on the correct sides. No text, no letters, no numbers, no logos, no brand names, no signage, no watermark.
```

## cards/start-pov.webp

- 參考圖：style-b（image 1，畫風錨）
- 生成 1 次，第 1 張採用。
- 提示詞：

```
Image 1 is the painting style reference: match its watercolor technique, the red PU track color and texture, white lane lines, paper grain, soft light.

First-person point of view of a sprinter crouched at the start, looking straight down at the red PU running track. A single crisp white start line runs horizontally across the upper-middle of the frame. Just behind the line, the runner's own two hands rest on the track in the sprint start "set" position: fingertips bridged on the surface, thumbs and index fingers spread forming arches, the LEFT hand on the left side of the frame and the RIGHT hand on the right side, wrists coming in from the bottom edge, each hand with exactly five fingers (four fingers and one thumb), fingers not touching the white line. Forearms partly visible, wearing nothing on the wrists. A corner of a metal starting block is visible near one lower edge. Warm afternoon light, soft shadows.
Keep the lower-middle part of the image clean and simple (plain red track texture) because a text box will cover it. Hands and start line in the upper half.
No text, no letters, no numbers, no logos, no watermark. Wide 16:9 landscape. Soft transparent watercolor, visible paper grain, not photo, not 3D.
```

## cards/pace-eyes.webp

- 參考圖：style-b（image 1，畫風錨）、lin-b（image 2，林向晚）
- 生成 1 次，第 1 張採用。
- 提示詞：

```
Image 1 is the painting style reference only. Image 2 is the character design of LIN XIANGWAN, a 17-year-old Taiwanese high school girl sprinter: keep her face, eye shape, black hair and wispy bangs.

Close-up of LIN XIANGWAN's face (from image 2), the instant she lifts her head after running: framed from mid-nose up to above the forehead, wide horizontal crop focusing on her eyes. Her eyes are clear and stubborn, looking straight ahead slightly toward the viewer. The wind blows the wisps of black hair on her forehead into disarray across her brow. A faint sheen of sweat, a little flush on the cheeks. Backlit afternoon sunlight, soft red track and green trees blurred far behind.
The eyes sit in the upper half of the frame; the lower part fades into soft, pale watercolor wash with low detail.
Painting style: delicate transparent watercolor on textured cold-press paper, exactly like image 1 — pale luminous washes, glowing backlight through trees, dappled leaf shadows, loose soft wet edges, visible paper grain, unpainted white paper areas. Hand-painted watercolor illustration, not anime cel shading, not 3D, not photo.
Wide 16:9 landscape. No text, no letters, no logos, no watermark.
```

## cards/coin-bg.webp

- 參考圖：style-b（image 1，畫風錨）
- 生成 1 次，第 1 張採用。
- 提示詞：

```
Image 1 is the painting style reference: match its soft transparent watercolor technique, glowing backlight, dappled leaf shadows, paper grain.

Background scene with NO people: the walkway outside the back door of a Taiwanese high school gymnasium on a sunny afternoon, seen from the side. A concrete walkway runs horizontally across the frame along the pale wall of the gym; a back door (metal double door, closed) in the wall; a single plain drinks vending machine standing against the wall in the left-center (its front shows only rows of generic colored drink cans, no words, no logos, no brand). On the right side of the frame the building ends at a corner, the wall turning away, leaving an open gap where someone could walk out from behind the corner. Trees overhead cast dappled shadows on the ground. Calm, empty, waiting.
Important elements in the upper two thirds; the bottom third is plain concrete walkway with soft shadows.
No people, no figures. No text, no letters, no numbers, no logos, no signage, no watermark. Wide 16:9 landscape.
```
