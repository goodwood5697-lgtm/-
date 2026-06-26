import streamlit as st
import pandas as pd
import datetime

# --- ページ全体の設定 ---
st.set_page_config(page_title="リバースター占い", page_icon="🌟", layout="wide")

st.title("🌟 リバースター占い 鑑定結果")

st.info("💡 **【現在のお試し版について】**\n現在はエクセルに保存されているデータ（1981年9月7日生まれの鑑定結果）をそのまま表示しています。今後、計算システムを組み込むことで、カレンダーの日付に合わせて結果が自動で切り替わるようになります！")

# カレンダー入力（※現在はデザインのみのダミーです）
st.date_input("生年月日を選択", value=datetime.date(1981, 9, 7))

# --- エクセルデータの読み込み ---
@st.cache_data
def load_data():
    # ヘッダーなしで読み込み、行番号で確実に取り出せるようにします
    # ※ファイル名が違う場合は "リバース星座占い.xlsx" の部分を直してください
    return pd.read_excel("リバース星座占い.xlsx", sheet_name="リバース占い鑑定結果", header=None)

try:
    df = load_data()
except Exception as e:
    st.error("エクセルファイルの読み込みに失敗しました。「リバース星座占い.xlsx」がGitHubにアップロードされているか確認してください。")
    st.stop()

# ==========================================
# 1. 表星座の鑑定結果（5種の運勢）
# ==========================================
st.markdown("---")
st.header(f"☀️ 社会的な表の顔： {df.iloc[4, 0]}")

col1, col2 = st.columns(2)
with col1:
    st.subheader(f"【{df.iloc[5, 0]}】")
    st.write(df.iloc[5, 1])
    st.subheader(f"【{df.iloc[6, 0]}】")
    st.write(df.iloc[6, 1])
    st.subheader(f"【{df.iloc[7, 0]}】")
    st.write(df.iloc[7, 1])
with col2:
    st.subheader(f"【{df.iloc[8, 0]}】")
    st.write(df.iloc[8, 1])
    st.subheader(f"【{df.iloc[9, 0]}】")
    st.write(df.iloc[9, 1])

# ==========================================
# 2. 裏星座の鑑定結果（5種の運勢）
# ==========================================
st.markdown("---")
st.header(f"🌙 無意識の裏の顔： {df.iloc[12, 0]}")
st.caption(df.iloc[13, 1]) # 裏星座の全体説明

col3, col4 = st.columns(2)
with col3:
    st.subheader(f"【{df.iloc[14, 0]}】")
    st.write(df.iloc[14, 1])
    st.subheader(f"【{df.iloc[15, 0]}】")
    st.write(df.iloc[15, 1])
with col4:
    st.subheader(f"【{df.iloc[16, 0]}】")
    st.write(df.iloc[16, 1])
    st.subheader(f"【{df.iloc[17, 0]}】")
    st.write(df.iloc[17, 1])

# ==========================================
# 3. リバーシブル・アングル
# ==========================================
st.markdown("---")
st.header("💫 表と裏のアングル（交差点）")
st.write(df.iloc[20, 0]) # アングルの説明文
st.success(f"**あなたのアングル： {df.iloc[21, 1]}**")

# ==========================================
# 4, 5, 6. 運勢バイオリズム（年・月・日）
# ==========================================
st.markdown("---")
st.header("📅 運勢バイオリズム（イベント・キャラ変）")
st.write("各タイミングでの運勢、起きやすいイベント、そして精神的な「キャラ変」を表示します。")

# 指定した名前（年天運など）から下の表を抽出して表示する関数
def display_fortune_section(df, start_keyword):
    idx_list = df[df[0] == start_keyword].index
    if len(idx_list) == 0:
        return
    start_idx = idx_list[0]
    
    data_rows = []
    for i in range(start_idx + 1, len(df)):
        val = df.iloc[i, 0]
        # 次の項目や空白行にぶつかったらストップ
        if str(val) in ["月天運", "日天運", "干合名"] or pd.isna(val):
            if pd.isna(val) and i+1 < len(df) and pd.isna(df.iloc[i+1, 0]):
                break
            continue
        data_rows.append(df.iloc[i])
        
    if data_rows:
        section_df = pd.DataFrame(data_rows)
        # 空白だらけの列を削除し、見やすくする
        section_df = section_df.dropna(axis=1, how='all').fillna("")
        st.dataframe(section_df, use_container_width=True)

st.subheader("🗓️ 年運（12年サイクル）")
display_fortune_section(df, "年天運")

st.subheader("🌙 月運（1年サイクル）")
display_fortune_section(df, "月天運")

st.subheader("☀️ 日運（毎日のサイクル）")
display_fortune_section(df, "日天運")

# ==========================================
# 7. キャラ変（干合）の詳細説明
# ==========================================
st.markdown("---")
st.header("🌪️ 「キャラ変」ビフォーアフター解説")
st.write("運勢表に表示される「オカン化」「エロ化」などが起きたとき、ステータス別にどのような変化が起きるかの解説です。")

chara_data = {
    "干合とキャラ変": ["⛰️ 甲己干合 (土化)\nオカン化", "⚔️ 乙庚干合 (金化)\nツンツン化", "💧 丙辛干合 (水化)\nデレ化", "🌳 丁壬干合 (木化)\nエロ化", "🔥 戊癸干合 (火化)\nオトメ化"],
    "未婚 (相手なし)": [
        "真面目な相手をロックオン。\n遊びは卒業しド安定志向へ。", 
        "信頼度100%の相手確保。\nこの人以外はバッサリ斬る本気モード。", 
        "素を見せられる相手との遭遇。\n強がり解除し甘えん坊化。", 
        "フェロモン全開で確保。\n恋に落ちたい恋愛至上主義。", 
        "打算からの突然の大発火。\nドライな関係から電撃スパーク。"
    ],
    "未婚 (相手あり)": [
        "恋人から人生の相棒へ。\nプロポーズ待ちで結婚願望が高まる。", 
        "白黒ハッキリ運命のジャッジ。\n優柔不断を終了し覚悟完了。", 
        "主導権争い終了。\nプライド崩壊しどっぷり尽くす深い愛情。", 
        "四六時中ベッタリ一心同体。\n理性喪失し盲目的な愛に沼る。", 
        "マンネリ打破の突然のスパーク。\n現状維持を打破する起爆剤。"
    ],
    "既婚 (夫婦)": [
        "盤石な家族の絆。\nマイホーム第一主義で家庭の平和を優先。", 
        "なぁなぁ解消、絆の再構築。\n伴侶への義理堅さ再確認。", 
        "潤い復活、思いやりの生活。\n意地っ張りからデレ顔へ。", 
        "お互いの領域が融合し濃密に。\nルームメイトから恋人へ再燃。", 
        "まさかの熱愛でマンネリ打破。\n事務的ルーティンに革命を。"
    ]
}
st.table(pd.DataFrame(chara_data))

st.markdown("---")
st.caption("© 2024 リバースター占い All Rights Reserved.")
