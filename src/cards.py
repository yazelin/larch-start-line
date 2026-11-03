"""白板卡片節點：對話卡、變數卡、連線。"""
_x = [0]


def _pos():
    _x[0] += 1
    return {'x': (_x[0] % 8) * 360, 'y': (_x[0] // 8) * 260}


LONG = 100   # 超過這個字數的一段折成四五行，會把對話框撐高、蓋住 CG（作者 2026-11-03）


def split_long(tx):
    """太長的一段在最靠近中間的句號切成兩頁；字一個不改，接回去要跟原文一樣。"""
    if len(tx) <= LONG: return [tx]
    cuts = [i + 1 + (tx[i + 1:i + 2] == '」') for i, ch in enumerate(tx) if ch == '。' and i + 1 < len(tx)]
    cuts = [c for c in cuts if 15 <= c <= len(tx) - 15]
    if not cuts: return [tx]
    c = min(cuts, key=lambda c: abs(c - len(tx) / 2))
    parts = split_long(tx[:c]) + split_long(tx[c:])
    assert ''.join(parts) == tx
    return parts


def dialogue(id, title, lines, bg='', start=False, speaker='', actors=None):
    """lines：字串（旁白）或 (講者, 文字)。太長的一段自動切成兩頁（split_long）。"""
    dl = []
    for l in lines:
        sp, tx = (l if isinstance(l, tuple) else (speaker, l))
        for part in split_long(tx):
            dl.append({'id': f'{id}-l{len(dl)}', 'speaker': sp, 'text': part})
    data = {'type': 'dialogue', 'title': title, 'speaker': dl[0]['speaker'], 'text': dl[0]['text'],
            'dialogueLines': dl, 'stage': {'actors': actors or []}}
    if bg: data['background'] = bg
    if start: data['start'] = True
    return {'id': id, 'type': 'story', 'position': _pos(), 'data': data}


def link(board, a, b):
    board['edges'].append({'id': f'{a}--{b}', 'source': a, 'target': b, 'sourceHandle': 'right', 'targetHandle': 'left'})


def setvar(id, title, ops):
    """設定變數卡：ops = [(變數, 值), ...]"""
    return {'id': id, 'type': 'story', 'position': _pos(), 'data': {
        'type': 'setVariable', 'title': title, 'text': '',
        'variableOps': [{'id': f'{id}-{i}', 'variable': k, 'kind': 'set', 'value': str(v).lower() if isinstance(v, bool) else str(v)} for i, (k, v) in enumerate(ops)]}}


def actor(name, url, slot='center'):
    """舞台立繪：名字要跟台詞的說話者一致，播放器才會在那句顯示這張立繪。"""
    return {'id': f'actor-{name}', 'name': name, 'url': url, 'slot': slot, 'offsetX': 0, 'offsetY': 0, 'scale': 1}
