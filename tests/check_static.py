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
    return (v == c['value']) if c.get('op', 'eq') == 'eq' else (v != c['value'])

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
                stop = [o for o in e['actions'][0]['choice']['options'] if o['id'] == 'stop'][0]
                cid = next(_jumps(stop['actions']))
                bg = nodes[cid]['data'].get('background', '')
                assert 'kitchen' not in bg, f'結局 B 收尾卡用了廚房圖 {bg}'

if __name__ == '__main__':
    only = sys.argv[1:]
    bad = 0
    for f in TESTS:
        if only and f.__name__ not in only: continue
        try: f(); print('ok  ', f.__name__)
        except Exception as e: bad += 1; print('FAIL', f.__name__, '-', type(e).__name__, e)
    sys.exit(1 if bad else 0)
