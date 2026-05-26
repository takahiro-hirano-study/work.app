import streamlit as st
from pathlib import Path
import json
from datetime import datetime

if 'result' not in st.session_state:
    st.session_state.result = 0.0

if 'realcycle_time' not in st.session_state:
    st.session_state.real_cycletime = 0.0

# ページ設定
st.set_page_config(page_title='工数計算アプリ', layout='centered')
st.title('工数計算アプリ')

# 保存ファイル
data_file = Path('data/work_records.json')
data_file.parent.mkdir(parents=True, exist_ok=True)

# 前回のデータ読み込み
if data_file.exists():
    try:
        records = json.loads(data_file.read_text(encoding='utf-8'))
    except:
        recods = []
else:
    records = []

# 入力フォーム
col1, col2 = st.columns(2)

with col1:
    part_name = st.selectbox('機種名',['A', 'B', 'C'])
    prod_qty = st.number_input(
        '生産台数A',
        min_value=1, 
        value=1,
        step=1,
        format='%d',
        help='空欄をクリックして直接数字を入力してください'
    )

with col2:
    qty = st.number_input(
        '数量B', 
        min_value=1, 
        value=1,
        step=1,
        format='%d',
        help='空欄をクリックして直接数字を入力してください'
    )
    time_min = st.number_input('作業時間 (分)', min_value=1, value=30)

# 理想時間 (機種ごとの基準)
ideal_times = {'A': 6, 'B': 5, 'C': 3}
ideal = ideal_times[part_name]

# 計算するために関数を定義
def real_cycletime(prod_qty, qty, time_min):
    a = prod_qty * qty
    if a > 0:
        b = time_min / a
        return a,b
    else:
        st.error('数量が0です')
        return 0, 0.0
   

# 計算ボタン
if st.button('計算する', type='secondary', width='stretch'):
    a, b = real_cycletime(prod_qty, qty, time_min)

    st.session_state.result = b
    st.session_state.real_cycletime = b

# 計算結果
st.subheader('計算結果')
col3, col4 = st.columns(2)

with col3:
    st.metric('秒数', f'{st.session_state.result:.2f} 分')
    st.metric('理想の秒数', f'{ideal:.2f} 分')

with col4:
    diff = st.session_state.result - ideal
    if diff < 0:
        st.success('とても速いです！素晴らしい！')
    elif diff <0.5:
        st.success('良いペースです！この調子でいきましょう！')
    elif diff < 1:
        st.warning('少し遅めです')
    else:
            st.error('かなり遅いです...改善しましょう')

# 保存ボタン
if st.button('この結果を保存'):
    record = {
        '日時': datetime.now().strftime('%Y-%m-%d %H:%M'),
        '機種': part_name,
        '実績': round(st.session_state.result, 3),
        '理想': ideal,
        '評価': '速い' if st.session_state.result < ideal else '遅い' if st.session_state.result > ideal else '順調'
    }
    records.append(record)
    data_file.write_text(json.dumps(records, ensure_ascii=False, indent=2),encoding='utf-8')
    st.success('保存しました！')

# これまでの記録表示
if records:
    st.subheader('これまでの記録')
    st.dataframe(records, width='stretch')
