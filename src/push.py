"""推到 Larch：快照 → 上傳用到的圖 → 換網址 → 整包 PUT（包在 {"project": …}）→ 讀回比對。

    python3 src/push.py "這次改了什麼"
"""
import json, os, re, sys, time, base64, pathlib, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(__file__))
import build

ROOT = build.ROOT
KEY = open(os.path.expanduser('~/.config/larch/key')).read().strip()
BASE = f'https://larch.ink/api/agent/projects/{build.PROJECT_ID}'
UPLOADED = ROOT / 'assets/uploaded.json'
MIME = {'.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.mp3': 'audio/mpeg'}


def req(method, path='', body=None, etag=None):
    h = {'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'}
    if etag: h['If-Match'] = etag
    for t in range(6):
        try:
            r = urllib.request.Request(BASE + path, method=method, headers=h, data=json.dumps(body).encode() if body is not None else None)
            with urllib.request.urlopen(r, timeout=180) as resp:
                return resp.headers.get('ETag'), json.loads(resp.read() or b'{}')
        except urllib.error.HTTPError as e:
            msg = e.read()[:300]
            if e.code == 429: print('429，等 30 秒'); time.sleep(30); continue
            raise SystemExit(f'{method} {path} → {e.code} {msg}')
    raise SystemExit('一直 429')


def upload_all(text):
    done = json.loads(UPLOADED.read_text()) if UPLOADED.exists() else {}
    for rel in sorted(set(re.findall(r'/files/assets/([\w./-]+\.(?:png|webp|jpg|mp3))', text))):
        f = ROOT / 'assets' / rel
        key = f'{rel}@{int(f.stat().st_mtime)}'
        if key in done: continue
        body = {'name': 'start-line_' + rel.replace('/', '_'), 'mimeType': MIME[f.suffix], 'category': 'image',
                'base64': base64.b64encode(f.read_bytes()).decode()}
        _, j = req('POST', '/media', body)
        done[key] = j['asset']['url']
        print('上傳', rel, '→', done[key], flush=True)
        UPLOADED.write_text(json.dumps(done, ensure_ascii=False, indent=1))
        time.sleep(2)
    latest = {}
    for k, url in done.items():
        latest[k.rsplit('@', 1)[0]] = url  # 同一檔多版本時取最後寫入的
    return latest


def main(summary):
    etag, cur = req('GET')
    online = cur.get('project', cur)
    snap = ROOT / 'snapshots' / time.strftime('%Y%m%d-%H%M%S.json')
    snap.parent.mkdir(exist_ok=True)
    snap.write_text(json.dumps(cur, ensure_ascii=False))
    print('快照', snap)

    built = build.build()
    text = json.dumps(built, ensure_ascii=False)
    urls = upload_all(text)
    for rel, url in urls.items():
        text = text.replace('/files/assets/' + rel, url)
    left = re.findall(r'/files/assets/[^"\\]+', text)
    if left: raise SystemExit(f'還有沒換掉的本機路徑：{left[:5]}')
    built = json.loads(text)

    etag, cur = req('GET')  # 上傳會改 media，重抓
    online = cur.get('project', cur)
    project = dict(online)
    for k in ('boards', 'nodes', 'edges', 'variables', 'settings', 'activeBoardId', 'name'):
        project[k] = built[k]
    req('PUT', '', {'project': project, 'summary': summary}, etag)

    _, back = req('GET')
    back = back.get('project', back)
    b0, w0 = back['boards'][0], built['boards'][0]
    assert len(b0['nodes']) == len(w0['nodes']), ('節點數不符', len(b0['nodes']), len(w0['nodes']))
    assert len(b0['edges']) == len(w0['edges']), ('連線數不符', len(b0['edges']), len(w0['edges']))
    for n in w0['nodes']:
        if n['data'].get('pluginCardId') == 'map':
            got = next(x for x in b0['nodes'] if x['id'] == n['id'])
            assert len(json.loads(got['data']['pluginValues']['map'])['events']) == len(json.loads(n['data']['pluginValues']['map'])['events']), n['id']
    assert 'start-line' in back['settings']['plugins'], '插件設定不見了'
    assert len(back['variables']) == len(built['variables']), '變數數量不符'
    print('推送完成，讀回比對通過：', len(b0['nodes']), '張卡、', len(b0['edges']), '條線')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '更新')
