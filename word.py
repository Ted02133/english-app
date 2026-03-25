import random
import os


# === 讀取單字檔 (修正空格問題) ===
def load_words(filename):
    word_dict = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # 使用 split(None, 1) 確保只切開第一個空格/定位點
                # 這樣 "binary tree 二元樹" 會切成 ["binary tree", "二元樹"]
                parts = line.split(None, 1)
                if len(parts) == 2:
                    eng, ch = parts
                    word_dict[eng.strip()] = ch.strip()
        return word_dict
    except FileNotFoundError:
        print(f"\n⚠️ 找不到檔案：{filename}")
        input("按 Enter 結束程式...")
        exit()


# === 顯示測驗結果 ===
def show_result(correct, wrong, wrong_list):
    os.system("cls" if os.name == "nt" else "clear")
    print("=== 測驗結束 ===")
    print(f"✅ 答對：{correct} 題")
    print(f"❌ 答錯：{wrong} 題\n")

    if wrong_list:
        print("以下是你答錯的題目：")
        for eng, ch in wrong_list:
            print(f"- {eng} = {ch}")
    else:
        print("🎉 全部答對！太棒了！")


# === 單字測驗 (修正自動跳題邏輯) ===
def quiz(word_dict, mode="en_to_ch"):
    words = list(word_dict.keys())
    random.shuffle(words)
    correct = 0
    wrong = 0
    wrong_list = []
    total = len(words)

    for i, word in enumerate(words, start=1):
        # 每題開始直接清屏，保持畫面乾淨
        os.system("cls" if os.name == "nt" else "clear")
        print(f"進度：{i}/{total} | 正確：{correct} | 錯誤：{wrong}")
        print("-" * 30)

        if mode == "en_to_ch":
            ans = input(f"題目：{word}\n請輸入中文意思：").strip()
            if ans.lower() == "exit":
                break

            if ans == word_dict[word]:
                correct += 1
                # 答對了：不印任何訊息，直接進入下一個迴圈(即下一題)
            else:
                print(f"\n❌ 錯誤！正確答案是：{word_dict[word]}")
                input("\n按 Enter 鍵繼續下一題...")  # 只有錯的時候才停下來
                wrong += 1
                wrong_list.append((word, word_dict[word]))

        elif mode == "ch_to_en":
            ans = input(f"題目：{word_dict[word]}\n請輸入英文單字：").strip()
            if ans.lower() == "exit":
                break

            if ans.lower() == word.lower():
                correct += 1
                # 答對了：直接跳下一題
            else:
                print(f"\n❌ 錯誤！正確答案是：{word}")
                input("\n按 Enter 鍵繼續下一題...")
                wrong += 1
                wrong_list.append((word, word_dict[word]))

    show_result(correct, wrong, wrong_list)

    if wrong_list:
        again = input("\n要重練錯題嗎？(y/n)：")
        if again.lower() == "y":
            quiz(dict(wrong_list), mode)


# === 選擇桌面上的 txt 檔 ===
def choose_txt_from_desktop():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "英文單字")
    if not os.path.exists(desktop_path):
        print(f"⚠️ 找不到資料夾：{desktop_path}")
        input("按 Enter 結束...")
        exit()

    txt_files = [f for f in os.listdir(desktop_path) if f.endswith(".txt")]
    if not txt_files:
        print("⚠️ 資料夾內沒有 .txt 檔")
        input("按 Enter 結束...")
        exit()

    print("\n=== 請選擇單字檔 ===")
    for i, file in enumerate(txt_files, start=1):
        print(f"{i}. {file}")

    while True:
        choice = input("\n請輸入編號：")
        if choice.isdigit() and 1 <= int(choice) <= len(txt_files):
            return os.path.join(desktop_path, txt_files[int(choice) - 1])
        print("❌ 輸入錯誤！")


def main():
    filename = choose_txt_from_desktop()
    word_dict = load_words(filename)

    print("\n1. 英翻中 | 2. 中翻英")
    mode_choice = input("請選擇：")
    mode = "en_to_ch" if mode_choice == "1" else "ch_to_en"

    quiz(word_dict, mode)
    print("\n👋 感謝使用！")


if __name__ == "__main__":
    main()
