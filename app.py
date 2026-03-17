import streamlit as st
import random

st.set_page_config(page_title="英文單字背誦", page_icon="🚀")
st.title("🚀 單字背誦 App")

# 1. 檔案上傳
uploaded_file = st.file_uploader("請上傳你的單字 .txt 檔", type="txt")

if uploaded_file:
    # 讀取單字並儲存在 session_state
    if "word_dict" not in st.session_state:
        content = uploaded_file.read().decode("utf-8")
        temp_dict = {}
        for line in content.splitlines():
            line = line.replace(',', ' ') 
            parts = line.strip().split()
            if len(parts) >= 2:
                temp_dict[parts[0]] = parts[1]
        
        st.session_state.word_dict = temp_dict
        st.session_state.words = list(temp_dict.keys())
        random.shuffle(st.session_state.words)
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.submitted = False # 新增一個狀態記錄是否已提交

    if st.session_state.word_dict:
        idx = st.session_state.index
        word_list = st.session_state.words

        if idx < len(word_list):
            current_word = word_list[idx]
            st.write(f"### 第 {idx+1} 題 / 共 {len(word_list)} 題")
            st.info(f"👉 請輸入 **{current_word}** 的中文意思")

            # 表單內只放輸入框和「送出」按鈕
            with st.form(key=f"word_form_{idx}"):
                user_ans = st.text_input("中文意思：")
                submit = st.form_submit_button("送出答案")

                if submit:
                    st.session_state.submitted = True
                    correct_ans = st.session_state.word_dict[current_word]
                    if user_ans.strip() == correct_ans.strip():
                        st.success("✅ 正確！")
                        st.session_state.score += 1
                    else:
                        st.error(f"❌ 錯誤！正確答案是：{correct_ans}")
            
            # 「下一題」按鈕放在 form 外面
            if st.session_state.submitted:
                if st.button("下一題 ➡️"):
                    st.session_state.index += 1
                    st.session_state.submitted = False # 重置提交狀態
                    st.rerun()
        else:
            st.balloons()
            st.write(f"🎉 測驗結束！總分：{st.session_state.score}/{len(word_list)}")
            if st.button("重新開始"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
