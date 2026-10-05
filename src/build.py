"""組出 dist/project.json：骨架＋劇情卡＋地圖＋插件。"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT_ID = 'project-c0f31c1f-2b06-44d8-a62e-374bff81fd60'


def load_skeleton():
    return json.loads((ROOT / 'skeleton/project.json').read_text())


def build():
    p = load_skeleton()
    board = p['boards'][0]
    board['nodes'], board['edges'] = [], []
    p['nodes'], p['edges'] = board['nodes'], board['edges']  # 頂層是目前白板的複本
    return p


def main():
    p = build()
    out = ROOT / 'dist/project.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(p, ensure_ascii=False))
    print('wrote', out, len(p['boards'][0]['nodes']), 'nodes')


if __name__ == '__main__':
    main()
