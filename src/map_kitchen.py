"""台北的小廚房：結局 A。"""
from mapkit import *
from text import para, new

W, H = 12, 9
MAP_ID = 'm-kitchen'
HERO_START = (6, 7)
LIN = (6, 3)        # 爐前
HUG = (6, 4)        # 她身後
HOOK = (10, 6)      # 門邊掛勾（右側牆邊）


def cell(x, y):
    if x in (0, W - 1) or y in (0, H - 1): return 'wall'
    if y in (1, 2): return 'counter'       # 流理台、爐子、窗
    if 1 <= x <= 2 and 5 <= y <= 7: return 'table'
    return 'floor'


def walls():
    return {(x, y) for x in range(W) for y in range(H) if cell(x, y) in ('wall', 'counter', 'table')}


def build_kitchen(art):
    events = [
        ev('hero', *HERO_START, actor='player', direction='up', sprite=walker(art['walk-cheng-adult']), actorId='chengche-adult'),
        ev('k-intro', 10, 7, trigger='auto', once=True,
           actions=[A('hero', value='chengche-adult'), item('key', '備用鑰匙'), say(new('鑰匙由來')), setv('bpm', 80), setv('phase', 'key')]),
        # 他把備用鑰匙掛上門邊：自己選來交給她的限制
        ev('key-hook', *HOOK, name='門邊掛勾', conditions=[cond('phase', 'key')], marker={'label': '門邊掛勾', 'kind': 'quest'},
           actions=[remove('key', '備用鑰匙'), say(new('掛鑰匙')), say(new('備用鑰匙說明')), setv('phase', 'kitchen')]),
        npc('lin-k', *LIN, walker(art['walk-lin-adult']), direction='up'),
        ev('hug', *HUG, trigger='touch', conditions=[cond('phase', 'kitchen')], marker={'label': '她身後', 'kind': 'quest'},
           actions=[setv('phase', 'proposal'), setv('bpm', 72), card('kitchen'), card('kitchen-2'), jump('fin')]),
    ]
    guidance = [{'text': '把備用鑰匙掛到門邊', 'eventId': 'key-hook', 'conditions': [cond('phase', 'key')]},
                {'text': '走到她身後', 'eventId': 'hug', 'conditions': [cond('phase', 'kitchen')]}]
    env = {'weather': 'rain', 'intensity': 0.35, 'darkness': 0.45, 'shake': 0, 'fog': {'density': 0.25, 'color': '#dfe6ee'},
           'lights': [{'id': 'stove', 'x': LIN[0], 'y': 2, 'radius': 3.5, 'color': '#ffcf8a', 'flicker': True}],
           'ambience': {'particles': 'none', 'vignette': 0.3}}
    m = map_dict('台北的小廚房', W, H, art['kitchen'], walls(), events, guidance, env)
    return map_node(MAP_ID, '台北的小廚房', m, bgm=art.get('bgm-06', ''))
