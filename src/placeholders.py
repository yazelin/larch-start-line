"""暫代圖：從地圖配置畫底圖、畫簡單的走路圖。正式美術到位前用。python3 src/placeholders.py"""
import pathlib
from PIL import Image, ImageDraw
import map_stadium as S

OUT = pathlib.Path(__file__).resolve().parent.parent / 'assets/placeholder'
COL = {'wall': '#8a8a80', 'stand': '#b8b0a2', 'tent': '#f0e6c8', 'gym': '#9fb3c2', 'vending': '#4f7fa8', 'track': '#c8584a',
       'line': '#fffaf2', 'grass': '#9cc38a', 'corridor': '#d9cfbf'}


def stadium(tile=48):
    im = Image.new('RGB', (S.W * tile, S.H * tile))
    d = ImageDraw.Draw(im)
    for y in range(S.H):
        for x in range(S.W):
            d.rectangle([x * tile, y * tile, (x + 1) * tile - 1, (y + 1) * tile - 1], fill=COL[S.cell(x, y)])
    im.save(OUT / 'stadium.png')


def walker(name, color):
    im = Image.new('RGBA', (144, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for row in range(4):
        for f in range(3):
            ox, oy = f * 48, row * 64
            d.ellipse([ox + 14, oy + 6, ox + 34, oy + 26], fill='#f2d4b8')           # 頭
            d.rectangle([ox + 12, oy + 26, ox + 36, oy + 48], fill=color)             # 身體
            step = (f - 1) * 4
            d.rectangle([ox + 14 + step, oy + 48, ox + 21 + step, oy + 62], fill='#333')
            d.rectangle([ox + 27 - step, oy + 48, ox + 34 - step, oy + 62], fill='#333')
            # 方向記號：下=眼睛、左/右=一個點偏邊、上=無
            if row == 0: d.point([(ox + 20, oy + 16), (ox + 28, oy + 16)], fill='#000')
            if row == 1: d.ellipse([ox + 14, oy + 14, ox + 18, oy + 18], fill='#000')
            if row == 2: d.ellipse([ox + 30, oy + 14, ox + 34, oy + 18], fill='#000')
    im.save(OUT / f'{name}.png')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    stadium()
    for n, c in [('walk-cheng', '#2f3e7a'), ('walk-lin', '#7a2f4e'), ('walk-judge', '#e8e8e8'), ('walk-mate', '#2f6a7a'), ('walk-runner', '#b02a2a')]:
        walker(n, c)
    print('ok', sorted(p.name for p in OUT.iterdir()))
