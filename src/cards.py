"""白板卡片節點：對話卡、變數卡、連線。"""
_x = [0]


def _pos():
    _x[0] += 1
    return {'x': (_x[0] % 8) * 360, 'y': (_x[0] // 8) * 260}


def dialogue(id, title, lines, bg='', start=False, speaker='', actors=None):
    """lines：字串（旁白）或 (講者, 文字)。"""
    dl = []
    for i, l in enumerate(lines):
        sp, tx = (l if isinstance(l, tuple) else (speaker, l))
        dl.append({'id': f'{id}-l{i}', 'speaker': sp, 'text': tx})
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
