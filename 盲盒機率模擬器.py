import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- 中文化字型設定 ---
# Windows 使用 'Microsoft JhengHei' (微軟正黑體)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False # 解決負號顯示問題

def run_simulation():
    try:
        # 取得使用者輸入的分母
        denominator = float(entry_chance.get())
        if denominator <= 0:
            raise ValueError
            
        p = 1 / denominator
        theoretical_ev = denominator # 理論期望值 E = 1/p
        iterations = 10000
        
        # 執行蒙地卡羅模擬
        results = []
        for _ in range(iterations):
            count = 0
            while True:
                count += 1
                if random.random() < p:
                    break
            results.append(count)
        
        simulated_ev = np.mean(results)
        error = abs(simulated_ev - theoretical_ev) / theoretical_ev * 100
        
        # 更新文字標籤
        label_theory.config(text=f"理論期望值：{theoretical_ev:.2f} 次")
        label_sim.config(text=f"模擬平均值：{simulated_ev:.2f} 次")
        label_error.config(text=f"數據誤差率：{error:.4f} %", fg="#D32F2F" if error > 1 else "#388E3C")
        
        # 繪製幾何分布圖表
        ax.clear()
        
        # 繪製模擬結果的直方圖
        max_val = int(np.percentile(results, 95)) # 取 95% 的數據範圍讓圖表好看
        bins = np.arange(1, max_val + 2) - 0.5 
        ax.hist(results, bins=bins, density=True, alpha=0.6, color='#2196F3', label='模擬數據 (10,000次)')
        
        # 繪製幾何分布的理論 PMF 曲線
        x = np.arange(1, max_val + 1)
        pmf = ((1 - p) ** (x - 1)) * p
        ax.plot(x, pmf, 'r-o', markersize=3, linewidth=1, label='理論幾何分布')
        
        # 設定中文標籤
        ax.set_title(f"幾何分布驗證 (中獎機率 1/{int(denominator)})")
        ax.set_xlabel("需要抽取的次數 (k)")
        ax.set_ylabel("出現機率 (P)")
        ax.legend() # 顯示圖例
        
        # 刷新畫布
        canvas.draw()
        
    except ValueError:
        messagebox.showerror("格式錯誤", "請輸入有效的大於 0 的數字")

# 主視窗設定
root = tk.Tk()
root.title("幾何分布模擬器")
root.geometry("650x750") 
root.configure(padx=20, pady=10)

# 標題與輸入區
tk.Label(root, text="盲盒機率模擬與幾何分布視覺化", font=("Arial", 14, "bold")).pack(pady=5)
tk.Label(root, text="輸入隱藏款機率分母 (1/x):").pack()
entry_chance = tk.Entry(root, justify='center')
entry_chance.insert(0, "72")
entry_chance.pack(pady=5)

# 執行按鈕
btn_run = tk.Button(root, text="執行模擬並繪製圖表", command=run_simulation, 
                    bg="#0B2596", fg="white", font=("Arial", 10, "bold"))
btn_run.pack(pady=10)

# 結果顯示區
label_theory = tk.Label(root, text="理論期望值：--", font=("Courier", 10))
label_theory.pack()
label_sim = tk.Label(root, text="模擬平均值：--", font=("Courier", 10))
label_sim.pack()
label_error = tk.Label(root, text="數據誤差率：--", font=("Courier", 10, "bold"))
label_error.pack(pady=5)

# Matplotlib 圖表嵌入
fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.mainloop()