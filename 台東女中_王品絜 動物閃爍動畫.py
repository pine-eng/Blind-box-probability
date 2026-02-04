#製作互動動畫，輸入喜好動物利用ASCII藝術創作和小視窗呈現圖案
import time
import os
import tkinter as tk

# 收集個人資訊
name = input("請問你的名字：")
favorite_animal = input("請問你最喜歡的動物：")

# 貓(動畫版)
def blinking_cat():
    open_eyes = [
        "     /\\_/\\  ",
        "    ( o.o ) ",
        "     > ^ <  "
    ]

    closed_eyes = [
        "     /\\_/\\  ",
        "    ( -.- ) ",
        "     > ^ <  "
    ]

    for _ in range(4):
        os.system('cls' if os.name == 'nt' else 'clear')  # 清屏
        for line in open_eyes:
            print(line)
        time.sleep(1)

        os.system('cls' if os.name == 'nt' else 'clear')
        for line in closed_eyes:
            print(line)
        time.sleep(0.3)

# 貓（粉色小視窗）
def cat_window():
    root = tk.Tk()
    root.title("粉色小貓")
    root.configure(bg="#FFE6FF")

    cat = """     /\\_/\\  
    ( o.o ) 
     > ^ <  """

    label = tk.Label(
        root,
        text=cat,
        font=("Courier", 20),
        bg="#FFE6FF",
        fg="black",
        justify="left"
    )
    label.pack(padx=20, pady=20)
    root.mainloop()

# 狗(飄移版)
def get_dog_ascii():
    return [
"            /    \\__",
"|\\         /    @   \\",
"\\ \\_______|    \\  .:|>",
" \\      ##|    | \\__/",
"  |    ####\\__/   \\",
"  /  /  ##       \\|",
" /  /__________\\  \\",
" L_JJ           \\__JJ"
]
# 走路
def walk_dog():
    dog = get_dog_ascii()
    for i in range(30):  # 走30步
        os.system('cls' if os.name == 'nt' else 'clear')
        space = " " * i  #一步多一格空白
        for line in dog:
            print(space + line)
        time.sleep(0.2)
# 隱藏版章魚哥
def octopus_a():
    octopus = [
        "   .--'''''''''--.",
        " .'      .---.      '.",
        "/    .-----------.    \\",
        "/        .-----.        \\",
        "|       .-.   .-.       |",
        "|      /   \\ /   \\      |",
        "|     | .-. | .-. |     |",
        "\\     | |_| | |_| |     /",
        " '-._|     |     |_.-'",
        "     | '-' | '-' |",
        "      \\___/ \\___/",
        "    _.-'  /   \\  `-._",
        "  .' _.--|     |--._ '.",
        " ' _...-|     |-..._ '",
        "       |     |",
        "       '.___.'",
        "         | |",
        "        _| |_",
        "       /\\( )/\\",
        "      /  ` '  \\",
        "     | |     | |",
        "     '-'     '-'",
        "     | |     | |",
        "     | |     | |",
        "     | |-----| |",
        "  .`/  |     | |/`.",
        "  |    |     |    |",
        "  '._.'| .-. |'._.'",
        "        \\ | /",
        "        | | |",
        "        | | |",
        "        | | |",
        "       /| | |\\",
        "     .'_| | |_`.",
        "     `. | | | .'",
        "      .   / \\   .",
        "  /o`.-'  / \\  `-.`o\\",
        " /o  o\\ .'   `. /o  o\\",
        " `.___.'       `.___.'"
    ]
    for line in octopus:
        print(line)
# 判斷解鎖
if favorite_animal == "貓":
    print("繪製咪咪中...")
    choice = input("要看哪種咪咪？(1=動畫版，2=粉色小視窗)：")
    if choice == "1":
        blinking_cat()
    elif choice == "2":
        cat_window()
    else:
        print("輸入錯誤，預設播放動畫版！")
        blinking_cat()

elif favorite_animal == "狗":
    print("繪製狗狗中...")
    walk_dog()

else:
    print(f"目前還沒有 {favorite_animal} 的圖案，要不要解鎖？ 🔒")
    choice = input("有隱藏版喔！(1=要，2=nono)：")
    if choice == "1":
        print("繪製章魚哥中...")
        octopus_a()
    elif choice == "2":
        print("繪製製作者最喜歡的狗狗中...")
        walk_dog()
    else:
        print("輸入錯誤，預設製作者最喜歡的狗狗！")
        walk_dog()
# 最後輸出
time.sleep(1)
print(f"\n{name}的{favorite_animal}完成啦！")

# 獲取當前時間
current_time = time.time()
print("目前時間戳：", current_time)

# 格式化時間顯示(動畫製作好的時間)
formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
print("現在時間：", formatted_time)