"""全專案變數只在這裡定義一次：名字 → (型別, 預設值, 標籤)。插件卡的 read/write 名單與地圖條件都對照這份。"""
VARS = {
    'round': ('number', 1, '第幾輪'),
    'phase': ('string', '', '階段'),
    'bpm': ('number', 0, '心跳'),
    'fouls': ('number', 0, '偷跑次數'),
    'thought': ('number', 0, '起跑前的想法'),
    'pace_score': ('number', -1, '配速分數'),
    'clue_order': ('boolean', False, '線索：秩序冊'),
    'clue_mate': ('boolean', False, '線索：隊友'),
    'clue_walk': ('boolean', False, '線索：步行'),
    'calc_ok': ('boolean', False, '推算答對'),
    'calc_tries': ('number', 0, '推算次數'),
    'drafted': ('boolean', False, '訊息送出'),
    'coin_ok': ('boolean', False, '零錢時機'),
    'coin_tries': ('number', 0, '零錢次數'),
    'ending': ('string', '', '結局'),
}


def project_variables():
    return [{'id': k, 'name': k, 'label': lab, 'type': t, 'defaultValue': d} for k, (t, d, lab) in VARS.items()]
