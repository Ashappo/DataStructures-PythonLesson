# -*- coding: utf-8 -*-
"""
实验四 第 3 题：Prim 算法构造最小生成树，求还需新建道路的最小总长度
================================================================

【解题思路】
1. Prim 算法（贪心）基本框架——适合稠密图（本题 n<=100，用邻接矩阵）：
   设两个集合 U（已并入生成树的顶点）与 V-U（尚未并入的顶点）。
   (1) 初始 U = {起点 0}（对应村庄 1），lowcost[j] = edges[0][j]，
       表示"把 j 接入当前生成树的最小代价"；
   (2) 重复 n-1 次：
       - 在 V-U 中选 lowcost 最小的顶点 k，把 k 并入 U，并累加
         lowcost[k]（这条边就是生成树的一条树边）；
       - 用 k 的各条出边松弛 V-U 中的顶点：
         lowcost[j] = min(lowcost[j], edges[k][j])。
   (3) n-1 条树边权值之和即为最小生成树权值和。

2. 本题的两个变形要点：
   (1) "已建道路无需花钱"：主程序把已建道路对应矩阵元素置 0，
       Prim 过程会优先（代价 0）选中这些边，它们被计入生成树但
       权值为 0，因此累加和恰好等于"还需新建道路的最小总长度"，
       无需对算法本身做任何修改——把免费边看成权值 0 的普通边即可。
   (2) 【最大陷阱】不能用 lowcost[j]==0 来判断顶点 j 是否已并入 U！
       经典写法常以"lowcost 不为 0 且不为 INF"作为 V-U 中顶点的判据，
       但本题存在权值为 0 的合法边（已建道路），未并入顶点的 lowcost
       也可能是 0，会造成漏选/错选。因此必须使用独立的 visited[]（或
       U 集合）数组标记顶点是否已并入，这是相对经典模板的必要改动。

3. 正确性依据（贪心选择性质）：每次选取的"连接 U 与 V-U 的最小权边"
   一定属于某棵最小生成树，故逐条累加得到的就是最小权值和。

【相对参考答案的优化点】
- 用独立的 visited[] 判断顶点归属，规避权 0 边的经典判据陷阱（见上）；
- lowcost 直接用 g.edges[0] 的切片复制，省去一遍循环赋值；
- 选最小 lowcost 与松弛合并写在一个函数内，逻辑紧凑；
- n<=100，采用 O(n^2) 的朴素 Prim 即可，无需堆优化（稀疏图才更宜
  用邻接表+优先队列的 O(e·log n) 写法）。

【复杂度】时间 O(n^2)；空间 O(n^2)（邻接矩阵本身）。
"""

INF = 0x3f3f3f3f                        # 表示∞

class MatGraph:                         # 图邻接矩阵类
    def __init__(self, n=0, e=0):
        self.edges = []                 # 邻接矩阵数组
        self.vexs = []                  # vexs[i]存放顶点i的信息，暂未用
        self.n = n                      # 顶点数
        self.e = e                      # 边数

    def CreateMatGraph(self, a, n, e):  # 通过数组a、n和e建立图的邻接矩阵
        self.n = n
        self.e = e
        import copy
        self.edges = copy.deepcopy(a)   # 深拷贝

    def DispMatGraph(self):             # 输出图的邻接矩阵
        for i in range(self.n):
            for j in range(self.n):
                if self.edges[i][j] == INF:
                    print("%4s" % ("∞"), end=' ')
                else:
                    print("%5d" % (self.edges[i][j]), end=' ')
            print()


# ============================ 学生编写区域 ============================
def Prim(g):
    """从顶点 0（村庄 1）出发求最小生成树权值和"""
    n = g.n
    lowcost = g.edges[0][:]                    # lowcost[j]：j 接入 U 的最小代价
    visited = [False] * n                      # visited[j]：j 是否已并入 U
    visited[0] = True                          # 从顶点 0（村庄 1）出发
    total = 0                                  # 生成树权值和（需新建道路总长）

    for _ in range(n - 1):                     # 还需并入 n-1 个顶点
        # ---- 第一步：在 V-U 中选 lowcost 最小的顶点 k ----
        k, mind = -1, INF
        for j in range(n):
            if not visited[j] and lowcost[j] < mind:
                k, mind = j, lowcost[j]
        # ---- 第二步：把 k 并入 U，累加对应树边权值 ----
        visited[k] = True
        total += lowcost[k]                    # 已建道路权值为 0，累加 0 即免费
        # ---- 第三步：用 k 的出边松弛 V-U 中顶点的候选边 ----
        for j in range(n):
            if not visited[j] and g.edges[k][j] < lowcost[j]:
                lowcost[j] = g.edges[k][j]
    return total
# =====================================================================


if __name__ == '__main__':
    n = int(input())
    a = []                              # 读入邻接矩阵
    for i in range(n):
        a.append(list(map(int, input().split())))
    k = int(input())
    for i in range(k):                  # 读入已建道路，对应元素置 0
        x, y = map(int, input().split())
        a[x - 1][y - 1] = a[y - 1][x - 1] = 0
    g = MatGraph()
    g.CreateMatGraph(a, n, 0)
    print(Prim(g))

# ------------------------- 本地自测（样例） -------------------------
'''
输入：
4
0 1 1061109567 10
1 0 2 5
1061109567 2 0 3
10 5 3 0
1
1 2
输出：5

推演：村庄1-2 间道路已建 -> edges[0][1]=edges[1][0]=0。
  U={0}: lowcost=[-,0,INF,10] -> 选 1(代价0，免费道路)，total=0
  松弛: lowcost[2]=min(INF,2)=2, lowcost[3]=min(10,5)=5
  U={0,1}: 选 2(代价2)，total=2；松弛 lowcost[3]=min(5,3)=3
  U={0,1,2}: 选 3(代价3)，total=5  -> 输出 5，与样例一致。

边界用例（n=1）：输入 "1 / 0 / 0" -> 无需任何道路，输出 0
（n-1=0 次 loop 不执行；注意此时 Prim 中循环体不进入，直接返回 0）
'''
