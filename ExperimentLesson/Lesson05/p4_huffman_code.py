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

def CreateHT(D, W, n):                  # 构造哈夫曼树（裁判程序提供）
    ht = [None] * (2 * n - 1)           # 初始为含 2n-1 个空结点的数组
    heap = []                           # 优先队列，元素为 [权值, 下标]，按权值建小根堆
    for i in range(n):                  # i 从 0 到 n-1 循环建立 n 个叶子结点并进队
        ht[i] = HTNode(D[i], W[i])      # 建立第 i 个叶子结点
        heapq.heappush(heap, [W[i], i]) # 将 [W[i], i] 进堆
    for i in range(n, 2 * n - 1):       # i 从 n 到 2n-2 循环做 n-1 次合并操作
        p1 = heapq.heappop(heap)        # 出队两个权值最小的结点 p1 和 p2
        p2 = heapq.heappop(heap)
        ht[i] = HTNode()                # 新建 ht[i] 结点
        ht[i].weight = ht[p1[1]].weight + ht[p2[1]].weight  # 权值之和
        ht[p1[1]].parent = i            # 设置 p1 的双亲为 ht[i]
        ht[i].lchild = p1[1]            # p1 作左孩子
        ht[p1[1]].flag = True
        ht[p2[1]].parent = i            # 设置 p2 的双亲为 ht[i]
        ht[i].rchild = p2[1]            # p2 作右孩子
        ht[p2[1]].flag = False
        heapq.heappush(heap, [ht[i].weight, i])  # 新结点进堆
    return ht

# 以下为裁判程序提供的类与函数（OJ 上判题端已包含；本地测试用，
# 若 OJ 要求只提交学生代码，提交时请删除本段）
import heapq                            # 引入堆队列模块

# ============================================================
# 题目 4：哈夫曼编码与译码 —— CreateHCode / DeCode
# ============================================================
'''
设计思路（整体）：
    依赖裁判程序提供的顺序存储哈夫曼树 ht[]（共 2n-1 个结点，
    下标 2n-2 为根），利用每个结点的 parent 双亲指针与 flag
    左右孩子标识完成编码与译码。

    【CreateHCode 求编码 —— 从叶到根回溯】
      从每个叶子 ht[i]（i = 0..n-1）出发，沿 parent 指针一步步走向根：
        * 若当前结点 flag == True，说明它是双亲的左孩子，记一位 '0'；
        * 若 flag == False，说明是右孩子，记一位 '1'；
      由于是从叶子往根"逆序"得到的编码，最后需 reverse() 逆置。
      每个叶子的回溯长度不超过树高，总时间 O(n · h)。

    【DeCode 译码 —— 从根到叶走链】
      从根结点 i = 2n-2 出发逐位扫描 0/1 编码串：
        * 遇 '0' 走左孩子，遇 '1' 走右孩子；
        * 一旦到达叶子（lchild == -1 且 rchild == -1），输出该叶子的
          结点值，并回到根结点继续译下一个符号；
      编码串保证可完全译码，扫描结束后换行。
      时间复杂度 O(|code|)。

测试用例：
4
A 1
B 2
C 4
D 8
01001
期望输出：
A:000
B:001
C:01
D:1
CB
'''
# 此处为学生编写代码嵌入点位
# 设计函数 CreateHCode、DeCode

#设计函数 CreateHCode
def CreateHCode(ht, n):                 # 根据哈夫曼树求哈夫曼编码
    hcd = []                            # hcd 存放哈夫曼编码，hcd[i] 对应叶子 ht[i]
    for i in range(n):                  # 遍历下标从 0 到 n-1 的叶子结点
        code = []                       # 存放 ht[i] 结点的哈夫曼编码（暂时逆序）
        j = i                           # 从叶子 ht[i] 出发沿双亲链回溯
        while ht[j].parent != -1:       # 未到根结点（根的双亲为 -1）时循环
            if ht[j].flag:              # ht[j] 是双亲的左孩子
                code.append('0')        # 左分支记 '0'
            else:                       # ht[j] 是双亲的右孩子
                code.append('1')        # 右分支记 '1'
            j = ht[j].parent            # 继续向根方向回溯
        code.reverse()                  # 回溯得到的是逆序编码，需逆置
        hcd.append(''.join(code))       # 转成字符串加入结果列表
    return hcd                          # 返回编码列表

#设计函数 DeCode
def DeCode(ht, code, n):                # 对 0/1 编码串译码
    i = 2 * n - 2                       # 从根结点（下标 2n-2）出发
    for ch in code:                     # 逐位扫描编码串
        if ch == '0':
            i = ht[i].lchild            # 遇 '0' 走左孩子
        else:
            i = ht[i].rchild            # 遇 '1' 走右孩子
        if ht[i].lchild == -1 and ht[i].rchild == -1:
            print(ht[i].data, end='')   # 到达叶子，输出其结点值（不换行）
            i = 2 * n - 2               # 回到根结点，继续译下一个符号
    print()                             # 译码结束，输出换行

if __name__ == '__main__':
    n = int(input())                    # 叶子结点个数
    D = []                              # 结点值列表
    W = []                              # 权值列表
    for i in range(n):                  # 读入 n 个叶子的结点值与权值
        data, w = input().split()
        D.append(data)
        W.append(int(w))
    code = input().strip()              # 待译码的 0/1 编码串
    ht = CreateHT(D, W, n)              # 构造哈夫曼树（裁判程序提供）
    hcd = CreateHCode(ht, n)            # 求哈夫曼编码
    for i in range(n):                  # 输出 n 行编码表：符号:编码
        print(ht[i].data + ':' + hcd[i])
    DeCode(ht, code, n)                 # 译码并输出结果
