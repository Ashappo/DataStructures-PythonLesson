# ============================================================
# 以下为裁判程序提供的类与函数（OJ 上判题端已包含；本地测试用，
# 若 OJ 要求只提交学生代码，提交时请删除本段）
# ============================================================
class BTNode:                           # 二叉链中结点类
    def __init__(self, d=None):         # 构造方法
        self.data = d                   # 结点值
        self.lchild = None              # 左孩子指针
        self.rchild = None              # 右孩子指针

class BTree:                            # 二叉树类
    def __init__(self):                 # 构造方法
        self.b = None                   # 根结点指针

    def DispBTree(self):                # 返回二叉链的括号表示串
        return self._DispBTree(self.b)

    def _DispBTree(self, t):            # 被 DispBTree 方法调用
        if t == None:                   # 空树返回空串
            return ''
        else:
            bstr = t.data               # 输出根结点值
            if t.lchild != None or t.rchild != None:
                bstr += '('             # 有孩子结点时输出 "("
                bstr += self._DispBTree(t.lchild)   # 递归输出左子树
                if t.rchild != None:
                    bstr += ','         # 有右孩子结点时输出 ","
                bstr += self._DispBTree(t.rchild)   # 递归输出右子树
                bstr += ')'             # 输出 ")"
        return bstr

def CreateBTree(s):                     # 由括号表示法串创建二叉链
    st = []                             # 栈：存放待处理的双亲结点
    b = None                            # 二叉树的根结点
    p = None                            # 当前处理的结点
    k = 0                               # 1 表示左孩子，2 表示右孩子
    for ch in s:                        # 逐个字符扫描括号表示法串
        if ch == '(':
            st.append(p)                # 双亲结点进栈
            k = 1                       # 下一个结点为左孩子
        elif ch == ')':
            st.pop()                    # 一对括号处理完毕
        elif ch == ',':
            k = 2                       # 下一个结点为右孩子
        else:
            p = BTNode(ch)              # 新建结点
            if b is None:
                b = p                   # 第一个结点为根结点
            elif k == 1:
                st[-1].lchild = p       # 接在栈顶结点的左链上
            else:
                st[-1].rchild = p       # 接在栈顶结点的右链上
    return b

class HTNode:                           # 哈夫曼树结点类
    def __init__(self, d=' ', w=None):  # 构造方法
        self.data = d                   # 结点值
        self.weight = w                 # 权值
        self.parent = -1                # 指向双亲结点
        self.lchild = -1                # 指向左孩子结点
        self.rchild = -1                # 指向右孩子结点
        self.flag = True                # 标识是双亲的左(True)或者右(False)孩子

# ============================================================
# 题目 3：构造哈夫曼树 —— CreateHT
# ============================================================
'''
设计思路（整体）：
    哈夫曼树采用教材的顺序存储结构 ht[]，共 2n-1 个单元：
      * 下标 0 ~ n-1 存放 n 个叶子结点；
      * 之后每做一次合并，就把新结点存入 ht[] 的下一个空单元（下标 n 起）；
      * 下标 2n-2 为最终的根结点（parent 为 -1）。

    为保证判定结果唯一，必须严格按题目规则合并：
      1) 用小根堆（优先队列）管理"尚无双亲"的结点，堆元素为 [权值, 下标]，
         这样权值相同时自动按下标从小到大出队 —— 天然满足
         "权值最小取下标最小者为 k1，其余中最小（下标最小）者为 k2"；
      2) 每轮 heappop 两次：先出者 p1 作新结点的左孩子（flag=True），
         后出者 p2 作右孩子（flag=False）；
      3) 新结点权值 = 两孩子权值之和，下标依次递增；
      4) 新结点 [新权值, 新下标] 重新进堆，共做 n-1 次合并。

    所有结点的 parent/lchild/rchild 均初始化为 -1（HTNode 构造方法中完成），
    叶子与根的空指针域输出时自然保持 -1。

    时间复杂度：建堆 O(n)，n-1 次合并每次 O(log n)，总计 O(n log n)。

测试用例：
4
A 1
B 2
C 4
D 8
期望输出：
0 1 4 -1 -1
1 2 4 -1 -1
2 4 5 -1 -1
3 8 6 -1 -1
4 3 5 0 1
5 7 6 4 2
6 15 -1 5 3
'''
import heapq                            # 引入堆队列模块（小根堆，合并操作需要）

# 此处为学生编写代码嵌入点位
# 设计函数 CreateHT

#设计函数 CreateHT
def CreateHT(D, W, n):                  # 构造哈夫曼树，返回顺序存储数组 ht
    ht = [None] * (2 * n - 1)           # 初始为含 2n-1 个空结点的数组
    heap = []                           # 优先队列，元素为 [权值, 下标]，按权值建小根堆
    for i in range(n):                  # i 从 0 到 n-1 循环建立 n 个叶子结点并进队
        ht[i] = HTNode(D[i], W[i])      # 建立第 i 个叶子结点（值 D[i]，权 W[i]）
        heapq.heappush(heap, [W[i], i]) # 将 [W[i], i] 进堆（权值相同时按下标 i 升序出队）
    for i in range(n, 2 * n - 1):       # i 从 n 到 2n-2 循环做 n-1 次合并操作
        p1 = heapq.heappop(heap)        # 出队权值最小（同权取下标最小）的结点 p1
        p2 = heapq.heappop(heap)        # 出队其余结点中权值最小者 p2
        ht[i] = HTNode()                # 新建 ht[i] 结点作为合并后的新结点
        # 新结点权值 = 左、右孩子权值之和
        ht[i].weight = ht[p1[1]].weight + ht[p2[1]].weight
        ht[p1[1]].parent = i            # 设置 p1 的双亲为 ht[i]
        ht[i].lchild = p1[1]            # 先出队者 p1 作 ht[i] 的左孩子
        ht[p1[1]].flag = True           # p1 是双亲的左孩子，flag 置 True
        ht[p2[1]].parent = i            # 设置 p2 的双亲为 ht[i]
        ht[i].rchild = p2[1]            # 后出队者 p2 作 ht[i] 的右孩子
        ht[p2[1]].flag = False          # p2 是双亲的右孩子，flag 置 False
        # 将新结点 ht[i] 以 [新权值, 新下标] 进堆，参与后续合并
        heapq.heappush(heap, [ht[i].weight, i])
    return ht                           # 返回建好的哈夫曼树顺序存储数组

if __name__ == '__main__':
    n = int(input())                    # 叶子结点个数
    D = []                              # 结点值列表
    W = []                              # 权值列表
    for i in range(n):                  # 读入 n 个叶子的结点值与权值
        data, w = input().split()
        D.append(data)
        W.append(int(w))
    ht = CreateHT(D, W, n)              # 构造哈夫曼树
    for i in range(2 * n - 1):          # 逐行输出 ht 数组的建树结果
        print(i, ht[i].weight, ht[i].parent, ht[i].lchild, ht[i].rchild)
