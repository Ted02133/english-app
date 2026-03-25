import random
import os


# === 讀取單字檔 ===
def load_words(filename):
    word_dict = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    eng, ch = parts
                    word_dict[eng] = ch
        return word_dict
    except FileNotFoundError:
        print(f"\n⚠️ 找不到檔案：{filename}")
        print("請確認文字檔與本程式在同一資料夾中。")
        input("按 Enter 結束程式...")
        exit()


# === 顯示測驗結果 ===
def show_result(correct, wrong, wrong_list):
    print("\n=== 測驗結束 ===")
    print(f"✅ 答對：{correct} 題")
    print(f"❌ 答錯：{wrong} 題\n")

    if wrong_list:
        print("以下是你答錯的題目：")
        for eng, ch in wrong_list:
            print(f"- {eng} = {ch}")
    else:
        print("🎉 全部答對！太棒了！")


# === 單字測驗 ===
# === 單字測驗 (優化流暢版) ===
def quiz(word_dict, mode="en_to_ch"):
    words = list(word_dict.keys())
    random.shuffle(words)
    correct = 0
    wrong = 0
    wrong_list = []

    total_count = len(words)

    for index, word in enumerate(words, start=1):
        # 每一題開始前先清空畫面，讓畫面維持只有一題
        os.system("cls" if os.name == "nt" else "clear")
        print(f"=== 進度：{index}/{total_count} | 正確：{correct} | 錯誤：{wrong} ===")
        print("\n輸入 exit 離開測驗\n")

        if mode == "en_to_ch":
            ans = input(f"題目：{word} \n請輸入中文意思：")
            if ans.lower() == "exit":
                break
            if ans == word_dict[word]:
                correct += 1
                # 答對了直接進下一輪迴圈，畫面會被清空並顯示下一題
            else:
                print(f"\n❌ 錯誤！正確答案是：{word_dict[word]}")
                input("按 Enter 鍵繼續...")  # 答錯時停下來讓你看一下正確答案
                wrong += 1
                wrong_list.append((word, word_dict[word]))

        elif mode == "ch_to_en":
            ans = input(f"題目：{word_dict[word]} \n請輸入英文單字：")
            if ans.lower() == "exit":
                break
            if ans.lower() == word.lower():
                correct += 1
            else:
                print(f"\n❌ 錯誤！正確答案是：{word}")
                input("按 Enter 鍵繼續...")
                wrong += 1
                wrong_list.append((word, word_dict[word]))

    os.system("cls" if os.name == "nt" else "clear")
    show_result(correct, wrong, wrong_list)

    # 錯題複習邏輯保持不變...
    if wrong_list:
        again = input("\n要重練錯題嗎？(y/n)：")
        if again.lower() == "y":
            quiz(dict(wrong_list), mode)


# === 選擇桌面上的 txt 檔 ===
def choose_txt_from_desktop():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "英文單字")

    # 檢查資料夾是否存在
    if not os.path.exists(desktop_path):
        print("⚠️ 找不到桌面上的『英文單字』資料夾！")
        print("請在桌面上建立一個名為『英文單字』的資料夾，並放入 .txt 檔。")
        input("按 Enter 結束程式...")
        exit()

    # 搜尋資料夾中的 .txt 檔案
    txt_files = [f for f in os.listdir(desktop_path) if f.endswith(".txt")]

    if not txt_files:
        print("⚠️ 『英文單字』資料夾中沒有找到任何 .txt 檔案！")
        input("按 Enter 結束程式...")
        exit()

    print("\n=== 請選擇要使用的文字檔 ===")
    for i, file in enumerate(txt_files, start=1):
        print(f"{i}. {file}")

    while True:
        choice = input("請輸入檔案編號：")
        if choice.isdigit() and 1 <= int(choice) <= len(txt_files):
            selected_file = txt_files[int(choice) - 1]
            full_path = os.path.join(desktop_path, selected_file)
            print(f"\n✅ 你選擇的檔案是：{selected_file}")
            return full_path
        else:
            print("❌ 輸入錯誤，請重新輸入！")


# === 主程式 ===
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("=== 單字測驗 ===")

    filename = choose_txt_from_desktop()
    word_dict = load_words(filename)

    print("\n請選擇測驗模式：")
    print("1️⃣ 英翻中")
    print("2️⃣ 中翻英")
    mode_choice = input("輸入 1 或 2：")

    if mode_choice == "1":
        quiz(word_dict, "en_to_ch")
    elif mode_choice == "2":
        quiz(word_dict, "ch_to_en")
    else:
        print("輸入錯誤，請重新執行！")


if __name__ == "__main__":
    main()

# 打包成exe
# cd C:\Users\ymca9\Desktop\code
# pyinstaller --onefile word.py
