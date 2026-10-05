"""自製插件 start-line：一個 HUD＋五張卡。產卡片節點、settings.plugins、manifest 與單卡測試專案。

    python3 src/plugin.py --test <card_id>   # 產 dist/test-<card_id>.json
"""
import json, pathlib, sys, copy
import cards, text, variables
from text import para, new

HERE = pathlib.Path(__file__).resolve().parent / 'plugin'
ROOT = HERE.parent.parent
PLUGIN_ID = 'start-line'
VERSION = '1.0.0'


def _script(card_id):
    if card_id == 'start-gun':
        return {'intro': para('但程徹那天在起跑線上蹲下時', '發令槍響前'), 'marks': para('「各就位。」', '「各就位。」')[0],
                'ready': para('「預備——」', '「預備——」')[0], 'ask': new('想法題目'), 'thoughts': text.lines('想法選項'),
                'fade': new('想法散掉'), 'foul': new('偷跑'), 'bang': new('槍響'),
                'after': para('在那個「預備」的停頓裡', '他的起跑，比發令槍早了')}
    raise KeyError(card_id)


# 卡片：檔名、讀、寫、呈現方式。write 名單少一個名字，larch:set 會被靜默丟掉。
CARDS = {
    'start-gun': {'name': '起跑', 'read': ['bpm', 'fouls'], 'write': ['bpm', 'fouls', 'thought'], 'presentation': 'fullscreen'},
}
HUD = {'id': 'heart', 'title': '心跳', 'anchor': 'top-right', 'width': 132, 'height': 44, 'offsetX': 16, 'offsetY': 16,
       'interactive': False, 'readVariables': ['bpm']}


def html(card_id):
    src = (HERE / f'{card_id}.html').read_text()
    return src.replace('<script src="common.js"></script>', '<script>' + (HERE / 'common.js').read_text() + '</script>')


def card_node(card_id, node_id, values=None):
    c = CARDS[card_id]
    v = {'script': json.dumps(_script(card_id), ensure_ascii=False)}
    v.update(values or {})
    return {'id': node_id, 'type': 'story', 'position': cards._pos(), 'data': {
        'type': 'plugin', 'title': c['name'], 'text': '', 'pluginId': PLUGIN_ID, 'pluginCardId': card_id,
        'pluginName': '起跑總在開始前', 'pluginCardName': c['name'], 'pluginVersion': VERSION, 'pluginIcon': 'timer',
        'pluginColor': '#b23a3a', 'pluginHtml': html(card_id), 'pluginPresentation': c['presentation'],
        'pluginValues': v, 'pluginAssets': [], 'pluginReadVars': list(c['read']), 'pluginWriteVars': list(c['write']),
        'pluginSkippable': False, 'pluginFrame': {'showTitle': False, 'showButton': False}, 'platforms': ['web']}}


def hud_html():
    return (HERE / 'heart.html').read_text()


def settings_entry():
    return {'enabled': True, 'playback': {'version': VERSION, 'permissions': ['player:ui', 'variables:read'], 'defaults': {},
                                          'huds': [dict(HUD, html=hud_html())]}}


def manifest():
    """給 larch_save_plugin_draft 的完整 manifest。"""
    return {'id': PLUGIN_ID, 'name': '起跑總在開始前', 'version': VERSION, 'author': '林亞澤',
            'description': '《起跑總在開始前》專用：心跳 HUD 與起跑、配速、筆記、草稿、零錢五張互動卡。',
            'categories': ['card', 'ui'], 'icon': 'timer',
            'permissions': ['variables:read', 'variables:write', 'assets:read', 'flow:control', 'player:ui'],
            'cards': [{'id': k, 'name': c['name'], 'description': c['name'], 'icon': 'timer', 'color': '#b23a3a',
                       'presentation': c['presentation'],
                       'fields': [{'key': 'script', 'kind': 'longText', 'label': '腳本（JSON）'},
                                  {'key': 'bg', 'kind': 'asset', 'assetKind': 'image', 'label': '背景圖'}],
                       'html': html(k)} for k, c in CARDS.items()],
            'huds': [dict(HUD, html=hud_html())]}


def test_project(card_id):
    sys.path.insert(0, str(HERE.parent))
    import build
    p = build.load_skeleton()
    b = p['boards'][0]
    b['nodes'], b['edges'] = [], []
    p['nodes'], p['edges'] = b['nodes'], b['edges']
    p['variables'] = variables.project_variables()
    p['settings']['plugins'][PLUGIN_ID] = settings_entry()
    b['nodes'].append(cards.dialogue('t-start', '測試開始', ['測試：' + card_id], start=True))
    b['nodes'].append(card_node(card_id, 't-card'))
    shown = ' '.join(f'{k}={{{{{k}}}}}' for k in CARDS[card_id]['write'])
    b['nodes'].append(cards.dialogue('t-result', '結果', ['RESULT ' + shown]))
    cards.link(b, 't-start', 't-card'); cards.link(b, 't-card', 't-result')
    return p


if __name__ == '__main__':
    if sys.argv[1:2] == ['--test']:
        cid = sys.argv[2]
        out = ROOT / f'dist/test-{cid}.json'
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(test_project(cid), ensure_ascii=False))
        print('wrote', out)
