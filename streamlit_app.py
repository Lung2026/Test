import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="華新戰情室", layout="centered")

st.title("🛡️ 華新 (1605) 戰情 App")
st.caption("信貸資金管理專用 - 紀律操作")

# 1. 自動帶出華新最新報價
stock_id = "1605.TW"
try:
    stock = yf.Ticker(stock_id)
    df = stock.history(period="2d")
    curr_p = round(df['Close'].iloc[-1], 2)
    prev_p = round(df['Close'].iloc[-2], 2)
    diff = round(curr_p - prev_p, 2)
    pct = round((diff / prev_p) * 100, 2)
    
    st.metric("華新當前股價", f"{curr_p} TWD", f"{diff} ({pct}%)")
except:
    st.error("股價讀取失敗，請確認網路...")

# 2. 壓力測試區 (針對你的 800 萬信貸)
with st.expander("🚨 壓力測試 (維持率檢查)"):
    cost_price = 43.65
    current_val = st.slider("假設股價跌到...", 30.0, 50.0, float(curr_p))
    # 簡單模擬：假設你質押 100 萬市值
    ratio = (current_val / cost_price) * 300 # 假設起始維持率 300%
    st.write(f"當股價為 {current_val} 時，推估維持率為: {round(ratio, 2)}%")
    if ratio < 250:
        st.error("⚠️ 警告：已低於 250% 安全線！")

# 3. 今日觀察筆記
st.divider()
st.subheader("📝 今日籌碼與計畫")
note = st.text_area("市場觀察", placeholder="例如：週五金銀大跌，觀察週一銅價連動...")
plan = st.selectbox("預定動作", ["續抱", "減碼", "質押回補", "獲利了結"])

if st.button("儲存今日筆記"):
    st.success("✅ 筆記已存檔（僅限本次開啟，長期存檔需連動 Google Sheet）")
