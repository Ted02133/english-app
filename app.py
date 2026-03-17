import streamlit as st
import random

st.set_page_config(page_title="英文單字背誦", page_icon="🚀")
st.title("🚀 單字背誦 App")

# 使用側邊欄 (Sidebar) 放置上傳功能，這樣主畫面會很乾淨
with st.sidebar:
    st.header("⚙️ 設定")
    uploaded_file = st.file_uploader("上傳單字 .txt 檔", type="txt")

if uploaded_file:
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
        st.session_state.submitted = False

    if st.session_state.word_dict:
        idx = st.session_state.index
        word_list = st.session_state.words

        if idx < len(word_list):
            current_word = word_list[idx]
            
            # 用簡單的 text 代替大標題，省空間
            st.write(f"**進度：{idx+1} / {len(word_list)}** | **得分：{st.session_state.score}**")
            st.subheader(f"❓ 請輸入：{current_word}")

            with st.form(key=f"word_form_{idx}", clear_on_submit=True):
                # 這裡增加 label_visibility，讓輸入框更明顯
                user_ans = st.text_input("在這裡輸入中文意思", label_visibility="collapsed")
                submit = st.form_submit_button("送出答案")

                if submit:
                    st.session_state.submitted = True
                    correct_ans = st.session_state.word_dict[current_word]
                    if user_ans.strip() == correct_ans.strip():
                        st.success("✅ 正確！")
                        st.session_state.score += 1
                    else:
                        st.error(f"❌ 錯誤！正確答案：{correct_ans}")
            
            if st.session_state.submitted:
                if st.button("下一題 ➡️", use_container_width=True):
                    st.session_state.index += 1
                    st.session_state.submitted = False
                    st.rerun()
        else:
            st.balloons()
            st.write(f"🎉 測驗結束！總分：{st.session_state.score}/{len(word_list)}")
            if st.button("重新開始", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
else:
    st.warning("👈 請點擊左上角箭頭，展開側邊欄上傳單字檔。")
