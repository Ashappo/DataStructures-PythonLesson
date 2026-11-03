# -*- coding: utf-8 -*-
"""双人五子棋（tkinter 单文件版）—— 实验八参考源代码"""
import tkinter as tk
from tkinter import messagebox

GRID = 15  # 棋盘 15×15 个交叉点
CELL = 40  # 网格间距（像素）
MARGIN = 30  # 棋盘四周留白
SIZE = CELL * (GRID - 1)  # 棋盘线总长：14×40 = 560
WIN_LEN = 5  # 连子数
DIRS = ((0, 1), (1, 0), (1, 1), (1, -1))  # 横、竖、左斜、右斜 4 条轴线


class Gomoku:
    def __init__(self, root):
        self.root = root
        self.root.title("双人五子棋")
        self.root.geometry("700x720")  # 画布 620×620 + 顶部标签 + 底部按钮
        self.root.resizable(False, False)

        self.board = [[0] * GRID for _ in range(GRID)]  # 0 空 1 黑 2 白
        self.history = []  # 悔棋栈
        self.now_player = 1  # 当前玩家
        self.score = {1: 0, 2: 0}  # 累计胜场
        self.game_over = False

        self._build_ui()
        self._draw_board()

    # ---------------- 界面 ----------------
    def _build_ui(self):
        top = tk.Frame(self.root)
        top.pack(pady=(10, 6))
        self.lbl_black = tk.Label(top, text="黑方：0 胜",
                                  font=("微软雅黑", 12, "bold"))
        self.lbl_black.pack(side=tk.LEFT, padx=14)
        self.lbl_turn = tk.Label(top, text="轮到：黑棋",
                                 font=("微软雅黑", 12), fg="#C0392B")
        self.lbl_turn.pack(side=tk.LEFT, padx=14)
        self.lbl_white = tk.Label(top, text="白方：0 胜",
                                  font=("微软雅黑", 12, "bold"))
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
        col = round((event.x - MARGIN) / CELL)
        row = round((event.y - MARGIN) / CELL)
        if not (0 <= row < GRID and 0 <= col < GRID):
            return
        # 容差判断：点得偏离交叉点太远则不落子
        x, y = MARGIN + col * CELL, MARGIN + row * CELL
        if abs(event.x - x) > CELL * 0.4 or abs(event.y - y) > CELL * 0.4:
            return
        if self.board[row][col] != 0:  # 禁止重复落子
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
            for r, c in line:  # 高亮获胜的连子
                self._draw_piece(r, c, self.board[r][c], outline="#E74C3C")
            self._update_labels()
            name = "黑棋" if self.now_player == 1 else "白棋"
            print(f"[计分] 黑 {self.score[1]} : {self.score[2]} 白")
            messagebox.showinfo("对局结束",
                                f"{name}五子连珠，获胜！\n当前比分  黑 {self.score[1]} : "
                                f"{self.score[2]} 白")
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
        self.lbl_black.config(text=f"黑方：{self.score[1]} 胜")
        self.lbl_white.config(text=f"白方：{self.score[2]} 胜")
        if self.game_over:
            self.lbl_turn.config(text="对局结束")
        else:
            name = "黑棋" if self.now_player == 1 else "白棋"
            self.lbl_turn.config(text="轮到：" + name)


if __name__ == "__main__":
    root = tk.Tk()
    Gomoku(root)
    root.mainloop()