# -*- coding: utf-8 -*-
"""
实验四 第 1 题：求无向图中顶点 u 到顶点 v 的一条简单路径
================================================================

【解题思路】
1. 问题本质：在无向图的邻接表上做"带回溯的深度优先搜索（DFS）"。
   简单路径 = 路径上的顶点互不重复，因此搜索过程中必须用 visited[] 记录
   "当前路径上已走过的顶点"，防止绕圈子。

2. DFS + 回溯的框架：
   (1) 进入顶点 x 时：置 visited[x]=1，并把 x 追加到 path 末尾；
   (2) 若 x == v：说明 u 到 v 的路径已经拼好，直接返回该路径；
   (3) 否则依次考察 x 的每个邻接点 w：
       - w 未访问过 -> 递归 dfs(w)；递归一旦返回 True（找到路径），
         立刻把 True 一路向上返回，路径自然保留在 path 中；
       - 若所有邻接点都走不通（返回 False），说明以当前 path 走到 x
         是"死路"——必须回溯：把 x 从 path 末尾弹出（path.pop()），
         并不撤销 visited[x]（因为本题只找一条路径，x 既然走不通，
         让后续分支跳过它反而能加速，且不影响正确性：若 x 真在某条
         可行路径上，更早的分支早已返回）。
   (4) 主调函数 dfs(u) 返回 False 表示不存在路径（本题保证存在，仅作兜底）。

3. 为什么任意一条都算对：DFS 按"邻接点在邻接表中的存放顺序"优先深入，
   不同的建表顺序会得到不同的合法路径，判题采用 Special Judge。

【相对参考答案的优化点】
- 参考答案用全局 visited[MAXV]、定长 path[-1]*MAXV 和"找到后切片
  path[0:d+1]"实现，需要人工维护深度 d，容易在边界 d 的增减上出错。
- 本版本改为：
  (1) visited 用局部列表 [False]*G.n，按实际顶点数分配，不依赖全局
      变量，多次调用函数互不干扰（可重入）；
  (2) path 用 list 的 append/pop 天然完成"进路径/回溯退路径"，
      不再需要深度参数 d 和末尾切片，代码更短且不易错；
  (3) 找到目标后用异常式的一路 return True 提前终止，剩余分支不再展开。

【复杂度】时间 O(n + e)（每个顶点、每条边至多访问一次）；空间 O(n)。
"""

INF = 0x3f3f3f3f                                    # 表示∞
MAXV = 100                                          # 最大顶点个数

class ArcNode:                                      # 边结点
    def __init__(self, adjv, w):                    # 构造方法
        self.adjvex = adjv                          # 邻接点
        self.weight = w                             # 边的权值

class AdjGraph:                                     # 图邻接表类
    def __init__(self, n=0, e=0):                   # 构造方法
        self.adjlist = []                           # 邻接表数组
        self.vexs = []                              # vexs[i]存放顶点i的信息，暂未用
        self.n = n                                  # 顶点数
        self.e = e                                  # 边数

    def CreateAdjGraph(self, a, n, e):              # 通过数组a、n和e建立图的邻接表
        self.n = n
        self.e = e
        for i in range(n):
            adi = []                                # 顶点i的邻接点列表
            for j in range(n):
                if a[i][j] != 0 and a[i][j] != INF: # 存在一条边<i,j>
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
def FindaPath(G, u, v):
    """求 G 中顶点 u 到顶点 v 的一条简单路径，返回顶点编号列表；不存在返回 None"""
    visited = [False] * G.n              # 局部访问标志，避免使用全局数组
    path = []                            # 当前搜索路径（path 是一个被所有递归层共享的栈）

    def dfs(x):                                    # 内嵌递归函数：从 x 继续扩展路径
        visited[x] = True                          # 标记 x 已进入当前路径
        '''
        为什么不需要撤销 visited？被证明“从当前前缀走不通”，
        之后任何分支再碰到 3 都不必重试，跳过它只会加速搜索且不影响正确性
        '''
        path.append(x)                             # x 加入路径末尾
        if x == v:                                 # 到达终点：路径已完整
            return True
        for p in G.adjlist[x]:                     # 依次考察 x 的每个邻接点 w
            w = p.adjvex
            if not visited[w]:                     # w 未访问过才扩展
                if dfs(w):                         # 递归：从 w 继续找 v
                    return True                    # 找到即层层返回，不再回溯
        path.pop()  # 所有邻接点走不通：回溯，弹出 x，pop 的只有一处，且和 return True 互斥
        return False                               # 报告此分支失败

    return path if dfs(u) else None                # 成功返回路径，失败返回 None
# =====================================================================


if __name__ == '__main__':
    n, e = map(int, input().split())
    a = [[0] * n for _ in range(n)]
    for i in range(e):                              # 读入无向边
        x, y = map(int, input().split())
        a[x][y] = a[y][x] = 1
    G = AdjGraph()
    G.CreateAdjGraph(a, n, e)
    u, v = map(int, input().split())
    path = FindaPath(G, u, v)
    for x in path:                                  # 输出路径顶点编号
        print(x, end=' ')
    print()

# ------------------------- 本地自测（样例） -------------------------
'''
输入：
5 8
0 1
0 3
0 4
1 2
1 3
2 3
2 4
3 4
0 3
输出（本实现的邻接点顺序下）：
0 1 2 3
说明：0 的邻接表按列序为 1,3,4，DFS 优先走 1；1 的邻接点 0(已访),2,3,4，
      优先走 2；2 的邻接点 1(已访),3,4，优先走 3 == v，故输出 0 1 2 3。
      
'''
