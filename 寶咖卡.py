# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import random, os, sys, json
import pygame

# 處理檔案路徑
if getattr(sys, 'frozen', False):
    BASE = sys._MEIPASS
else:
    BASE = os.path.dirname(os.path.abspath(__file__))

class BaoKaKaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 寶咖卡：地鼠卡比大挑戰")
        self.root.geometry("600x950")
        self.root.configure(bg="#000000")
        
        # 1. 音樂與資料初始化
        pygame.mixer.init()
        self.play_bgm("b.mp3")
        
        self.save_file = "game_save.json"
        self.user_name = "冒險者"
        self.difficulty = tk.StringVar(value="Normal")
        self.load_data()
        
        # 2. 資源列表
        self.gif_frames = {"capoo_walk":[], "capoo_atk":[], "kirby_walk":[], "kirby_bw":[], "capoo_side":[]}
        self.grid_rects = [[None for _ in range(3)] for _ in range(3)]
        self.current_frame_idx = 0
        self.is_attacking = False
        self.game_running = False
        self.gacha_running = False
        self.mole_pos = [1, 1]
        self.is_black_white = False
        
        # 扭蛋獎項池
        self.prizes_pool = ["神級卡比盾", "狂暴咖波爪", "雙倍金幣卡", "幸運餅乾", "空氣獎" , "特大獎：咖波肉包"]
        
        self.init_resources()
        self.show_main_menu()
        self.animate_loop()

    # 基礎工具
    def play_bgm(self, filename):
        path = os.path.join(BASE, filename)
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(-1)
            except: pass

    def load_gif_frames(self, filename, size=(110, 110), make_bw=False):
        if not filename.endswith(".gif"): filename += ".gif"
        path = os.path.join(BASE, filename)
        if not os.path.exists(path): return []
        frames = []
        img = Image.open(path)
        try:
            while True:
                frame = img.copy().convert("RGBA").resize(size)
                if make_bw:
                    r, g, b, a = frame.split()
                    bw = ImageOps.grayscale(frame.convert("RGB"))
                    frame = Image.merge("RGBA", (bw, bw, bw, a))
                frames.append(ImageTk.PhotoImage(frame))
                img.seek(len(frames))
        except EOFError: pass
        return frames

    def init_resources(self):
        self.gif_frames["capoo_walk"] = self.load_gif_frames("capoo_walk")
        self.gif_frames["capoo_atk"] = self.load_gif_frames("capoo_atk")
        self.gif_frames["kirby_walk"] = self.load_gif_frames("kirby_walk")
        self.gif_frames["kirby_bw"] = self.load_gif_frames("kirby_walk", make_bw=True)
        self.gif_frames["capoo_side"] = self.load_gif_frames("capoo_side", (150, 150))

    def clear_screen(self):
        for w in self.root.winfo_children(): w.destroy()

    #畫面切換：主選單
    def show_main_menu(self):
        self.game_running = self.gacha_running = False
        self.clear_screen()
        
        tk.Label(self.root, text="🐾 寶 咖 卡 🐾", font=("微軟正黑體", 45, "bold"), fg="#F0CCF0", bg="#000000").pack(pady=60)
        
        login_f = tk.Frame(self.root, bg="#000000")
        login_f.pack(pady=10)
        tk.Label(login_f, text="冒險者登入:", font=("微軟正黑體", 12), fg="white", bg="#000000").pack(side="left")
        self.name_input = tk.Entry(login_f, font=("微軟正黑體", 14), width=15)
        self.name_input.insert(0, self.user_name)
        self.name_input.pack(side="left", padx=10)

        diff_f = tk.LabelFrame(self.root, text=" 難度選擇 ", font=("微軟正黑體", 12), fg="#AD5EF6", bg="#000000", padx=15, pady=15)
        diff_f.pack(pady=20)
        for t, v in [("簡單", "Easy"), ("普通", "Normal"), ("困難", "Hard")]:
            tk.Radiobutton(diff_f, text=t, variable=self.difficulty, value=v, bg="#000000", fg="#AD5EF6", font=("微軟正黑體", 12), selectcolor="#222").pack(side="left", padx=15)

        tk.Button(self.root, text="開始冒險 (Login)", font=("微軟正黑體", 18, "bold"), bg="#AD5EF6", fg="white", width=18, command=self.press_start).pack(pady=15)
        tk.Button(self.root, text="扭蛋機", font=("微軟正黑體", 14), bg="#444444", fg="white", width=18, command=self.show_gacha).pack()
        
        tk.Label(self.root, text=f"最高紀錄: {self.high_score} | 金幣: {self.coins}", fg="gray", bg="#000000").pack(side="bottom", pady=20)

    def press_start(self):
        self.user_name = self.name_input.get() if self.name_input.get() else "冒險者"
        self.start_game()

    #畫面切換：遊戲內容
    def start_game(self):
        self.clear_screen()
        self.reset_game_data()
        self.game_running = True
        
        tk.Label(self.root, text=f"👤 {self.user_name} | 難度: {self.difficulty.get()}", font=("微軟正黑體", 12), fg="#F0CCF0", bg="#000000").pack(pady=5)
        self.can = tk.Canvas(self.root, width=450, height=450, bg="#050505", highlightthickness=2, highlightbackground="#333")
        self.can.pack(pady=10)
        
        self.ui_info = tk.Label(self.root, text="", font=("Arial Black", 18), fg="#F0CCF0", bg="#000000")
        self.ui_info.pack()
        self.hp_bar = ttk.Progressbar(self.root, length=400); self.hp_bar.pack(pady=20)
        
        self.auto_move_mole()
        self.game_tick()
        self.root.bind("<Key>", self.handle_key)

    def flash_square_effect(self):
        """ 目前所在的方格閃爍 """
        x, y = self.pos
        rect_id = self.grid_rects[x][y]
        if rect_id:
            self.can.itemconfig(rect_id, fill="#F0CCF0")
            self.root.after(100, lambda: self.can.itemconfig(rect_id, fill="#180818"))

    def handle_key(self, e):
        if not self.game_running: return
        k = e.keysym.lower()
        m = {'w':(0,-1), 's':(0,1), 'a':(-1,0), 'd':(1,0)}
        if k in m:
            self.pos[0] = max(0, min(2, self.pos[0] + m[k][0]))
            self.pos[1] = max(0, min(2, self.pos[1] + m[k][1]))
        elif k == 'space':
            self.flash_square_effect()
            self.attack()

    def attack(self):
        if self.is_attacking: return
        self.is_attacking = True
        if self.pos == self.mole_pos:
            if self.is_black_white: self.hp -= 50
            else: self.score += 1; self.coins += 10; self.mole_pos = [-1,-1]
        else: self.hp -= 5
        self.root.after(300, lambda: setattr(self, 'is_attacking', False))

    #畫面切換：遊戲結束
    def show_game_over(self):
        self.game_running = False
        self.clear_screen()
        if self.score > self.high_score: self.high_score = self.score
        self.save_data()
        
        tk.Label(self.root, text="挑戰結束", font=("微軟正黑體", 36, "bold"), fg="#FF4444", bg="#000000").pack(pady=80)
        tk.Label(self.root, text=f"冒險者: {self.user_name}\n最終得分: {self.score}", font=("微軟正黑體", 20), fg="white", bg="#000000").pack(pady=20)
        
        tk.Button(self.root, text="再來一局 (Retry)", font=("微軟正黑體", 18, "bold"), bg="#AD5EF6", fg="white", width=15, command=self.start_game).pack(pady=10)
        tk.Button(self.root, text="回主選單", font=("微軟正黑體", 14), bg="#444444", fg="white", width=15, command=self.show_main_menu).pack()

    #畫面切換：扭蛋機 (文字跳動滾動)
    def show_gacha(self):
        self.clear_screen()
        self.gacha_running = True
        tk.Label(self.root, text="🎰 寶咖卡：幸運扭蛋機 🎰", font=("微軟正黑體", 28, "bold"), fg="#F0CCF0", bg="#000000").pack(pady=50)
        
        self.gacha_can = tk.Canvas(self.root, width=160, height=160, bg="#000000", highlightthickness=0); self.gacha_can.pack()
        self.coin_label = tk.Label(self.root, text=f"金幣: {self.coins}", font=("微軟正黑體", 16), fg="cyan", bg="#000000"); self.coin_label.pack()
        
        self.gacha_res = tk.Label(self.root, text="期待抽到什麼呢？", font=("微軟正黑體", 16), fg="#F0CCF0", bg="#111111", width=25, height=2)
        self.gacha_res.pack(pady=30)
        
        tk.Button(self.root, text=" 抽取 (50 幣) ", font=("微軟正黑體", 16, "bold"), bg="#AD5EF6", fg="white", command=self.do_gacha).pack(pady=10)
        tk.Button(self.root, text="返回選單", font=("微軟正黑體", 12), bg="#444444", fg="white", command=self.show_main_menu).pack(pady=20)

    def do_gacha(self):
        if self.coins < 50: 
            self.gacha_res.config(text="❌ 金幣不足！", fg="red")
            return
        self.coins -= 50
        self.save_data()
        self.coin_label.config(text=f"金幣: {self.coins}")
        
        final_prize = random.choice(self.prizes_pool)
        self.animate_text_rolling(final_prize, 0)

    def animate_text_rolling(self, final_text, step):
        """ 文字隨機跳動變換動畫 """
        colors = ["#AD5EF6", "#00FFFF", "#FFD700", "#FF69B4", "#FFFFFF"]
        if step < 12:
            random_word = random.choice(self.prizes_pool)
            curr_c = random.choice(colors)
            display = f"🎲 {random_word} 🎲"
            self.gacha_res.config(text=display, fg=curr_c, font=("微軟正黑體", 16 + (step % 4)))
            
            delay = 50 + (step * 20) # 速度越來越慢
            self.root.after(delay, lambda: self.animate_text_rolling(final_text, step + 1))
        else:
            self.gacha_res.config(text=f"✨【 {final_text} 】✨", fg="#F0CCF0", font=("微軟正黑體", 20, "bold"))

    #遊戲驅動引擎
    def auto_move_mole(self):
        if not self.game_running: return
        cfg = {"Easy":(1800,0.2), "Normal":(1100,0.35), "Hard":(700,0.5)}.get(self.difficulty.get())
        self.mole_pos = [random.randint(0,2), random.randint(0,2)]
        self.is_black_white = random.random() < cfg[1]
        self.root.after(cfg[0], self.auto_move_mole)

    def update_game_display(self):
        if not hasattr(self, 'can'): return
        self.can.delete("all")
        s = 150
        for i in range(3):
            for j in range(3):
                bg_c = "#180818" if self.pos == [i,j] else "#050505"
                self.grid_rects[i][j] = self.can.create_rectangle(i*s, j*s, i*s+s, j*s+s, fill=bg_c, outline="#333")
        
        mk = "kirby_bw" if self.is_black_white else "kirby_walk"
        mf = self.gif_frames[mk]
        if mf: self.can.create_image(self.mole_pos[0]*s+75, self.mole_pos[1]*s+75, image=mf[self.current_frame_idx % len(mf)])
        
        pk = "capoo_atk" if self.is_attacking else "capoo_walk"
        pf = self.gif_frames[pk]
        if pf: self.can.create_image(self.pos[0]*s+75, self.pos[1]*s+75, image=pf[self.current_frame_idx % len(pf)])
        
        if self.is_black_white: self.can.create_text(225, 225, text="⛔ WAIT!", fill="red", font=("Arial Black", 40))
        self.ui_info.config(text=f"Score: {self.score} | Time: {self.time_left}s")
        self.hp_bar["value"] = (self.hp/200)*100

    def animate_loop(self):
        self.current_frame_idx += 1
        if self.game_running: self.update_game_display()
        elif self.gacha_running and hasattr(self, 'gacha_can'):
            self.gacha_can.delete("all")
            f = self.gif_frames["capoo_side"]
            if f: self.gacha_can.create_image(80, 80, image=f[self.current_frame_idx % len(f)])
        self.root.after(100, self.animate_loop)

    def game_tick(self):
        if self.game_running and self.time_left > 0 and self.hp > 0:
            self.time_left -= 1; self.root.after(1000, self.game_tick)
        elif self.game_running: self.show_game_over()

    def reset_game_data(self):
        self.hp, self.score, self.time_left, self.pos = 200, 0, 60, [1,1]

    def load_data(self):
        try:
            with open(self.save_file, "r") as f:
                d = json.load(f); self.high_score, self.coins = d.get("high_score", 0), d.get("coins", 0)
        except: self.high_score = self.coins = 0

    def save_data(self):
        with open(self.save_file, "w") as f:
            json.dump({"high_score": self.high_score, "coins": self.coins}, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = BaoKaKaApp(root)
    root.mainloop()