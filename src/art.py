"""美術路徑：正式圖在 assets/art/ 就用正式圖，不在就用 assets/placeholder/。本機預覽用 /files/assets/…（serve.py 從 dist/ 提供，build 會把 assets 連過去）；推上平台時 push.py 換成上傳後的網址。"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

# 鍵 → (正式圖, 暫代圖)
FILES = {
    'stadium': ('art/maps/stadium.webp', 'placeholder/stadium.png'),
    'kitchen': ('art/maps/kitchen.webp', 'placeholder/kitchen.png'),
    'walk-cheng': ('art/walk/walk-cheng.png', 'placeholder/walk-cheng.png'),
    'walk-lin': ('art/walk/walk-lin.png', 'placeholder/walk-lin.png'),
    'walk-judge': ('art/walk/walk-judge.png', 'placeholder/walk-judge.png'),
    'walk-mate': ('art/walk/walk-mate.png', 'placeholder/walk-mate.png'),
    'walk-runner': ('art/walk/walk-runner.png', 'placeholder/walk-runner.png'),
    'cg-gaze': ('art/cg/cg-gaze.webp', None), 'cg-finish': ('art/cg/cg-finish.webp', None),
    'cg-vending': ('art/cg/cg-vending.webp', None), 'cg-seawall': ('art/cg/cg-seawall.webp', None),
    'cg-kitchen': ('art/cg/cg-kitchen.webp', None), 'style': ('art/anchors/style-b.webp', None),
    'start-pov': ('art/cards/start-pov.webp', None), 'pace-eyes': ('art/cards/pace-eyes.webp', None),
    'coin-bg': ('art/cards/coin-bg.webp', None),
    'p-cheng': ('art/portraits/cheng-hs-calm.png', None), 'p-lin': ('art/portraits/lin-hs-calm.png', None),
}


def paths():
    out = {}
    for k, (real, ph) in FILES.items():
        if (ROOT / 'assets' / real).exists(): out[k] = '/files/assets/' + real
        elif ph: out[k] = '/files/assets/' + ph
        else: out[k] = ''   # 沒有暫代圖的（CG、卡片背景）缺圖就不放
    return out
