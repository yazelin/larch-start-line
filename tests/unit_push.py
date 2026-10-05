"""push.py 單元測試（不連網）：python3 tests/unit_push.py"""
import sys, os, io, urllib.error
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
os.environ.setdefault('LARCH_KEY_FILE', '/dev/null')
import push
bad = 0
def t(name, fn):
    global bad
    try: fn(); print('ok  ', name)
    except Exception as e: bad += 1; print('FAIL', name, '-', type(e).__name__, e)

def keeps_online_settings():
    online = {'titleScreen': {'layers': [1]}, 'aiMode': 'x', 'plugins': {'other': {'enabled': True}, 'larch-rpg-system': {'enabled': True, 'settings': {'lobby': 'keep', 'database': 'old'}}}}
    built = {'titleCoverImage': 'c', 'projectThumbnail': 't', 'aiMode': 'authored', 'plugins': {'start-line': {'enabled': True}, 'larch-rpg-system': {'enabled': True, 'settings': {'database': 'new'}}}}
    m = push.merge_settings(online, built)
    assert m['titleScreen'] == {'layers': [1]}, '線上的 titleScreen 被洗掉'
    assert m['aiMode'] == 'x', '產生器不負責的鍵被覆蓋'
    assert m['plugins']['other'] == {'enabled': True}, '線上其他插件被洗掉'
    assert m['plugins']['larch-rpg-system']['settings'] == {'lobby': 'keep', 'database': 'new'}
    assert m['plugins']['start-line'] == {'enabled': True} and m['titleCoverImage'] == 'c'

def retries_5xx_and_network():
    calls = []
    def fake(r, timeout=0):
        calls.append(1)
        if len(calls) == 1: raise urllib.error.HTTPError('u', 502, 'bad', {}, io.BytesIO(b''))
        if len(calls) == 2: raise urllib.error.URLError('timeout')
        class R:
            headers = {'ETag': 'e'}
            def read(self): return b'{"ok":1}'
            def __enter__(self): return self
            def __exit__(self, *a): pass
        return R()
    push._open, push._sleep = fake, lambda s: None
    et, j = push.req('GET')
    assert j == {'ok': 1} and len(calls) == 3, (j, len(calls))

t('只覆寫產生器負責的設定，其他保留線上', keeps_online_settings)
t('GET 遇到 502、網路錯誤會重試', retries_5xx_and_network)
sys.exit(1 if bad else 0)
