"""台北的小廚房：結局 A。"""
from mapkit import *
from text import para, new

W, H = 12, 9
MAP_ID = 'm-kitchen'
HERO_START = (6, 7)
LIN = (6, 3)        # 爐前
HUG = (6, 4)        # 她身後


def cell(x, y):
    if x in (0, W - 1) or y in (0, H - 1): return 'wall'
    if y in (1, 2): return 'counter'       # 流理台、爐子、窗
    if 1 <= x <= 2 and 5 <= y <= 7: return 'table'
    return 'floor'


def walls():
    return {(x, y) for x in range(W) for y in range(H) if cell(x, y) in ('wall', 'counter', 'table')}


def build_kitchen(art):
    events = [
        ev('hero', *HERO_START, actor='player', direction='up', sprite=walker(art['walk-cheng']), actorId='chengche'),
        ev('k-intro', 10, 7, trigger='auto', once=True,
           actions=[A('hero', value='chengche'), setv('phase', 'kitchen'), setv('bpm', 80)]),
        npc('lin-k', *LIN, walker(art['walk-lin']), direction='up'),
        ev('hug', *HUG, trigger='touch', conditions=[cond('phase', 'kitchen')],
           actions=[setv('phase', 'proposal'), setv('bpm', 72), card('kitchen'), item('key', '備用鑰匙'), say(new('備用鑰匙說明')), jump('fin')]),
    ]
    guidance = [{'text': '走到她身後', 'eventId': 'hug', 'conditions': [cond('phase', 'kitchen')]}]
    env = {'weather': 'rain', 'intensity': 0.35, 'darkness': 0.45, 'shake': 0, 'fog': {'density': 0.25, 'color': '#dfe6ee'},
           'lights': [{'id': 'stove', 'x': LIN[0], 'y': 2, 'radius': 3.5, 'color': '#ffcf8a', 'flicker': True}],
           'ambience': {'particles': 'none', 'vignette': 0.3}}
    m = map_dict('台北的小廚房', W, H, art['kitchen'], walls(), events, guidance, env)
    return map_node(MAP_ID, '台北的小廚房', m)
