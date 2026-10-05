"""靜態檢查：不用開瀏覽器。python3 tests/check_static.py"""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import text

TESTS = []
def test(f): TESTS.append(f); return f

@test
def para_range():
    ps = text.para('在槍響之前', '所謂的起跑')
    assert len(ps) == 2 and ps[0].startswith('在槍響之前'), ps

@test
def para_missing_raises():
    try: text.para('不存在的句子', '所謂的起跑')
    except KeyError: return
    raise AssertionError('找不到段落應該 raise KeyError')

@test
def new_section():
    assert text.new('備用鑰匙說明') == '把自己的門，交給另一個人。'
    assert text.lines('想法選項') == ['我要贏', '配速', '等跑完，我要去認識她']

@test
def every_original_para_used():
    import build
    blob = json.dumps(build.build(), ensure_ascii=False)
    missing = [s[:24] for s in text.all_paras() if s[:24] not in blob]
    assert not missing, '原文沒放進遊戲的段落：' + ' / '.join(missing)

def gate_problems(card_html, read, write):
    sets = set(re.findall(r"L\.set\('(\w+)'", card_html))
    gets = set(re.findall(r"L\.get\('(\w+)'", card_html))
    return sorted(f'寫 {n} 不在 write 名單' for n in sets - set(write)) + sorted(f'讀 {n} 不在 read 名單' for n in gets - set(read))

@test
def gate_checker_catches_missing():
    probs = gate_problems("L.set('a',1);L.set('b',2);L.get('c')", read=[], write=['a'])
    assert probs == ['寫 b 不在 write 名單', '讀 c 不在 read 名單'], probs

@test
def plugin_variable_gate():
    import plugin, variables
    for cid, c in plugin.CARDS.items():
        probs = gate_problems(plugin.html(cid), c['read'], c['write'])
        assert not probs, f'{cid}: {probs}'
        unknown = [n for n in c['read'] + c['write'] if n not in variables.VARS]
        assert not unknown, f'{cid}: 變數表沒有 {unknown}'
    assert set(plugin.HUD['readVariables']) <= set(variables.VARS)

def _maps():
    import build
    p = build.build()
    out = []
    for n in p['boards'][0]['nodes']:
        if n['data'].get('pluginCardId') == 'map':
            out.append((n, json.loads(n['data']['pluginValues']['map'])))
    return p, out

def _walls(m):
    W = m['width']; cells = set()
    for L in m['layers']:
        if L.get('collision'):
            cells |= {(i % W, i // W) for i, t in enumerate(L['tiles']) if t}
    return cells

def _event_conds(e):
    yield from e.get('conditions', [])
    for pg in e.get('pages', []): yield from pg.get('conditions', [])

def _all_actions(e):
    def walk(acts):
        for a in acts:
            yield a
            for o in (a.get('choice') or {}).get('options', []): yield from walk(o.get('actions', []))
    yield from walk(e.get('actions', []))
    for pg in e.get('pages', []): yield from walk(pg.get('actions', []))

@test
def maps_exist():
    _, ms = _maps()
    assert ms, '還沒有地圖卡'

@test
def map_events_wellformed():
    _, ms = _maps()
    for n, m in ms:
        seen = {}
        walls = _walls(m)
        for e in m['events']:
            assert e.get('sprite'), f"{n['id']}/{e['id']} 沒有 sprite"
            c = (e['x'], e['y'])
            if e.get('environment') is None and m.get('environment'):
                env = m['environment']
                for k in ('intensity', 'darkness', 'shake'): assert k in env, f"{n['id']} environment 少了 {k}"
                assert isinstance(m['picture']['url'], str) and m['picture']['url'].startswith(('/', 'https://')), f"{n['id']} 底圖網址要 / 或 https 開頭"
            assert c not in seen, f"{n['id']}: {e['id']} 跟 {seen.get(c)} 同格 {c}"
            seen[c] = e['id']
            assert c not in walls, f"{n['id']}/{e['id']} 在牆上 {c}"
            assert 0 <= e['x'] < m['width'] and 0 <= e['y'] < m['height'], f"{e['id']} 出界"
            for a in _all_actions(e):
                sp = a.get('speaker')
                if a['kind'] == 'dialogue' and sp not in (None, '', 'player', 'narrator') and not re.match(r'(party|event):', sp):
                    raise AssertionError(f"{e['id']} 對話說話者 {sp!r} 不合法（只能 ''/player/narrator/party:id/event:id）")
                if a['kind'] == 'screen': assert isinstance(a.get('screen'), dict), f"{e['id']} screen 參數沒包在 screen:{{}}"
        assert isinstance(m.get('guidance'), list), f"{n['id']} guidance 不能是 null"
        ids = {e['id'] for e in m['events']}
        for g in m['guidance']:
            assert g['eventId'] in ids, f"{n['id']} 任務提示指向不存在的事件 {g['eventId']}"

@test
def map_events_reachable():
    _, ms = _maps()
    for n, m in ms:
        walls = _walls(m); W, H = m['width'], m['height']
        hero = next(e for e in m['events'] if e['actor'] == 'player')
        seen, q = {(hero['x'], hero['y'])}, [(hero['x'], hero['y'])]
        while q:
            x, y = q.pop()
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in walls and (nx, ny) not in seen:
                    seen.add((nx, ny)); q.append((nx, ny))
        for e in m['events']:
            if e['sprite'].get('url') == '' and e['trigger'] in ('auto', 'condition', 'parallel'): continue
            near = {(e['x'], e['y']), (e['x']+1, e['y']), (e['x']-1, e['y']), (e['x'], e['y']+1), (e['x'], e['y']-1)}
            assert near & seen, f"{n['id']}/{e['id']} 從起點走不到 ({e['x']},{e['y']})"

@test
def map_variable_gate():
    import variables
    _, ms = _maps()
    for n, m in ms:
        used = set()
        for e in m['events']:
            used |= {c['variable'] for c in _event_conds(e) if c.get('kind') == 'variable'}
            used |= {a['variable'] for a in _all_actions(e) if a['kind'] == 'variable'}
        reads, writes = set(n['data']['pluginReadVars']), set(n['data']['pluginWriteVars'])
        assert used <= reads and used <= writes, f"{n['id']} 讀寫名單漏了 {sorted(used - (reads & writes))}"
        assert used <= set(variables.VARS), f"{n['id']} 變數表沒有 {sorted(used - set(variables.VARS))}"

@test
def flow_reachable():
    p, ms = _maps()
    b = p['boards'][0]
    nodes = {n['id'] for n in b['nodes']}
    out = {i: set() for i in nodes}
    for e in b['edges']: out[e['source']].add(e['target'])
    for n, m in ms:
        for e in m['events']:
            for a in _all_actions(e):
                if a.get('cardId') and not a['cardId'].startswith('monsters:'): out[n['id']].add(a['cardId'])
    for t in sum(map(list, out.values()), []): assert t in nodes, f'指向不存在的卡 {t}'
    start = [n['id'] for n in b['nodes'] if n['data'].get('start')]
    assert start == ['prologue'], start
    seen, q = set(start), list(start)
    while q:
        for t in out[q.pop()]:
            if t not in seen: seen.add(t); q.append(t)
    assert nodes <= seen, f'走不到的卡：{sorted(nodes - seen)}'
    for must in ('ending-b', 'fin', 'm-kitchen', 'c-coin', 'c-notebook'):
        assert must in nodes, f'少了 {must}'

def _holds(c, st):
    import variables
    v = st.get(c['variable'], variables.VARS.get(c['variable'], ('', ''))[1])
    v = str(v).lower() if isinstance(v, bool) else str(v)
    op = c.get('op', 'eq')
    if op in ('gte', 'lte'):
        a, b = float(v or 0), float(c['value'])
        return a >= b if op == 'gte' else a <= b
    return (v == c['value']) if op == 'eq' else (v != c['value'])

def _active(e, st):
    """回傳此狀態下事件生效的分頁（最後一個條件全成立的），都不成立回 None。"""
    act = e if all(_holds(c, st) for c in e.get('conditions', [])) else None
    for pg in e.get('pages', []):
        if all(_holds(c, st) for c in pg['conditions']): act = pg
    return act

def _jumps(acts):
    for a in acts:
        if a['kind'] == 'jump': yield a['cardId']
        for o in (a.get('choice') or {}).get('options', []): yield from _jumps(o.get('actions', []))

@test
def card_reentry_after_unfinished():
    """地圖跳去插件卡、卡片沒玩完就讀檔回地圖時，地圖上要還有事件能再進那張卡。"""
    import plugin
    p, ms = _maps()
    cardset = set(plugin.NODE.values())
    for n, m in ms:
        for e in m['events']:
            for pg in [e] + e.get('pages', []):
                def walk(acts, st):
                    for a in acts:
                        if a['kind'] == 'variable' and not a.get('op'): st = dict(st, **{a['variable']: a['value']})
                        if a['kind'] == 'jump' and a['cardId'] in cardset:
                            # 跳卡當下的狀態：這張卡的條件＋跳之前寫的變數
                            ok = any(_active(e2, st) and a['cardId'] in set(_jumps(_active(e2, st).get('actions', []))) for e2 in m['events'])
                            assert ok, f"{n['id']}/{e['id']}：玩到 {a['cardId']} 一半讀檔回地圖，沒有事件能再進去（狀態 {st}）"
                        for o in (a.get('choice') or {}).get('options', []): walk(o.get('actions', []), dict(st))
                base = {c['variable']: c['value'] for c in pg.get('conditions', []) if c.get('op', 'eq') == 'eq'}
                walk(pg.get('actions', []), base)

@test
def caught_is_not_a_shortcut():
    import map_stadium as S
    p, ms = _maps()
    m = dict(ms)[next(n for n, _ in ms if n['id'] == S.MAP_ID)] if False else next(mm for n, mm in ms if n['id'] == S.MAP_ID)
    for e in m['events']:
        if e['id'].startswith('seen'):
            arr = next(a['arrive'] for a in e['actions'] if a['kind'] == 'jump')
            d = abs(arr['x'] - S.PEEK[0]) + abs(arr['y'] - S.PEEK[1])
            assert d > 5, f"被看到後落在 {arr}，離目標只有 {d} 格"

@test
def ending_b_close_has_no_kitchen():
    import art
    p, ms = _maps()
    nodes = {n['id']: n for n in p['boards'][0]['nodes']}
    for n, m in ms:
        for e in m['events']:
            if e['id'] == 'ending-b-menu':
                ch = next(a for a in e['actions'] if a['kind'] == 'choice')
                stop = [o for o in ch['choice']['options'] if o['id'] == 'stop'][0]
                cid = next(_jumps(stop['actions']))
                bg = nodes[cid]['data'].get('background', '')
                assert 'kitchen' not in bg, f'結局 B 收尾卡用了廚房圖 {bg}'

def _event(map_id, eid):
    p, ms = _maps()
    m = next(mm for n, mm in ms if n['id'] == map_id)
    return m, next(e for e in m['events'] if e['id'] == eid)

@test
def pocari_given_once():
    m, coins = _event('m-stadium', 'coins')
    v2 = next(pg for pg in coins['pages'] if pg['id'] == 'vending2')
    top = [a for a in v2['actions'] if a['kind'] == 'item' and a['itemId'] == 'pocari']
    assert not top, '每次進販賣機分頁就給一瓶寶礦力，B→A 會拿兩瓶'

@test
def flags_set_before_performance():
    for eid, var in [('gaze0', 'gaze_seen')]:   # race-done 不列：地圖演出中無法存檔，且先寫 phase 會讓看台上的她提早消失
        m, e = _event('m-stadium', eid)
        first = next(i for i, a in enumerate(e['actions']) if a['kind'] in ('dialogue', 'camera', 'move'))
        flag = next(i for i, a in enumerate(e['actions']) if a['kind'] == 'variable' and a['variable'] == var)
        assert flag < first, f'{eid}：{var} 在演出之後才寫，演出中讀檔會重演'

@test
def midstory_reload_returns_to_mid():
    """在中章／草稿／防波堤讀檔回到田徑場時（phase=mid），要回到中章，不能直接換人。"""
    m, sw = _event('m-stadium', 'switch')
    assert {'variable': 'phase', 'value': 'mid'} not in [{'variable': c['variable'], 'value': c['value']} for c in sw['conditions']], 'switch 在 phase=mid 就換人'
    st = {'round': '1', 'phase': 'mid'}
    assert any(_active(e, st) and 'mid' in set(_jumps(_active(e, st).get('actions', []))) for e in m['events']), 'phase=mid 回到地圖沒有事件帶回中章'

@test
def nobody_tags_along():
    """兩輪都只有一個人在走：資料庫角色不能自動入隊跟隨（role=party 又沒有 joinVariable 會自動跟著走）。"""
    import build
    db = json.loads(build.build()['settings']['plugins']['larch-rpg-system']['settings']['database'])
    for a in db['actors']:
        assert a.get('join') == 'later' or a.get('role') != 'party' or a.get('joinVariable'), f"{a['id']} 會自動跟在主角身邊"

@test
def kitchen_uses_adult_clothes():
    """台北廚房是幾年後：兩人都不能還穿田徑隊服。"""
    import build, art
    a = art.FILES
    m, intro = _event('m-kitchen', 'k-intro')
    heroes = [x['value'] for x in intro['actions'] if x['kind'] == 'hero']
    assert heroes == ['chengche-adult'], f'廚房換成的主角是 {heroes}'
    lin = next(e for e in m['events'] if e['id'] == 'lin-k')
    assert 'adult' in lin['sprite']['url'], f"廚房的林向晚走路圖是 {lin['sprite']['url']}"
    db = json.loads(build.build()['settings']['plugins']['larch-rpg-system']['settings']['database'])
    adult = next(x for x in db['actors'] if x['id'] == 'chengche-adult')
    assert 'adult' in adult['walk']['url'] and adult.get('join') == 'later', adult

def _route_cells(start, route):
    x, y = start; cells = []
    for leg in route:
        dx, dy = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}[leg['dir']]
        for _ in range(leg['steps']): x += dx; y += dy; cells.append((x, y))
    return cells

@test
def race_runs_a_full_lap():
    import map_stadium as S
    for eid, start in [('race-done', S.START_LINE), ('race2-run', S.CHE_RACE)]:
        m, e = _event('m-stadium', eid)
        mv = next(a for a in e['actions'] if a['kind'] == 'move')
        cells = _route_cells(start, mv['move']['route'])
        assert len(mv['move']['route']) <= 8 and all(l['steps'] <= 20 for l in mv['move']['route']), '路線超過 8 段或單段超過 20 格'
        assert len(cells) >= 80, f'{eid} 只跑了 {len(cells)} 格，不像一圈'
        assert cells[-1] == S.FINISH, f'{eid} 停在 {cells[-1]}，不是終點'
        bad = [c for c in cells if S.cell(*c) not in ('track', 'line')]
        assert not bad, f'{eid} 跑出跑道：{bad[:3]}'
        assert S.START_LINE not in cells, f'{eid} 經過起跑線事件格，會再觸發起跑卡'

@test
def nameplates_are_real_names():
    """地圖對話說話者留空＝事件自己講話，名牌顯示事件名稱，所以事件名稱不能是程式代號。"""
    p, ms = _maps()
    for n, m in ms:
        for e in m['events']:
            for a in _all_actions(e):
                if a['kind'] == 'dialogue' and not a.get('cardId') and a.get('speaker', '') == '':
                    assert re.search(r'[\u4e00-\u9fff]', e.get('name', '')), f"{e['id']} 的台詞名牌會顯示「{e.get('name')}」"

@test
def spare_key_is_played():
    """備用鑰匙要玩家自己掛上門邊，掛完才能去求婚。"""
    m, intro = _event('m-kitchen', 'k-intro')
    assert any(a['kind'] == 'item' and a['itemId'] == 'key' for a in intro['actions']), '進廚房時背包裡要有備用鑰匙'
    assert any(a['kind'] == 'variable' and a['variable'] == 'phase' and a['value'] == 'key' for a in intro['actions'])
    _, hook = _event('m-kitchen', 'key-hook')
    assert any(a['kind'] == 'removeItem' and a['itemId'] == 'key' for a in hook['actions']), '掛勾要把鑰匙從背包拿走'
    assert [a['value'] for a in hook['actions'] if a['kind'] == 'variable' and a['variable'] == 'phase'] == ['kitchen']
    _, hug = _event('m-kitchen', 'hug')
    assert {'variable': 'phase', 'value': 'kitchen'} in [{'variable': c['variable'], 'value': c['value']} for c in hug['conditions']]
    assert not any(a['kind'] == 'item' and a['itemId'] == 'key' for a in hug['actions']), '求婚後不要再給一次鑰匙'
    assert [g['eventId'] for g in m['guidance']] == ['key-hook', 'hug']

@test
def race2_camera_truly_follows():
    """第二輪看他比賽：鏡頭只會跟主角，所以比賽時把主角暫時換成程徹去跑，跑完換回林向晚、回到看台。"""
    import map_stadium as S
    m, start = _event('m-stadium', 'race2-start')
    assert [a['value'] for a in start['actions'] if a['kind'] == 'hero'] == ['chengche']
    assert [a['value'] for a in start['actions'] if a['kind'] == 'variable' and a['variable'] == 'phase'] == ['race2b'], '換成程徹之前就要切到 race2b，重新載入時看台上的她才會出現'
    _, run = _event('m-stadium', 'race2-run')
    mv = next(a for a in run['actions'] if a['kind'] == 'move')
    assert mv['move']['who'] == 'player', '要讓主角（程徹）跑，鏡頭才會跟'
    assert [a['value'] for a in run['actions'] if a['kind'] == 'hero'] == ['xiangwan'], '跑完要換回林向晚'
    lin = next(e for e in m['events'] if (e['x'], e['y']) == S.STANDS_SEAT)
    assert any(any(c['variable'] == 'phase' and c['value'] == 'race2b' for c in pg['conditions']) and pg.get('actor') == 'npc' for pg in lin.get('pages', [])), '他跑的時候看台上要有林向晚'

@test
def start_and_finish_are_labeled():
    import map_stadium as S
    p, ms = _maps()
    m = next(mm for n, mm in ms if n['id'] == S.MAP_ID)
    at = {(e['x'], e['y']): e for e in m['events']}
    for cell, word in [(S.START_LINE, '起跑'), (S.FINISH, '終點')]:
        e = at.get(cell)
        assert e and word in (e.get('marker') or {}).get('label', ''), f'{cell} 沒有「{word}」標示'

@test
def every_goal_is_labeled():
    """任務提示指過去的地方都要有名牌，玩家才知道要走去哪。"""
    p, ms = _maps()
    for n, m in ms:
        by = {e['id']: e for e in m['events']}
        for g in m['guidance']:
            mk = by[g['eventId']].get('marker') or {}
            assert mk.get('label'), f"{n['id']}：任務「{g['text']}」指向的 {g['eventId']} 沒有名牌"

@test
def stairs_hint_in_round2():
    import map_stadium as S
    p, ms = _maps()
    m = next(mm for n, mm in ms if n['id'] == S.MAP_ID)
    hints = [e for e in m['events'] if e['id'].startswith('stairs-hint')]
    assert len(hints) == 2 and all('看台後方' in e['marker']['label'] for e in hints), '兩個樓梯口要有「往看台後方」提示'

@test
def round2_has_her_music():
    m, e = _event('m-stadium', 'r2-music')
    assert e['trigger'] == 'auto' and {'variable': 'round', 'value': '2'} in [{'variable': c['variable'], 'value': c['value']} for c in e['conditions']]
    mu = next(a for a in e['actions'] if a['kind'] == 'music')
    assert 'bgm-05' in mu['audio']['url'] and mu['audio'].get('loop'), mu

@test
def round2_inner_voice_with_faces():
    """第二輪三個時刻用她自己的口吻，配表情立繪。"""
    p, ms = _maps()
    nodes = {n['id']: n for n in p['boards'][0]['nodes']}
    for eid, card_id, face in [('peek', 'r2-peek', 'lin-hs-shy'), ('seen13', 'r2-caught', 'lin-hs-flustered'), ('race2-after', 'r2-watch-distracted', 'lin-hs-shy'), ('race2-after', 'r2-watch-steady', 'lin-hs-shy')]:
        m, e = _event('m-stadium', eid)
        d = next(a for pg in [e] + e.get('pages', []) for a in pg['actions'] if a['kind'] == 'dialogue' and a.get('cardId') == card_id)
        assert d.get('presentation') == 'portrait', f'{eid} 要用立繪呈現'
        data = nodes[card_id]['data']
        assert any(l['speaker'] == '林向晚' for l in data['dialogueLines']), f'{card_id} 要有她自己說的話'
        assert any(face in a['url'] and a['name'] == '林向晚' for a in data['stage']['actors']), f'{card_id} 立繪要是 {face}'

@test
def race_watch_echoes_round1():
    """第二輪看他比賽的那句，跟著第一輪配速分數變：高分＝跑得好穩，低分＝一直在分心。"""
    m, e = _event('m-stadium', 'race2-after')
    base = {'round': '2', 'phase': 'race2c'}
    pick = lambda score: next(a['cardId'] for a in _active(e, dict(base, pace_score=str(score)))['actions'] if a['kind'] == 'dialogue')
    assert pick(30) == 'r2-watch-steady' and pick(3) == 'r2-watch-distracted', (pick(30), pick(3))

@test
def vending_choice_not_eaten_by_enter():
    """按 Enter 互動的那一下不能直接選掉選項：販賣機分支的選項前要先有一句要按的對話。"""
    m, e = _event('m-stadium', 'coins')
    v2 = next(pg for pg in e['pages'] if pg['id'] == 'vending2')
    kinds = [a['kind'] for a in v2['actions']]
    assert kinds.index('dialogue') < kinds.index('choice'), kinds

@test
def ending_a_goes_to_site_chapter():
    """結局 A 演完自動進第二章（內嵌公開站）。"""
    import build
    p = build.build()
    assert len(p['boards']) == 2, '要有第二章白板'
    ch2 = p['boards'][1]
    site = next(n for n in ch2['nodes'] if n['data'].get('type') == 'miniGame')
    assert 'yazelin.github.io/larch-start-line' in site['data']['miniGameHtml'] and site['data'].get('start'), '第二章要內嵌公開站'
    b0 = p['boards'][0]
    nxt = [e['target'] for e in b0['edges'] if e['source'] == 'fin']
    assert nxt, '「完」之後要接跳章卡'
    j = next(n for n in b0['nodes'] if n['id'] == 'to-site')['data']
    assert j['type'] == 'boardJump' and j['jumpBoardId'] == ch2['id'] and j['jumpNodeId'] == site['id'], j
    assert not [e for e in b0['edges'] if e['source'] == 'fin-b'], '結局 B 不接第二章'
    path = ['fin']
    while path[-1] != 'to-site':
        path.append(next(e['target'] for e in b0['edges'] if e['source'] == path[-1]))
    ops = [o for nid in path for o in (next(n for n in b0['nodes'] if n['id'] == nid)['data'].get('variableOps') or [])]
    assert {'variable': 'bpm', 'value': '0'} in [{'variable': o['variable'], 'value': o['value']} for o in ops], '進第二章前要把心跳歸零，HUD 才不會擋住公開站'

@test
def cg_gallery_only_real_cgs():
    """CG 收藏只放遊戲裡實際演出的 CG（＋封面），不能混進走路圖、立繪、卡片背景。"""
    import build
    st = build.build()['settings']
    assert st.get('cgGallerySource') == 'picked', 'CG 收藏要用挑選模式'
    urls = [i['url'] for i in st['cgGalleryItems']]
    assert len(urls) == 7 and all(('/cg/cg-' in u) or ('/cover/' in u) for u in urls), urls
    assert all(i.get('title') for i in st['cgGalleryItems'])

@test
def stairs_reachable_from_the_side():
    """看台前那排只有他正前方會被看到；樓梯口兩側要能橫著走過去，不必從跑道正下方直上。"""
    import map_stadium as S
    p, ms = _maps()
    m = next(mm for n, mm in ms if n['id'] == S.MAP_ID)
    seen = {(e['x'], e['y']) for e in m['events'] if e['id'].startswith('seen')}
    for sx in sorted(S.STAIR_XS):
        for dx in (-2, -1, 1, 2):
            assert (sx + dx, 5) not in seen, f'樓梯口 x={sx} 旁邊 ({sx + dx},5) 會被看到，從側面走不過去'
    assert seen and all(13 <= x <= 26 for x, _ in seen), sorted(seen)

if __name__ == '__main__':
    only = sys.argv[1:]
    bad = 0
    for f in TESTS:
        if only and f.__name__ not in only: continue
        try: f(); print('ok  ', f.__name__)
        except Exception as e: bad += 1; print('FAIL', f.__name__, '-', type(e).__name__, e)
    sys.exit(1 if bad else 0)
