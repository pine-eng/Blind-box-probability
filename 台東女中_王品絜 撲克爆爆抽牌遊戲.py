import tkinter as tk
from tkinter import messagebox
import random

#一次抽一張牌
def draw_one_card():
    if not deck:
        messagebox.showinfo("提示", "牌堆抽完！")
        return
    draw_cards_loop([deck.pop()])

# 遊戲資料初始化
deck = list(range(1, 14)) * 2
random.shuffle(deck)
player_score = 0
target_pile = []
items = []

# 道具效果
def add_score(points):
    global player_score
    player_score += points
    update_display()

item_effects = {
    "重洗牌": lambda: random.shuffle(deck),
    "幸運卡": lambda: add_score(random.randint(5, 15)),
    "爆爆卡": lambda:add_score(random.randint(-15, 25)),
    "爆牌護身符": lambda: enable_skip_bust(),
}

skip_next_bust = False

def enable_skip_bust():
    global skip_next_bust
    skip_next_bust = True
    messagebox.showinfo("道具效果", "下次爆牌不扣分！")

# GUI 初始化
root = tk.Tk()
root.title("撲克爆爆")
root.geometry("600x400")

score_var = tk.StringVar()
score_label = tk.Label(root, textvariable=score_var, font=("Arial", 16))
score_label.pack(pady=5)

deck_frame = tk.Frame(root)
deck_frame.pack(pady=5)
deck_var = tk.StringVar()
deck_label = tk.Label(deck_frame, textvariable=deck_var, font=("Arial", 12))
deck_label.pack(side="left", padx=10)
tk.Label(deck_frame, text="牌堆", font=("Arial", 12)).pack(side="left")

target_frame = tk.Frame(root)
target_frame.pack(pady=10)
target_label = tk.Label(target_frame, text="目標堆：", font=("Arial", 12))
target_label.pack(side="left")
target_cards_frame = tk.Frame(target_frame)
target_cards_frame.pack(side="left")

items_var = tk.StringVar()
items_label = tk.Label(root, textvariable=items_var, font=("Arial", 12))
items_label.pack(pady=5)


# 顯示更新函式
def update_display():
    score_var.set(f"分數：{player_score}")
    deck_var.set(f"牌堆剩餘：{len(deck)} 張")
    items_var.set(f"道具：{items if items else '（無）'}")
    # 更新目標堆牌圖示
    for widget in target_cards_frame.winfo_children():
        widget.destroy()
    for card in target_pile:
        lbl = tk.Label(target_cards_frame, text=str(card), bg="lightblue",
                       width=3, height=2, relief="raised", font=("Arial", 12))
        lbl.pack(side="left", padx=2)


# 抽牌動畫（迴圈版）
def draw_cards_loop(cards_to_draw):
    if not cards_to_draw:
        return
    card = cards_to_draw.pop(0)

    # 抽到13將重置遊戲
    if card == 13:
        messagebox.showinfo("刷新遊戲", "抽到 13，遊戲重置！")
        end_game()
        return

    # 升序判定
    if target_pile and card < target_pile[-1]:
        global skip_next_bust, player_score
        if skip_next_bust:
            skip_next_bust = False
            messagebox.showwarning("保護生效", f"牌 {card} 小於頂牌，保護生效！")
        else:
            player_score = 0
            messagebox.showwarning("爆牌！", f"牌 {card} 小於頂牌，分數歸零！")
            update_display()
            return

    # 顯示牌背
    card_back = tk.Label(target_cards_frame, text="?", bg="gray", width=3, height=2, relief="raised")
    card_back.pack(side="left", padx=2)

    # 延遲翻牌
    def reveal():
        target_pile.append(card)
        card_back.config(text=str(card), bg="lightblue")
        global player_score
        player_score += card

        # 隨機獲得道具
        if random.random() < 0.3:
            item = random.choice(list(item_effects.keys()))
            items.append(item)
            messagebox.showinfo("獲得道具", f"你獲得了「{item}」！")

        update_display()
        draw_cards_loop(cards_to_draw)  # 遞迴處理下一張牌

    root.after(300, reveal)  # 0.3秒翻牌延遲

# 使用道具
def use_item():
    global skip_next_bust
    if not items:
        messagebox.showinfo("提示", "你沒有道具")
        return

    item_win = tk.Toplevel(root)
    item_win.title("使用道具")
    tk.Label(item_win, text="選擇道具：").pack(pady=5)

    for it in items[:]:  # 用拷貝避免迴圈中刪除錯誤
        def use_this(item=it):
            items.remove(item)
            item_effects[item]()
            messagebox.showinfo("使用道具", f"使用了 {item}！")
            item_win.destroy()
            update_display()

        tk.Button(item_win, text=it, width=12, command=use_this).pack(pady=2)


# 結束遊戲
def end_game():
    messagebox.showinfo("遊戲結束", f"最終分數：{player_score}\n目標堆：{target_pile}\n剩餘道具：{items if items else '（無）'}")
    root.destroy()


# 按鈕介面
button_frame = tk.Frame(root) 
button_frame.pack(pady=15)
tk.Button(button_frame, text="抽牌", width=12, command=draw_one_card).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="使用道具", width=12, command=use_item).grid(row=0, column=1, padx=5)
tk.Button(root, text="結束遊戲", width=12, command=end_game).pack(side="bottom", pady=10)

# 啟動遊戲
update_display()
root.mainloop()
