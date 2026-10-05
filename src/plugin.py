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
    if card_id == 'pace':
        eyes = next(p for p in text.all_paras() if '清澈又倔強的眼神' in p)
        eyes = eyes[eyes.index('她剛才抬頭'):].rstrip('。')
        return {'intro': new('配速開場'), 'sprintText': new('配速衝刺'), 'endGood': new('配速終點好'),
                'endMessy': new('配速終點亂'), 'eyes': eyes}
    if card_id == 'notebook':
        return {'title': new('筆記標題'), 'question': new('筆記題目'), 'answer': new('筆記答案'),
                'hint1': new('筆記提示一'), 'hint2': new('筆記提示二'), 'right': new('筆記答對'),
                'submit': '就這個時間', 'next': '繼續',
                'clues': [{'var': 'clue_order', 'text': new('線索秩序冊')}, {'var': 'clue_mate', 'text': new('線索隊友')},
                          {'var': 'clue_walk', 'text': new('線索步行')}]}
    if card_id == 'drafts':
        return {'drafts': text.lines('草稿'), 'sendLabel': '送出', 'to': '林向晚'}
    if card_id == 'coin-drop':
        return {'intro': new('零錢開場'), 'earlyText': new('零錢太早'), 'lateText': new('零錢太晚')}
    raise KeyError(card_id)


# 卡片：檔名、讀、寫、呈現方式。write 名單少一個名字，larch:set 會被靜默丟掉。
CARDS = {
    'start-gun': {'name': '起跑', 'read': ['bpm', 'fouls'], 'write': ['bpm', 'fouls', 'thought'], 'presentation': 'fullscreen'},
    'pace': {'name': '配速', 'read': ['bpm'], 'write': ['bpm', 'pace_score'], 'presentation': 'fullscreen'},
    'notebook': {'name': '她的筆記', 'read': ['clue_order', 'clue_mate', 'clue_walk', 'calc_tries'], 'write': ['calc_ok', 'calc_tries'], 'presentation': 'fullscreen'},
    'drafts': {'name': '三次草稿', 'read': [], 'write': ['drafted'], 'presentation': 'fullscreen'},
    'coin-drop': {'name': '零錢', 'read': ['bpm', 'coin_tries'], 'write': ['bpm', 'coin_ok', 'coin_tries'], 'presentation': 'fullscreen'},
}
# 卡片在白板上的節點 id（地圖 jump 用）
NODE = {'start-gun': 'c-start', 'pace': 'c-pace', 'notebook': 'c-notebook', 'drafts': 'c-drafts', 'coin-drop': 'c-coin'}
# 單卡測試時的變數初始值（模擬走到這張卡之前的狀態）
TEST_PRESET = {'notebook': {'clue_order': True, 'clue_mate': True, 'clue_walk': True}}
HUD = {'id': 'heart', 'title': '心跳', 'anchor': 'top-right', 'width': 132, 'height': 44, 'offsetX': 16, 'offsetY': 16,
       'interactive': False, 'readVariables': ['bpm']}


def card_art(card_id, a):
    """每張卡從美術路徑表取哪些圖（缺圖就不帶）。"""
    want = {'start-gun': {'bg': 'start-pov'}, 'pace': {'eyesImg': 'pace-eyes'}, 'coin-drop': {'bg': 'coin-bg', 'him': 'walk-cheng'}}
    return {k: a[v] for k, v in want.get(card_id, {}).items() if a.get(v)}


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
    for v in p['variables']:
        if v['name'] in TEST_PRESET.get(card_id, {}): v['defaultValue'] = TEST_PRESET[card_id][v['name']]
    p['settings']['plugins'][PLUGIN_ID] = settings_entry()
    b['nodes'].append(cards.dialogue('t-start', '測試開始', ['測試：' + card_id], start=True))
    import art
    b['nodes'].append(card_node(card_id, 't-card', card_art(card_id, art.paths())))
    shown = ' '.join(f'{k}={{{{{k}}}}}' for k in CARDS[card_id]['write'])
    b['nodes'].append(cards.dialogue('t-result', '結果', ['RESULT ' + shown]))
    cards.link(b, 't-start', 't-card'); cards.link(b, 't-card', 't-result')
    return p


if __name__ == '__main__':
    import build
    if sys.argv[1:2] == ['--test']:
        cid = sys.argv[2]
        out = ROOT / f'dist/test-{cid}.json'
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(test_project(cid), ensure_ascii=False))
        build.mirror_assets(out.parent / 'assets')
        print('wrote', out)
