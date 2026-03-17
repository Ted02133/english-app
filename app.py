import streamlit as st
import random

# 設定網頁標題
st.title("🚀 單字背誦 App")

# 1. 檔案上傳 (取代原本的桌面路徑，更適合手機使用)
uploaded_file = st.file_uploader("請上傳你的單字 .txt 檔", type="txt")

if uploaded_file:
    # 讀取單字
    content = uploaded_file.read().decode("utf-8")
    word_dict = {}
    for line in content.splitlines():
        parts = line.strip().split()
        if len(parts) == 2:
            word_dict[parts[0]] = parts[1]

    # 初始化 Session State (確保網頁重新整理時數據不會消失)
    if "words" not in st.session_state:
        st.session_state.words = list(word_dict.keys())
        random.shuffle(st.session_state.words)
        st.session_state.index = 0
        st.session_state.score = 0

    # 顯示進度
    idx = st.session_state.index
    if idx < len(st.session_state.words):
        current_word = st.session_state.words[idx]
        st.write(f"### 當前題目： {current_word}")

        user_ans = st.text_input("請輸入中文意思：", key=f"q_{idx}")

        if st.button("送出答案"):
            if user_ans == word_dict[current_word]:
                st.success("✅ 正確！")
                st.session_state.score += 1
            else:
                st.error(f"❌ 錯誤！正確答案是：{word_dict[current_word]}")

            st.session_state.index += 1
            st.rerun()  # 進入下一題
    else:
        st.balloons()  # 撒花慶祝
        st.write(
            f"🎉 測驗結束！總分：{st.session_state.score}/{len(st.session_state.words)}"
        )
        if st.button("重新開始"):
            del st.session_state.words
            st.rerun()
