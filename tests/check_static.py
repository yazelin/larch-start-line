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

if __name__ == '__main__':
    only = sys.argv[1:]
    bad = 0
    for f in TESTS:
        if only and f.__name__ not in only: continue
        try: f(); print('ok  ', f.__name__)
        except Exception as e: bad += 1; print('FAIL', f.__name__, '-', type(e).__name__, e)
    sys.exit(1 if bad else 0)
