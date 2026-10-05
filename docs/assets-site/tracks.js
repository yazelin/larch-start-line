/* 原聲帶七首。scene 照 docs/bgm-prompts.md；line 是那一段的原文（結局 B 那句取自新寫）；
   cover 是曲目封面，slides 是播放時依序換上的背景（照劇情順序）；
   bpm 是生成時提示詞指定的速度，只拿來讓播放器的心跳線跟著打拍子。路徑都相對於 assets/。 */
window.TRACKS = [
  { n: 1, bpm: 72, file: "audio/bgm-01-title.mp3", title: "Slow Light Through Curtains", scene: "標題畫面、序章", dur: 129,
    line: "在槍響之前，在所有裁判與觀眾以為一切正要開始之前，有些事早就已經塵埃落定。",
    cover: "art/cover/cover.webp", pos: "70% 50%", slides: ["art/cover/cover.webp", "art/cards/pace-sky.webp"] },
  { n: 2, bpm: 96, file: "audio/bgm-02-stadium.mp3", title: "Waiting for the Whistle", scene: "第一輪：程徹在田徑場", dur: 172,
    line: "風把她額前的碎髮吹亂，她忽然抬頭，兩人的視線撞在了一起。",
    cover: "art/cg/cg-gaze.webp", pos: "40% 50%", slides: ["art/maps/stadium.webp", "art/cg/cg-gaze.webp", "art/cg/cg-vending.webp"] },
  { n: 3, bpm: 92, file: "audio/bgm-03-race.mp3", title: "Final Straightaway", scene: "配速卡：八百公尺", dur: 167,
    line: "那場比賽他拿了小組第一，衝過終點線時他沒有看計時板。",
    cover: "art/cg/cg-finish.webp", pos: "30% 40%", slides: ["art/cards/start-pov.webp", "art/cards/pace-eyes.webp", "art/cg/cg-finish.webp"] },
  { n: 4, bpm: 80, file: "audio/bgm-04-seawall.mp3", title: "Unsent at the Seawall", scene: "中章、訊息草稿、花蓮防波堤", dur: 123,
    line: "「你記得我們第一次說話是什麼時候嗎？」",
    cover: "art/cg/cg-seawall.webp", pos: "45% 50%", slides: ["art/cg/cg-seawall.webp"] },
  { n: 5, bpm: 100, file: "audio/bgm-05-her-side.mp3", title: "Sunday Morning Mischief", scene: "第二輪：林向晚那一邊、零錢卡", dur: 124,
    line: "我算了你的時間，知道你習慣比完賽去那台販賣機買水。",
    cover: "art/cards/lin-avatar.webp", pos: "50% 40%", slides: ["art/maps/stadium.webp", "art/cards/coin-bg.webp", "art/cg/cg-vending.webp"] },
  { n: 6, bpm: 66, file: "audio/bgm-06-ending-a.mp3", title: "Tea and Midnight Rain", scene: "結局 A：防波堤後半、台北廚房", dur: 172,
    line: "窗外的雨聲細碎，像極了多年前田徑場上細碎的風聲。",
    cover: "art/cg/cg-kitchen.webp", pos: "50% 35%", slides: ["art/cg/cg-seawall.webp", "art/cg/cg-kitchen-backhug.webp", "art/cg/cg-kitchen.webp"] },
  { n: 7, bpm: 60, file: "audio/bgm-07-ending-b.mp3", title: "Weight of an Empty Chair", scene: "結局 B", dur: 93,
    line: "她一直很自由，自由到始終沒有起跑。",
    cover: "art/cards/coin-bg.webp", pos: "62% 50%", slides: ["art/cards/coin-bg.webp", "art/cards/pace-sky.webp"] }
];
