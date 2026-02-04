import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

#功能函式
def temperature_conversion():
    try:
        celsius = float(entry_temp.get())
        fahrenheit = (celsius * 9/5) + 32
        messagebox.showinfo("結果", f"攝氏 {celsius:.2f}°C = 華氏 {fahrenheit:.2f}°F")
    except ValueError:
        messagebox.showerror("錯誤", "請輸入正確的數字！")

def bmi_calculation():
    try:
        height = float(entry_height.get()) / 100
        weight = float(entry_weight.get())
        bmi = weight / (height ** 2)
        result = f"您的 BMI 值為：{bmi:.2f}\n"
        if bmi < 18.5:
            result += "體重過輕"
        elif 18.5 <= bmi < 24:
            result += "正常範圍"
        elif 24 <= bmi < 27:
            result += "過重"
        else:
            result += "肥胖"
        messagebox.showinfo("結果", result)
    except ValueError:
        messagebox.showerror("錯誤", "請輸入正確的數字！")

def age_calculation():
    try:
        birth_year = int(entry_year.get())
        current_year = datetime.now().year
        age = current_year - birth_year
        if age < 0:
            messagebox.showerror("錯誤", "年份輸入不合理！")
        else:
            messagebox.showinfo("結果", f"您今年大約 {age} 歲")
    except ValueError:
        messagebox.showerror("錯誤", "請輸入有效的年份！")

#介面
root = tk.Tk()
root.title("智慧生活助手")
root.geometry("400x300")

#分頁系統
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

#分頁1：溫度轉換
frame_temp = ttk.Frame(notebook)
notebook.add(frame_temp, text="溫度轉換")

tk.Label(frame_temp, text="攝氏溫度：").pack(pady=5)
entry_temp = tk.Entry(frame_temp)
entry_temp.pack()
tk.Button(frame_temp, text="轉換 C → F", command=temperature_conversion).pack(pady=10)

#分頁2：BMI 計算
frame_bmi = ttk.Frame(notebook)
notebook.add(frame_bmi, text="BMI 計算")

tk.Label(frame_bmi, text="身高 (cm)：").pack(pady=5)
entry_height = tk.Entry(frame_bmi)
entry_height.pack()
tk.Label(frame_bmi, text="體重 (kg)：").pack(pady=5)
entry_weight = tk.Entry(frame_bmi)
entry_weight.pack()
tk.Button(frame_bmi, text="計算 BMI", command=bmi_calculation).pack(pady=10)

#分頁3：年齡計算
frame_age = ttk.Frame(notebook)
notebook.add(frame_age, text="年齡計算")

tk.Label(frame_age, text="出生年份：").pack(pady=5)
entry_year = tk.Entry(frame_age)
entry_year.pack()
tk.Button(frame_age, text="計算年齡", command=age_calculation).pack(pady=10)

#退出按鈕（放在主視窗底部）
tk.Button(root, text="退出", command=root.quit, fg="#EC3D94").pack(pady=15)

root.mainloop()



import tkinter as tk
from PIL import Image, ImageTk

# -----------------------------
# 精靈圖設定
# -----------------------------
sprite_sheet = Image.open("卡比比.png")
frame_width, frame_height = 64, 69  # 每格大小
cols = 8                             # 每排有幾張

# 載入精靈圖
sprite_sheet = Image.open(sprite_path)
total_rows = sprite_sheet.height // frame_height

# 切割成單格
frames = []
for row in range(total_rows):
    for col in range(cols):
        left = col * frame_width
        upper = row * frame_height
        right = left + frame_width
        lower = upper + frame_height
        frame = sprite_sheet.crop((left, upper, right, lower))
        frames.append(ImageTk.PhotoImage(frame))

# -----------------------------
# Tkinter 視窗
# -----------------------------
root = tk.Tk()
root.title("卡比比動畫")
canvas = tk.Canvas(root, width=frame_width, height=frame_height)
canvas.pack()

# -----------------------------
# 動畫函數
# -----------------------------
current_frame = 0
image_id = canvas.create_image(0, 0, anchor='nw', image=frames[0])

def animate():
    global current_frame
    current_frame = (current_frame + 1) % len(frames)
    canvas.itemconfig(image_id, image=frames[current_frame])
    root.after(100, animate)  # 每 100ms 更新一次

animate()
root.mainloop()
