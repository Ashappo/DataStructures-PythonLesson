# -*- coding: utf-8 -*-
"""
实验四 第 4 题：拓扑排序输出一个可行的课程学习顺序
================================================================

【解题思路】
1. 拓扑排序（Kahn 算法，基于减入度）的步骤：
   (1) 统计入度：遍历邻接表，每条有向边 <i,w> 使 ind[w] 加 1。
       入度为 0 表示该课程没有任何先修课（或先修课已全部修完）。
   (2) 所有入度为 0 的顶点进栈（进栈顺序决定最终序列的形态，
       但任何合法序列都会被判题接受——Special Judge）。
   (3) 栈不空时循环：出栈顶点 i 加入结果序列 res；把 i 的每条出边
       <i,w> 的终点 w 入度减 1（表示"课程 i 已修完"）；若某 w 的
       入度减到 0，说明其先修课全部完成，w 进栈。
   (4) 栈空时 res 中恰好含全部 n 个顶点（题目保证是 DAG），返回 res。

2. 为什么用栈（而不是队列）：栈和队列都能正确完成拓扑排序，区别只在
   产出的序列形态不同。本题用 collections.deque 以 append()（尾进）+
   pop()（尾出）模拟栈，两个操作都是 O(1)；若误用 popleft() 则变成
   BFS 式拓扑排序，同样正确但序列与样例可能不同。

3. 易错点：
   (1) ind 数组要按 G.n 统计并使用，直接复用 MAXV 长度也可（全局未
       越界），但比较循环必须以 G.n 为界，否则 n < MAXV 时会把无效
       顶点（入度恒 0）也排进序列——这是参考答案用 [0]*MAXV 而仍
       正确的原因：主循环 range(G.n) 限定了范围；
   (2) 邻接表存的是"出边"，减入度时遍历的是 G.adjlist[i]（i 的
       出边邻接点），不要误用入边方向；
   (3) 顶点从 0 开始编号，输出时用空格分隔、末尾换行。

【相对参考答案的优化点】
- ind 按 G.n 分配（[0]*G.n），不依赖 MAXV，避免全局数组复用隐患；
- 入度为 0 的初始顶点用列表推导一次收集，代替逐个 if 判断；
- 直接用 Python list 作栈（append/pop 即为进栈/出栈），不必引入
  deque；两者复杂度相同，代码更简洁。
- 附加健壮性说明：若图中存在环，循环结束后 len(res) < G.n，
  可据此检测"课程先修关系成环、无法完成学业"（本题保证 DAG，
  故未加入输出逻辑，仅作扩展提示）。

【复杂度】时间 O(n + e)（入度统计、每个顶点各进出栈一次、每条边
减一次入度）；空间 O(n)。
"""

from collections import deque

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
def TopSort(G):
    """返回 G 的一个拓扑序列（顶点编号列表）"""
    ind = [0] * G.n                                # ind[i]：顶点 i 的入度
    for i in range(G.n):                           # 遍历每个顶点的出边统计入度
        for p in G.adjlist[i]:
            ind[p.adjvex] += 1                     # 边 <i,w> 使 w 入度加 1

    st = [i for i in range(G.n) if ind[i] == 0]    # 所有入度为 0 的顶点进栈（list 模拟栈）
    res = []                                       # 存放拓扑序列
    while st:                                      # 栈不空时循环
        i = st.pop()                               # 出栈一个无前驱（先修已全修完）的顶点
        res.append(i)                              # 加入拓扑序列
        for p in G.adjlist[i]:                     # 删除 i 的所有出边：终点入度减 1
            w = p.adjvex
            ind[w] -= 1
            if ind[w] == 0:                        # w 的先修课全部完成
                st.append(w)                       # w 进栈
    return res
    # 扩展提示：若此处 len(res) < G.n，说明图中存在回路（非 DAG），
    # 拓扑排序失败——可用于"判断课程能否修完"类题目。
# =====================================================================


if __name__ == '__main__':
    n, e = map(int, input().split())
    a = [[0] * n for _ in range(n)]
    for i in range(e):                              # 读入有向边
        x, y = map(int, input().split())
        a[x][y] = 1
    G = AdjGraph()
    G.CreateAdjGraph(a, n, e)
    order = TopSort(G)
    for x in order:                                 # 输出拓扑序列
        print(x, end=' ')
    print()

# ------------------------- 本地自测（样例） -------------------------
'''
输入：
7 8
0 2
1 3
2 3
1 4
3 4
3 5
1 6
6 5
输出：1 6 0 2 3 5 4

推演：初始入度 ind=[0,0,1,2,2,2,1]，栈 [0,1]
  出 1 -> ind 3:1, 4:1, 6:0(进栈)；出 6 -> ind 5:1；出 0 -> ind 2:0(进栈)
  出 2 -> ind 3:0(进栈)；出 3 -> ind 4:0, 5:0(进栈)；出 5；出 4
  序列 1 6 0 2 3 5 4，与样例一致。

边界用例 1（无先修关系 e=0）：
  输入 "3 0" -> 所有顶点入度 0，栈 [0,1,2]，输出 2 1 0（栈序弹出，仍合法）
边界用例 2（链式先修）：
  输入 "4 3 / 0 1 / 1 2 / 2 3" -> 唯一拓扑序列 0 1 2 3
'''
