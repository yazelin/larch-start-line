"""組出 dist/project.json：骨架＋劇情卡＋地圖＋插件。"""
import json, pathlib
import os, cards, text, variables, plugin, art, mapkit
import map_stadium
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
    p['settings']['plugins'][plugin.PLUGIN_ID] = plugin.settings_entry()
    a = art.paths()
    p['settings']['plugins']['larch-rpg-system']['settings']['database'] = json.dumps(rpg_database(a), ensure_ascii=False)
    story_cards(board)
    N = board['nodes'].append
    for cid in ('start-gun', 'pace', 'drafts'):
        N(plugin.card_node(cid, plugin.NODE[cid]))
    N(map_stadium.build_stadium(a))
    L = lambda x, y: cards.link(board, x, y)
    L(PROLOGUE, map_stadium.MAP_ID)
    L(plugin.NODE['start-gun'], plugin.NODE['pace']); L(plugin.NODE['pace'], map_stadium.MAP_ID)
    L(MID, plugin.NODE['drafts']); L(plugin.NODE['drafts'], SEAWALL)
    return p


def rpg_database(a):
    def actor(id, name, walk):
        return {'id': id, 'name': name, 'title': '', 'profile': '', 'role': 'party', 'walk': mapkit.walker(a[walk]),
                'portrait': '', 'kit': 'none', 'rig': '', 'joinVariable': ''}
    return {'version': 1, 'heroId': 'chengche', 'leadSwitch': False,
            'actors': [actor('chengche', '程徹', 'walk-cheng'), actor('xiangwan', '林向晚', 'walk-lin')]}


# 卡片 id：地圖事件與插件共用，只在這裡定義
PROLOGUE, MID, SEAWALL, SEAWALL2, ENDING_B, GAZE, R1_FINISH = 'prologue', 'mid', 'seawall', 'seawall2', 'ending-b', 'gaze', 'r1-finish'


def story_cards(board):
    N = board['nodes'].append
    N(cards.dialogue(PROLOGUE, '序章', para('在槍響之前', '所謂的起跑'), start=True))
    N(cards.dialogue(GAZE, '四目相對', para('程徹第一次見到林向晚', '沒有任何對白')))
    N(cards.dialogue(R1_FINISH, '小組第一', para('那場比賽他拿了小組第一', '那場比賽他拿了小組第一')))
    N(cards.dialogue(MID, '後來', para('後來他們真的在一起了', '人們總以為愛情的開始')))
    N(cards.dialogue(SEAWALL, '花蓮防波堤', para('大三那年夏天', '程徹愣住了') + [new('換人提示')]))
    N(cards.dialogue(SEAWALL2, '她的起跑線', para('那天我早就在看台後面', '起跑總在開始前，如同')))
    N(cards.dialogue(ENDING_B, '沒有起跑', text.blocks('結局B')))


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
