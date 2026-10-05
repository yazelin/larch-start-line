"""讀 canon：原文切段、新寫取段。遊戲裡的文字一律從這裡來，不在程式裡手打。"""
import pathlib, re
CANON = pathlib.Path(__file__).resolve().parent.parent / 'canon'


def all_paras():
    blocks = [b.strip() for b in (CANON / '原文.md').read_text().split('\n\n') if b.strip()]
    return blocks[2:]  # 跳過標題與說明段


def para(start, end):
    ps = all_paras()
    i = next((k for k, p in enumerate(ps) if start in p), None)
    if i is None:
        raise KeyError(start)
    j = next((k for k in range(i, len(ps)) if end in ps[k]), None)
    if j is None:
        raise KeyError(end)
    return ps[i:j + 1]


def _sections():
    out, cur = {}, None
    for line in (CANON / '新寫.md').read_text().splitlines():
        m = re.match(r'## (.+)', line)
        if m:
            cur = m.group(1).strip(); out[cur] = []
        elif cur:
            out[cur].append(line)
    return {k: '\n'.join(v).strip() for k, v in out.items()}


def new(section):
    return _sections()[section]


def lines(section):
    return [l for l in new(section).splitlines() if l.strip()]


def blocks(section):
    return [b.strip() for b in new(section).split('\n\n') if b.strip()]
