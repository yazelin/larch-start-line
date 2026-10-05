"""組出 dist/project.json：骨架＋劇情卡＋地圖＋插件。"""
import json, pathlib
import os, cards, text, variables, plugin, art, mapkit
import map_stadium, map_kitchen
from text import para, new
ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT_ID = 'project-c0f31c1f-2b06-44d8-a62e-374bff81fd60'


def load_skeleton():
    return json.loads((ROOT / 'skeleton/project.json').read_text())


def build():
    p = load_skeleton()
    board = p['boards'][0]
    board['nodes'], board['edges'] = [], []
    p['nodes'], p['edges'] = board['nodes'], board['edges']  # 頂層是目前白板的複本
    p['variables'] = variables.project_variables()
    p['description'] = text.new('簡介')
    p['settings']['plugins'][plugin.PLUGIN_ID] = plugin.settings_entry()
    a = art.paths()
    p['settings']['plugins']['larch-rpg-system']['settings']['database'] = json.dumps(rpg_database(a), ensure_ascii=False)
    story_cards(board, a)
    if a['bgm-01']: p['settings'].setdefault('titleScreen', {})['bgm'] = a['bgm-01']   # 標題音樂
    p['settings']['titleCoverImage'] = a['cover']        # 專用封面：左半留給標題與選單
    p['settings']['projectThumbnail'] = a['cover']
    N = board['nodes'].append
    for cid in plugin.NODE:
        N(plugin.card_node(cid, plugin.NODE[cid], plugin.card_art(cid, a)))
        if cid in ('notebook', 'coin-drop') and a['bgm-05']: board['nodes'][-1]['data'].update(bgm=a['bgm-05'], bgmVolume=0.5, bgmLoop=True)   # 她的視角
        if cid == 'pace' and a['bgm-03']: board['nodes'][-1]['data'].update(bgm=a['bgm-03'], bgmVolume=0.5, bgmLoop=True)   # 八百公尺
    N(cards.setvar('go-r2', '換到她那邊', [('phase', 'r2')]))
    N(map_stadium.build_stadium(a))
    N(map_kitchen.build_kitchen(a))
    L = lambda x, y: cards.link(board, x, y)
    L(PROLOGUE, map_stadium.MAP_ID)
    L(plugin.NODE['start-gun'], plugin.NODE['pace']); L(plugin.NODE['pace'], map_stadium.MAP_ID)
    L(MID, plugin.NODE['drafts']); L(plugin.NODE['drafts'], SEAWALL); L(SEAWALL, 'go-r2'); L('go-r2', map_stadium.MAP_ID)
    L(plugin.NODE['notebook'], map_stadium.MAP_ID)
    L(plugin.NODE['coin-drop'], SEAWALL2); L(SEAWALL2, map_kitchen.MAP_ID)
    L(ENDING_B, map_stadium.MAP_ID)
    return p


def rpg_database(a):
    def actor(id, name, walk, portrait):
        return {'id': id, 'name': name, 'title': '', 'profile': '', 'role': 'party', 'walk': mapkit.walker(a[walk]),
                'portrait': a[portrait], 'join': 'later', 'kit': 'none', 'rig': '', 'joinVariable': ''}
    return {'version': 1, 'heroId': 'chengche', 'leadSwitch': False,
            'actors': [actor('chengche', '程徹', 'walk-cheng', 'p-cheng'), actor('xiangwan', '林向晚', 'walk-lin', 'p-lin'),
                       actor('chengche-adult', '程徹', 'walk-cheng-adult', 'p-cheng-adult')]}


# 卡片 id：地圖事件與插件共用，只在這裡定義
PROLOGUE, MID, SEAWALL, SEAWALL2, ENDING_B, GAZE, R1_FINISH, KITCHEN, FIN, VENDING = 'prologue', 'mid', 'seawall', 'seawall2', 'ending-b', 'gaze', 'r1-finish', 'kitchen', 'fin', 'vending'


def story_cards(board, a):
    N = board['nodes'].append
    N(cards.dialogue(PROLOGUE, '序章', para('在槍響之前', '所謂的起跑'), start=True, bg=a['style']))
    if a['bgm-01']: board['nodes'][-1]['data'].update(bgm=a['bgm-01'], bgmVolume=0.5, bgmLoop=True)
    N(cards.dialogue(GAZE, '四目相對', para('程徹第一次見到林向晚', '沒有任何對白'), bg=a['cg-gaze']))
    N(cards.dialogue(R1_FINISH, '小組第一', para('那場比賽他拿了小組第一', '那場比賽他拿了小組第一'), bg=a['cg-finish']))
    N(cards.dialogue(MID, '後來', para('後來他們真的在一起了', '人們總以為愛情的開始')))
    if a['bgm-04']: board['nodes'][-1]['data'].update(bgm=a['bgm-04'], bgmVolume=0.5, bgmLoop=True)   # 中章到防波堤
    N(cards.dialogue(SEAWALL, '花蓮防波堤', para('大三那年夏天', '程徹愣住了') + [new('換人提示')], bg=a['cg-seawall']))
    N(cards.dialogue(SEAWALL2, '她的起跑線', para('那天我早就在看台後面', '起跑總在開始前，如同'), bg=a['cg-seawall']))
    if a['bgm-06']: board['nodes'][-1]['data'].update(bgm=a['bgm-06'], bgmVolume=0.5, bgmLoop=True)   # 防波堤後半到廚房
    N(cards.dialogue(ENDING_B, '沒有起跑', text.blocks('結局B'), bg=a['coin-bg']))
    if a['bgm-07']: board['nodes'][-1]['data'].update(bgm=a['bgm-07'], bgmVolume=0.5, bgmLoop=True)   # 結局 B
    N(cards.dialogue(KITCHEN, '冬夜', para('幾年後的一個冬夜', '世人總在等那聲槍響'), bg=a['cg-kitchen']))
    N(cards.dialogue(VENDING, '販賣機前', [('程徹', '妳的十塊錢。')], bg=a['cg-vending']))
    # 第二輪她的內心話（立繪表情：害羞、被嚇到）
    N(cards.dialogue('r2-peek', '偷看', [new('偷看'), ('林向晚', new('偷看心聲'))], actors=[cards.actor('林向晚', a['p-lin-shy'])]))
    N(cards.dialogue('r2-caught', '差點被看到', [('林向晚', new('差點被看到'))], actors=[cards.actor('林向晚', a['p-lin-flustered'])]))
    # 呼應第一輪：配速穩＝他跑得好穩；節拍亂＝他一直在分心（在想她）
    N(cards.dialogue('r2-watch-steady', '他跑得好穩', [new('看他比賽'), ('林向晚', new('看他比賽心聲穩'))], actors=[cards.actor('林向晚', a['p-lin-shy'])]))
    N(cards.dialogue('r2-watch-distracted', '他在看這邊嗎', [new('看他比賽'), ('林向晚', new('看他比賽心聲分心'))], actors=[cards.actor('林向晚', a['p-lin-shy'])]))
    N(cards.dialogue(FIN, '完', [new('完')], bg=a['cg-kitchen']))
    N(cards.dialogue('fin-b', '完（結局 B）', [new('完')], bg=a['coin-bg']))
    if a['bgm-07']: board['nodes'][-1]['data'].update(bgm=a['bgm-07'], bgmVolume=0.5, bgmLoop=True)


def main():
    p = build()
    out = ROOT / 'dist/project.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(p, ensure_ascii=False))
    mirror_assets(out.parent / 'assets')
    print('wrote', out, len(p['boards'][0]['nodes']), 'nodes')


def mirror_assets(dst):
    """serve.py 只提供 JSON 所在資料夾裡的真實檔案（符號連結會被擋），所以用硬連結鏡像一份 assets。"""
    import shutil
    def link(src, d):
        try: os.link(src, d)
        except OSError: shutil.copy2(src, d)
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(ROOT / 'assets', dst, copy_function=link)


if __name__ == '__main__':
    main()
