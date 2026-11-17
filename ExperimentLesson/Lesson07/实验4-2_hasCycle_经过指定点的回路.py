# -*- coding: utf-8 -*-
"""
实验四 第 2 题：判断连通无向图 G 中是否存在经过顶点 v 的回路
================================================================

【解题思路】
1. 回路的判定转化为"从 v 出发能否沿着简单路径绕回 v"：
   以 v 为起点做 DFS，搜索过程中维护深度 d（当前顶点 u 距起点 v 的边数）。
   当在顶点 u 处考察邻接点 w 时，若 w == v 且 d > 1，说明当前路径
   v -> ... -> u -> v 首尾相接构成回路，立即返回 True。

2. 关键条件 d > 1 的含义（易错点）：
   - d = 1 时回到 v，对应路径 v -> a -> v，即沿同一条边 (v,a) 走了个来回，
     这在无向图中不算回路（边重复使用）；回路在简单图中至少要 3 条边，
     即至少经过 2 个中间顶点。
   - 因此只有当 d >= 2（路径上已有至少 2 条边、u 不是 v 的直接邻接点
     那一层）时，w == v 才构成真正的回路。
   - 若把条件误写成 d >= 1 或 w == v，任何带边的图都会误判为 yes。

3. visited 数组的作用：防止 DFS 在图中绕圈死循环。注意起点 v 保持
   "已访问"状态，其他分支不会再提前进入 v，回 v 只能通过 w == v 判定。

【相对参考答案的优化点】
- 参考答案依赖全局 visited[MAXV]，每次调用需手动重置；本版本用局部
  visited，按 G.n 分配，天然初始化，函数可重入。
- 参考答案把"初始化 + 递归"拆成 hasCycle / hasCycle1 两个函数并传递
  d 参数；本版本用内嵌函数闭包直接捕获 v，少一层传参。
- 剪枝不变：一旦找到回路立即层层 return True，避免无效搜索。

【复杂度】时间 O(n + e)；空间 O(n)（递归栈 + visited）。
"""

INF = 0x3f3f3f3f                                    # 表示∞
MAXV = 100                                          # 最大顶点个数

class ArcNode:                                      # 边结点
    def __init__(self, adjv, w):                    # 构造方法
        self.adjvex = adjv                          # 邻接点
        self.weight = w                             # 边的权值

class AdjGraph:                                     # 图邻接表类
    def __init__(self, n=0, e=0):                   # 构造方法
        self.adjlist = []
        self.vexs = []
        self.n = n
        self.e = e

    def CreateAdjGraph(self, a, n, e):              # 通过数组a、n和e建立图的邻接表
        self.n = n
        self.e = e
        for i in range(n):
            adi = []
            for j in range(n):
                if a[i][j] != 0 and a[i][j] != INF:
                    p = ArcNode(j, a[i][j])
                    adi.append(p)
            self.adjlist.append(adi)

    def DispAdjGraph(self):                         # 输出图的邻接表
        for i in range(self.n):
            print("  [%d]" % (i), end='')
            for p in self.adjlist[i]:
                print("->(%d,%d)" % (p.adjvex, p.weight), end='')
            print("->∧")


# ============================ 学生编写区域 ============================
def hasCycle(G, v):
    """判断连通无向图 G 中是否存在经过顶点 v 的回路"""
    visited = [False] * G.n                        # 局部访问标志，自动初始化为未访问

    def dfs(u, d):                                 # u：当前顶点；d：u 距起点 v 的边数
        visited[u] = True                          # 标记 u 已访问
        for p in G.adjlist[u]:                     # 依次考察 u 的每个邻接点 w
            w = p.adjvex
            if w == v and d > 1:                   # 回到起点且路径长度>1：找到回路
                return True                        #（d==1 时只是沿原边折返，不算回路）
            if not visited[w]:                     # w 未访问过则继续深入
                if dfs(w, d + 1):                  # 路径深度加 1
                    return True                    # 找到回路层层返回，提前终止
        return False                               # u 的所有分支均无回路

    return dfs(v, 0)                               # 从指定顶点 v 出发搜索
# =====================================================================


if __name__ == '__main__':
    n, e = map(int, input().split())
    a = [[0] * n for _ in range(n)]
    for i in range(e):                              # 读入无向边
        x, y = map(int, input().split())
        a[x][y] = a[y][x] = 1
    G = AdjGraph()
    G.CreateAdjGraph(a, n, e)
    v = int(input())
    if hasCycle(G, v):
        print("yes")
    else:
        print("no")

# ------------------------- 本地自测 -------------------------
'''
11 13
0 1
0 2
0 3
1 4
1 5
2 3
2 5
2 6
3 7
6 7
6 8
6 9
7 10
3

yes
样例输入：11 个顶点 13 条边（见题目），指定顶点 3 -> 输出 yes
（路径 3-2-6-7-3 构成经过 3 的回路）

序号	操作	状态变化	递归调用链（即当前路径）
①	调用 hasCycle(G,3)	visited 全置 False，转 dfs(3,0)	—
②	dfs(3,0)	visited[3]=True；邻接 [0,2,7]，w=0：0≠v、未访问 → 深入	3
③	dfs(0,1)	visited[0]=True；邻接 [1,2,3]，w=1：1≠v、未访问 → 深入	3→0
④	dfs(1,2)	visited[1]=True；邻接 [0,4,5]：w=0 已访跳过；w=4 → 深入	3→0→1
⑤	dfs(4,3)	visited[4]=True；邻接 [1] 已访，for 空转 → return False	3→0→1→4
⑥	回到 dfs(1,2)	收到 False，继续循环，w=5 → 深入	3→0→1
⑦	dfs(5,3)	visited[5]=True；邻接 [1,2]：w=1 已访；w=2 → 深入	3→0→1→5
⑧	dfs(2,4)	visited[2]=True；邻接 [0,3,5,6]：w=0 已访跳过；w=3 == v 且 d=4>1 → return True	3→0→1→5→2
⑨	逐层回传	dfs(2)→dfs(5)→dfs(1)→dfs(0)→dfs(3) 全部 return True，主程序打印	—

边界用例 1（无回路）：
  输入：3 2 / 0 1 / 1 2 / 0      -> 输出 no（树结构无回路）
边界用例 2（只有一条边的图，验证 d>1 条件）：
  输入：2 1 / 0 1 / 0            -> 输出 no（0-1-0 只是原边折返，不是回路）
边界用例 3（最小回路：三角形）：
  输入：3 3 / 0 1 / 1 2 / 2 0 / 0 -> 输出 yes（0-1-2-0）
'''
