"""田徑場地圖：兩輪共用。配置（哪格是什麼）只在 cell() 定義，底圖、碰撞格、驗收都從這裡來。"""
from mapkit import *
from text import para, new
import plugin

W, H = 40, 30
MAP_ID = 'm-stadium'
# 地點
HERO_START = (6, 28)
CLERK = (6, 25)          # 檢錄處（帳篷前）
BOARD = (8, 27)          # 秩序冊公告欄
GAZE = [(13, 25), (14, 25), (15, 25)]   # 終點線後方
LIN_FINISH = (14, 24)
FINISH = (14, 22)
START_LINE = (24, 22)    # 八百公尺起跑線
STANDS_SEAT = (29, 5)    # 看台階梯口（她坐的位置）
VENDING = (33, 26)       # 販賣機（牆）
COINS = (32, 26)         # 販賣機前
LIN_VENDING = (31, 27)
MATE = (10, 13)


def cell(x, y):
    """回傳這格的種類：wall/stand/tent/gym/vending/track/line/grass/corridor"""
    if x in (0, W - 1) or y in (0, H - 1): return 'wall'
    if y == 1: return 'corridor'                      # 看台後方通道
    if 2 <= y <= 4 and 6 <= x <= 33 and x not in (10, 29): return 'stand'
    if 1 <= x <= 4 and 24 <= y <= 27: return 'tent'
    if 34 <= x <= 38 and 23 <= y <= 28: return 'gym'
    if (x, y) == VENDING: return 'vending'
    outer = 3 <= x <= 36 and 6 <= y <= 23
    inner = 7 <= x <= 32 and 10 <= y <= 19
    if outer and not inner:
        if (x == FINISH[0] or x == START_LINE[0]) and 20 <= y <= 23: return 'line'
        return 'track'
    return 'grass'


WALL_KINDS = {'wall', 'stand', 'tent', 'gym', 'vending'}


def walls():
    return {(x, y) for x in range(W) for y in range(H) if cell(x, y) in WALL_KINDS}


R1 = cond('round', 1)


def round1_events(art):
    lin = walker(art['walk-lin'])
    ev_list = [
        ev('hero', *HERO_START, actor='player', direction='up', sprite=walker(art['walk-cheng']), actorId='chengche'),
        ev('r1-intro', 1, 28, trigger='auto', once=True, conditions=[R1, cond('phase', '')],
           actions=[setv('bpm', 96), setv('phase', 'bib')]),
        npc('clerk', *CLERK, walker(art['walk-judge']), conditions=[R1, cond('phase', 'bib')],
            actions=[say(new('檢錄'), speaker=''), item('bib', '號碼布'), item('pin', '別針'), setv('phase', 'start')],
            pages=[page('clerk-after', [cond('phase', 'bib', 'neq')], [], actor='npc', sprite=walker(art['walk-judge']), solid=True)]),
        npc('mate-r1', *MATE, walker(art['walk-mate']), conditions=[R1], actions=[say(new('隊友第一輪'), speaker='')]),
        npc('lin-finish', *LIN_FINISH, lin, conditions=[R1, cond('gaze_seen', False)], direction='down'),
        npc('lin-stand', *STANDS_SEAT, lin, conditions=[R1, cond('phase', 'start'), cond('pace_score', -1, 'neq')]),
        npc('lin-vending', *LIN_VENDING, lin, conditions=[R1, cond('phase', 'vending')], direction='right'),
    ]
    for i, (x, y) in enumerate(GAZE):
        ev_list.append(ev(f'gaze{i}', x, y, trigger='touch', conditions=[R1, cond('phase', 'start'), cond('gaze_seen', False)],
                          actions=[setv('bpm', 120), balloon('exclamation'), card('gaze'), setv('gaze_seen', True)]))
    ev_list += [
        ev('startline', *START_LINE, trigger='touch', conditions=[R1, cond('phase', 'bib')],
           actions=[say(new('先去檢錄'), speaker=''), move([('up', 1)])],
           pages=[page('startline-early', [R1, cond('phase', 'start'), cond('gaze_seen', False)],
                       [say(new('還沒點名'), speaker=''), move([('up', 1)])], trigger='touch'),
                  page('startline-go', [R1, cond('phase', 'start'), cond('gaze_seen', True)],
                       [jump(plugin.NODE['start-gun'])], trigger='touch')]),
        ev('race-done', 2, 28, trigger='condition', conditions=[R1, cond('phase', 'start'), cond('pace_score', -1, 'neq')],
           actions=[move([('left', START_LINE[0] - FINISH[0])], face='up'), camera(*STANDS_SEAT, hold=1800),
                    card('r1-finish'), setv('bpm', 110), setv('phase', 'vending')]),
        ev('coins', *COINS, conditions=[R1, cond('phase', 'vending')],
           actions=[item('coin10', '十塊錢'), say('妳的十塊錢。', speaker='player'), remove('coin10', '十塊錢'),
                    setv('phase', 'mid'), jump('mid')]),
    ]
    return ev_list


R2 = cond('round', 2)
PEEK = (20, 1)
CHE_WARM = (20, 7)
CHE_RACE = (24, 21)
LIN_R2_START = (14, 24)
STAIRS = (10, 29)


def round2_events(art):
    che = walker(art['walk-cheng'])
    out = [
        # 第一輪結束（販賣機那一下之後回到地圖時）：換成林向晚，回到同一天更早的時間
        ev('switch', 3, 28, trigger='auto', conditions=[cond('phase', 'mid')],
           actions=[setv('round', 2), setv('phase', 'watch'), setv('bpm', 100), A('hero', value='xiangwan'),
                    jump(MAP_ID, arrive={'x': LIN_R2_START[0], 'y': LIN_R2_START[1], 'direction': 'up'})]),
        npc('che-warm', *CHE_WARM, che, conditions=[R2, cond('calc_ok', False)], direction='right'),
        ev('peek', *PEEK, trigger='touch', conditions=[R2, cond('phase', 'watch')],
           actions=[say(new('偷看')), setv('bpm', 110), setv('phase', 'clue')]),
        ev('board', *BOARD, conditions=[R2], actions=[say(new('線索秩序冊')), setv('clue_order', True)]),
        ev('clues-done', 4, 28, trigger='condition',
           conditions=[R2, cond('phase', 'clue'), cond('clue_order', True), cond('clue_mate', True), cond('clue_walk', True)],
           actions=[setv('phase', 'calc'), jump(plugin.NODE['notebook'])]),
        npc('che-race', *CHE_RACE, che, conditions=[R2, cond('phase', 'calc'), cond('calc_ok', True)], direction='left',
            trigger='auto', once=True,
            actions=[camera(*CHE_RACE, hold=600, back=False), move([('left', CHE_RACE[0] - FINISH[0])], who='self', face='up'),
                     balloon('heart', target='player', ms=2200), say(new('看他比賽')), setv('bpm', 140), setv('phase', 'vending2')]),
        ev('ending-b-menu', 5, 28, trigger='condition', conditions=[R2, cond('ending', 'B')],
           actions=[A('choice', text='', choice={'options': [
               {'id': 'again', 'label': new('回到販賣機前'), 'actions': [setv('ending', '')]},
               {'id': 'stop', 'label': new('就到這裡'), 'actions': [jump('fin')]}]})]),
    ]
    # 走出看台的遮蔽（看台前那一排，樓梯口除外）就會被看到
    for x in range(6, 34):
        if x in STAIRS: continue
        out.append(ev(f'seen{x}', x, 5, trigger='touch', conditions=[R2, cond('phase', 'watch')],
                      actions=[balloon('exclamation', target='event', event_id='che-warm'), setv('bpm', 150),
                               say(new('差點被看到')), setv('bpm', 110),
                               jump(MAP_ID, arrive={'x': PEEK[0], 'y': PEEK[1], 'direction': 'down'})]))
    return out


def round2_pages(events, art):
    """第二輪沿用第一輪同一格的事件，用分頁切換。"""
    by = {e['id']: e for e in events}
    mate = walker(art['walk-mate'])
    by['mate-r1']['conditions'] = [R1]
    by['mate-r1']['pages'] = [page('mate-r2', [R2], [say(new('線索隊友'), speaker=''), setv('clue_mate', True)],
                                   actor='npc', sprite=mate, solid=True)]
    by['coins']['pages'] = [
        page('walk-clue', [R2, cond('phase', 'clue'), cond('clue_walk', False)],
             [say(new('線索步行')), setv('clue_walk', True)], trigger='touch'),
        page('too-early', [R2, cond('phase', 'clue'), cond('clue_walk', True)], [say(new('線索不夠'))]),
        page('vending2', [R2, cond('phase', 'vending2'), cond('ending', '')],
             [item('pocari', '寶礦力'), A('choice', text='', choice={'options': [
                 {'id': 'drop', 'label': '讓零錢掉下去', 'actions': [setv('ending', 'A'), jump(plugin.NODE['coin-drop'])]},
                 {'id': 'leave', 'label': '轉身離開', 'actions': [setv('ending', 'B'), jump('ending-b')]}]})]),
    ]


GUIDE_R2 = [
    ('去看台後面', 'peek', [R2, cond('phase', 'watch')]),
    ('看看秩序冊', 'board', [R2, cond('phase', 'clue'), cond('clue_order', False)]),
    ('問問他的隊友', 'mate-r1', [R2, cond('phase', 'clue'), cond('clue_mate', False)]),
    ('自己走一趟體育館後門', 'coins', [R2, cond('phase', 'clue'), cond('clue_walk', False)]),
    ('去體育館後門的販賣機', 'coins', [R2, cond('phase', 'vending2')]),
]


GUIDE_R1 = [
    ('去檢錄處拿號碼布', 'clerk', [R1, cond('phase', 'bib')]),
    ('到終點線那邊', 'gaze1', [R1, cond('phase', 'start'), cond('gaze_seen', False)]),
    ('到八百公尺起跑線', 'startline', [R1, cond('phase', 'start'), cond('gaze_seen', True)]),
    ('去體育館後門的販賣機', 'coins', [R1, cond('phase', 'vending')]),
]


def build_stadium(art):
    events = round1_events(art)
    round2_pages(events, art)
    events += round2_events(art)
    guidance = [{'text': t, 'eventId': e, 'conditions': c} for t, e, c in GUIDE_R1 + GUIDE_R2]
    env = {'weather': 'clear', 'intensity': 0, 'darkness': 0, 'shake': 0, 'lights': [],
           'ambience': {'particles': 'motes', 'density': 0.3, 'rays': 0.35, 'clouds': 0.3}}
    m = map_dict('市運會田徑場', W, H, art['stadium'], walls(), events, guidance, env)
    return map_node(MAP_ID, '田徑場', m)
