import streamlit as st
import pandas as pd
import datetime

# 1. ページの設定（タイトルを「リバースター占い」に変更）
st.set_page_config(page_title="リバースター占い", page_icon="🌟")
st.title("🌟 リバースター占い")
st.write("生年月日を入力して、あなたの「社会的な表の顔」と「無意識の裏の顔」を占います！")

# 2. エクセルデータの読み込み
@st.cache_data
def load_data():
    return pd.read_excel("リバース星座占い.xlsx", sheet_name="表裏星座一覧")

try:
    df = load_data()
except Exception as e:
    st.error("エクセルファイルの読み込みに失敗しました。")
    st.stop()

# 3. 生年月日の入力カレンダー
birthday = st.date_input(
    "あなたの生年月日を教えてください",
    min_value=datetime.date(1920, 1, 1),
    max_value=datetime.date.today(),
    value=datetime.date(1990, 1, 1)
)

# 4. 鑑定ボタン
if st.button("鑑定する！"):
    st.markdown("---")
    st.header(f"🔮 鑑定結果（{birthday.year}年{birthday.month}月{birthday.day}日 生まれ）")

    # ※仮の固定表示です
    surface_sign = "おとめ座"
    
    st.subheader(f"☀️ 表の顔：{surface_sign}")
    
    # データの検索と表示
    surface_data = df[df['表星座'] == surface_sign]
    
    if not surface_data.empty:
        st.write("**【全体運】**")
        st.write(surface_data.iloc[0]['全体運'])
        
        st.write("**【仕事運】**")
        st.write(surface_data.iloc[0]['仕事運'])
        
        st.write("**【恋愛結婚運】**")
        st.write(surface_data.iloc[0]['恋愛結婚運'])
        
        st.write("**【金運】**")
        st.write(surface_data.iloc[0]['金運'])
        
        st.write("**【健康運】**")
        st.write(surface_data.iloc[0]['健康運'])
    else:
        st.write("データが見つかりませんでした。")

    st.success("鑑定完了！")
