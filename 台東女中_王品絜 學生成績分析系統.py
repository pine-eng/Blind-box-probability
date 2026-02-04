import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt

class ScoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("學生成績分析系統")
        self.root.geometry("650x500")

        self.final_result = None
        self.midterm_df = None
        self.final_df = None

        ttk.Label(root, text="學生成績分析系統", font=("Arial", 20)).pack(pady=10)

        ttk.Button(root, text="載入成績 CSV", command=self.load_csv).pack(pady=10)
        ttk.Button(root, text="執行分析", command=self.analyze_scores).pack(pady=10)
        ttk.Button(root, text="查詢學生成績", command=self.search_student).pack(pady=10)
        ttk.Button(root, text="繪製圖表", command=self.plot_menu).pack(pady=10)
        ttk.Button(root, text="離開", command=root.quit).pack(pady=20)

    # 載入 CSV
    def load_csv(self):
        paths = filedialog.askopenfilenames(title="選擇成績 CSV（一次或兩次）", filetypes=[("CSV files","*.csv")])
        if not paths:
            return

        if len(paths) == 1:
            self.midterm_df = pd.read_csv(paths[0], dtype={"學號": str})
            for col in ["國文","英文","數學","自然","社會"]:
                self.midterm_df[col] = pd.to_numeric(self.midterm_df[col], errors="coerce")
            self.final_df = None
            messagebox.showinfo("完成", f"已載入單次成績: {paths[0].split('/')[-1]}")
        elif len(paths) == 2:
            self.midterm_df = pd.read_csv(paths[0], dtype={"學號": str})
            self.final_df = pd.read_csv(paths[1], dtype={"學號": str})
            for col in ["國文","英文","數學","自然","社會"]:
                self.midterm_df[col] = pd.to_numeric(self.midterm_df[col], errors="coerce")
                self.final_df[col] = pd.to_numeric(self.final_df[col], errors="coerce")
            messagebox.showinfo("完成", f"已載入兩次成績: {paths[0].split('/')[-1]}, {paths[1].split('/')[-1]}")
        else:
            messagebox.showerror("錯誤", "最多只能選擇兩個 CSV")

    # 分析成績
    def analyze_scores(self):
        if self.midterm_df is None:
            messagebox.showerror("錯誤", "請先載入至少一個 CSV")
            return

        subjects = ["國文","英文","數學","自然","社會"]

        mid = self.midterm_df.copy()
        mid["總分"] = mid[subjects].sum(axis=1)
        mid["排名"] = mid["總分"].rank(ascending=False).astype(int)

        if self.final_df is None:
            result = mid
            messagebox.showinfo("完成", "單次考試分析完成")
        else:
            final = self.final_df.copy()
            final["總分"] = final[subjects].sum(axis=1)
            final["排名"] = final["總分"].rank(ascending=False).astype(int)
            result = mid.merge(final, on=["學號","姓名"], suffixes=("_期中","_期末"))
            result["總分進步"] = result["總分_期末"] - result["總分_期中"]
            messagebox.showinfo("完成", "期中+期末分析完成")

        # 儲存分析結果 CSV (數字右對齊)
        df_save = result.copy()
        num_cols = [col for col in df_save.columns if col not in ["學號","姓名"]]
        for col in num_cols:
            df_save[col] = df_save[col].apply(lambda x: f"{x:>6.1f}")
        df_save.to_csv("成績分析結果.csv", index=False, encoding="utf-8-sig")

        self.final_result = result

    # 查詢學生
    def search_student(self):
        if self.final_result is None:
            messagebox.showerror("錯誤", "尚未分析成績")
            return

        win = tk.Toplevel(self.root)
        win.title("查詢學生")
        win.geometry("450x300")

        ttk.Label(win, text="輸入學號：").pack()
        entry = ttk.Entry(win)
        entry.pack()

        def search():
            sid = entry.get().strip()
            student = self.final_result[self.final_result["學號"] == sid]
            if student.empty:
                messagebox.showerror("錯誤", "找不到該學生")
            else:
                df_display = student.copy()
                num_cols = [col for col in df_display.columns if col not in ["學號","姓名"]]
                for col in num_cols:
                    df_display[col] = df_display[col].apply(lambda x: f"{x:>6.1f}")
                info = df_display.to_string(index=False, justify="right")
                messagebox.showinfo("成績", info)

        ttk.Button(win, text="查詢", command=search).pack(pady=10)

    # 圖表選單
    def plot_menu(self):
        if self.final_result is None:
            messagebox.showerror("錯誤", "尚未分析成績")
            return

        win = tk.Toplevel(self.root)
        win.title("圖表選單")
        win.geometry("300x300")

        ttk.Button(win, text="各科平均長條圖", command=self.plot_subject_mean).pack(pady=10)
        ttk.Button(win, text="總分排行榜", command=self.plot_total_rank).pack(pady=10)
        if self.final_df is not None:
            ttk.Button(win, text="總分進步趨勢圖", command=self.plot_improve).pack(pady=10)

    # 各科平均長條圖
    def plot_subject_mean(self):
        if self.final_df is None:
            subjects = ["國文","英文","數學","自然","社會"]
            mean_values = self.final_result[subjects].mean()
        else:
            subjects = ["國文_期末","英文_期末","數學_期末","自然_期末","社會_期末"]
            mean_values = self.final_result[subjects].mean()

        mean_values.plot(kind="bar")
        plt.ylabel("平均分數")
        plt.title("各科平均成績")
        plt.show()

    # 總分排行榜
    def plot_total_rank(self):
        if self.final_df is None:
            df = self.final_result.sort_values("總分", ascending=False)
            plt.bar(df["姓名"], df["總分"])
            plt.title("學生總分排行榜")
        else:
            df = self.final_result.sort_values("總分_期末", ascending=False)
            plt.bar(df["姓名"], df["總分_期末"])
            plt.title("學生總分排行榜（期末）")
        plt.xticks(rotation=45)
        plt.ylabel("總分")
        plt.show()

    # 總分進步趨勢圖
    def plot_improve(self):
        if self.final_df is None:
            messagebox.showerror("錯誤", "只有兩次考試才有進步趨勢圖")
            return
        df = self.final_result
        plt.plot(df["姓名"], df["總分進步"], marker="o")
        plt.xticks(rotation=45)
        plt.ylabel("分數差")
        plt.title("學生總分進步趨勢")
        plt.show()

# 主程式
root = tk.Tk()
app = ScoreApp(root)
root.mainloop()
