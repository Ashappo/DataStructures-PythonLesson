# -*- coding: utf-8 -*-
"""双人五子棋（tkinter 单文件版）

兼容性说明：
    - Python 3.5 及以上均可运行（未使用 f-string 等新语法）；
    - 仅使用 Python 内置 tkinter，Windows / macOS 均可直接运行，
      无需安装任何第三方库；
    - 运行后弹出图形窗口，命令行保持安静是正常现象。

玩法：
    1. 黑棋先行，鼠标左键点击棋盘交叉点落子，黑白交替；
    2. 横、竖、左斜、右斜任一方向连成五子即获胜并弹窗、计分；
    3. “悔棋”撤回上一步，“重置对局”清空棋盘与比分重新开始。

运行方法：
    python gomoku.py        （Windows）
    python3 gomoku.py       （macOS）
"""
import sys

# Python 2 环境下没有 tkinter 包，给出明确提示而不是闪退
try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    tk = None

# ---------------- 跨平台设置 ----------------
IS_MAC = sys.platform == "darwin"
IS_WIN = sys.platform == "win32"
# 界面字体：mac 用苹方，Windows 用微软雅黑，其他系统交给 Tk 自动回退
if IS_MAC:
    UI_FONT = "PingFang SC"
elif IS_WIN:
    UI_FONT = "微软雅黑"
else:
    UI_FONT = "Helvetica"

GRID = 15                                  # 棋盘 15×15 个交叉点
CELL = 40                                  # 网格间距（像素）
MARGIN = 30                                # 棋盘四周留白
SIZE = CELL * (GRID - 1)                   # 棋盘线总长：14×40 = 560
WIN_LEN = 5                                # 连子数
DIRS = ((0, 1), (1, 0), (1, 1), (1, -1))   # 横、竖、左斜、右斜 4 条轴线


class Gomoku(object):
    def __init__(self, root):
        self.root = root
        self.root.title("双人五子棋")
        self.root.geometry("700x720")     # 画布 620×620 + 顶部标签 + 底部按钮
        self.root.resizable(False, False)

        self.board = [[0] * GRID for _ in range(GRID)]   # 0 空 1 黑 2 白
        self.history = []                                # 悔棋栈
        self.now_player = 1                              # 当前玩家
        self.score = {1: 0, 2: 0}                        # 累计胜场
        self.game_over = False

        self._build_ui()
        self._draw_board()

        # 兼容性修复：部分 macOS 的 Tk（含 Tk 8.6.10+ 与 Tk 9.0）在窗口
        # 完全显示前绘制的内容可能不刷新，导致棋盘一片空白。
        # 这里等窗口显示完成后强制重绘一次，并短暂置顶防止被遮挡。
        self.root.update_idletasks()
        self.root.after(150, self._force_redraw)

    def _force_redraw(self):
        self._draw_board()
        self.root.lift()
        if IS_MAC:
            self.root.attributes("-topmost", True)
            self.root.after(300, lambda: self.root.attributes("-topmost", False))

    # ---------------- 界面 ----------------
    def _build_ui(self):
        top = tk.Frame(self.root)
        top.pack(pady=(10, 6))
        self.lbl_black = tk.Label(top, text="黑方：0 胜",
                                  font=(UI_FONT, 12, "bold"))
        self.lbl_black.pack(side=tk.LEFT, padx=14)
        self.lbl_turn = tk.Label(top, text="轮到：黑棋",
                                 font=(UI_FONT, 12), fg="#C0392B")
        self.lbl_turn.pack(side=tk.LEFT, padx=14)
        self.lbl_white = tk.Label(top, text="白方：0 胜",
                                  font=(UI_FONT, 12, "bold"))
        self.lbl_white.pack(side=tk.LEFT, padx=14)

        self.canvas = tk.Canvas(self.root, width=SIZE + 2 * MARGIN,
                                height=SIZE + 2 * MARGIN,
                                bg="#E9C08A", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        bottom = tk.Frame(self.root)
        bottom.pack(pady=10)
        tk.Button(bottom, text="悔棋", width=12,
                  command=self.undo).pack(side=tk.LEFT, padx=12)
        tk.Button(bottom, text="重置对局", width=12,
                  command=self.reset).pack(side=tk.LEFT, padx=12)

    def _draw_board(self):
        """重绘棋盘：网格线 + 星位 + 已有棋子"""
        self.canvas.delete("all")
        self.canvas.config(bg="#E9C08A")
        self.canvas.update_idletasks()
        for i in range(GRID):
            p = MARGIN + i * CELL
            self.canvas.create_line(MARGIN, p, MARGIN + SIZE, p)
            self.canvas.create_line(p, MARGIN, p, MARGIN + SIZE)
        for r, c in ((3, 3), (3, 11), (11, 3), (11, 11), (7, 7)):
            x, y = MARGIN + c * CELL, MARGIN + r * CELL
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="black")
        for r in range(GRID):
            for c in range(GRID):
                if self.board[r][c]:
                    self._draw_piece(r, c, self.board[r][c])

    def _draw_piece(self, r, c, color, outline="#333333"):
        x, y = MARGIN + c * CELL, MARGIN + r * CELL
        rad = CELL // 2 - 3
        self.canvas.create_oval(x - rad, y - rad, x + rad, y + rad,
                                fill=("black" if color == 1 else "white"),
                                outline=outline)

    # ---------------- 交互 ----------------
    def on_click(self, event):
        if self.game_over:
            return
        col = int(round((event.x - MARGIN) / float(CELL)))
        row = int(round((event.y - MARGIN) / float(CELL)))
        if not (0 <= row < GRID and 0 <= col < GRID):
            return
        # 容差判断：点得偏离交叉点太远则不落子
        x, y = MARGIN + col * CELL, MARGIN + row * CELL
        if abs(event.x - x) > CELL * 0.4 or abs(event.y - y) > CELL * 0.4:
            return
        if self.board[row][col] != 0:      # 禁止重复落子
            return
        self._place(row, col)

    def _place(self, row, col):
        self.board[row][col] = self.now_player
        self.history.append((row, col))
        self._draw_board()
        line = self.check_win(row, col)
        if line:
            self.game_over = True
            self.score[self.now_player] += 1
            for r, c in line:                    # 高亮获胜的连子
                self._draw_piece(r, c, self.board[r][c], outline="#E74C3C")
            self._update_labels()
            name = "黑棋" if self.now_player == 1 else "白棋"
            print("[计分] 黑 {0} : {1} 白".format(self.score[1], self.score[2]))
            messagebox.showinfo(
                "对局结束",
                "{0}五子连珠，获胜！\n当前比分  黑 {1} : {2} 白".format(
                    name, self.score[1], self.score[2]))
        else:
            self.now_player = 3 - self.now_player
            self._update_labels()

    def check_win(self, row, col):
        """通用胜负检测：沿 4 条轴线正反两向统计连续同色棋子，≥5 即胜"""
        color = self.board[row][col]
        for dr, dc in DIRS:
            line = [(row, col)]
            for sign in (1, -1):
                r, c = row + dr * sign, col + dc * sign
                while (0 <= r < GRID and 0 <= c < GRID
                       and self.board[r][c] == color):
                    line.append((r, c))
                    r += dr * sign
                    c += dc * sign
            if len(line) >= WIN_LEN:
                return line
        return None

    def undo(self):
        if self.game_over:
            messagebox.showwarning("提示", "本局已结束，请点击“重置对局”开始新的一局。")
            return
        if not self.history:
            messagebox.showinfo("提示", "当前还没有落子，无法悔棋。")
            return
        row, col = self.history.pop()
        self.board[row][col] = 0
        self.now_player = 3 - self.now_player
        self._draw_board()
        self._update_labels()

    def reset(self):
        self.board = [[0] * GRID for _ in range(GRID)]
        self.history.clear()
        self.now_player = 1
        self.score = {1: 0, 2: 0}
        self.game_over = False
        self._draw_board()
        self._update_labels()

    def _update_labels(self):
        self.lbl_black.config(text="黑方：{0} 胜".format(self.score[1]))
        self.lbl_white.config(text="白方：{0} 胜".format(self.score[2]))
        if self.game_over:
            self.lbl_turn.config(text="对局结束")
        else:
            name = "黑棋" if self.now_player == 1 else "白棋"
            self.lbl_turn.config(text="轮到：" + name)


def main():
    if IS_WIN:
        # Windows 高分屏下让界面清晰（老系统没有该接口时静默跳过）
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    root = tk.Tk()
    Gomoku(root)
    # 窗口居中显示
    root.update_idletasks()
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("+{0}+{1}".format(max((sw - 700) // 2, 0),
                                    max((sh - 720) // 3, 0)))
    root.mainloop()


if __name__ == "__main__":
    if tk is None:
        msg = "当前 Python 版本过旧（Python 2），请使用 Python 3 运行：python3 gomoku.py"
        sys.stderr.write(msg + "\n")
        try:
            input(msg + "，按回车键退出...")
        except Exception:
            pass
        sys.exit(1)
    try:
        main()
    except Exception:
        # 防闪退：任何启动错误都打印出来、写入日志，并停住窗口等待查看
        import os
        import time
        import traceback
        err = traceback.format_exc()
        sys.stderr.write("\n" + err + "\n")
        try:
            log = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "gomoku_error.log")
            with open(log, "a") as f:
                f.write(time.strftime("[%Y-%m-%d %H:%M:%S]\n") + err + "\n")
            tip = "错误详情已写入 gomoku_error.log"
        except Exception:
            tip = "错误详情见上方红字"
        try:
            input("{0}，按回车键退出...".format(tip))
        except Exception:
            time.sleep(10)  # 双击运行无控制台时，至少停留10秒
