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
# 题目 1：二叉树基本运算 —— NodeCount / LeafCount / Height / Level
# ============================================================
'''
设计思路（整体）：
    四个函数都基于二叉链存储结构，采用"先处理小规模问题（递归出口），
    再分解为同构子问题（递归体）"的分治思想求解。
    由于裁判程序的接口传入的是 BTree 包装对象（属性 b 为根结点），
    因此每个接口函数先取出 bt.b，再调用对应的"下划线私有递归函数"
    对结点指针 t 递归求解 —— 这是教材惯用的"接口 + 递归工作函数"两层结构。

    各递归模型：
        NodeCount:  f(t) = 0                          （t 为空）
                    f(t) = f(l) + f(r) + 1            （否则，后序统计）
        LeafCount:  f(t) = 0                          （t 为空）
                    f(t) = 1                          （左、右孩子均为空）
                    f(t) = f(l) + f(r)                （否则）
        Height:     f(t) = 0                          （t 为空）
                    f(t) = max(f(l), f(r)) + 1        （否则）
        Level:      f(t, x, h) = 0                    （t 为空，找不到）
                    f(t, x, h) = h                    （t.data == x）
                    f(t, x, h) = 左子树结果不为 0 ? 左子树结果
                                 : 右子树结果          （否则，先左后右找）

测试用例：
A(B(D,E(H(J,K(L,M(,N))))),C(F,G(,I)))
K
期望输出：
14
6
7
5
'''
# 此处为学生编写代码嵌入点位
# 设计函数 NodeCount、LeafCount、Height、Level

#设计函数 NodeCount
def NodeCount(bt):                      # 接口函数：求二叉树的结点个数
    return _NodeCount(bt.b)             # 从根结点 bt.b 开始递归统计

def _NodeCount(t):                      # 递归工作函数：求以 t 为根的子树结点数
    if t == None:
        return 0                        # 递归出口：空树结点个数为 0
    else:
        # 递归体：结点总数 = 左子树结点数 + 右子树结点数 + 根结点本身（后序思想）
        return _NodeCount(t.lchild) + _NodeCount(t.rchild) + 1

#设计函数 LeafCount
def LeafCount(bt):                      # 接口函数：求二叉树的叶子结点个数
    return _LeafCount(bt.b)             # 从根结点 bt.b 开始递归统计

def _LeafCount(t):                      # 递归工作函数：求以 t 为根的子树叶落数
    if t == None:
        return 0                        # 递归出口：空树叶子个数为 0
    if t.lchild == None and t.rchild == None:
        return 1                        # 左、右子树均为空 => t 是叶子，计 1
    else:
        # 递归体：叶落数只在叶子中产生，非叶结点本身不计入
        return _LeafCount(t.lchild) + _LeafCount(t.rchild)

#设计函数 Height
def Height(bt):                         # 接口函数：求二叉树的高度
    return _Height(bt.b)                # 从根结点 bt.b 开始递归求解

def _Height(t):                         # 递归工作函数：求以 t 为根的子树高度
    if t == None:
        return 0                        # 递归出口：空树的高度为 0
    else:
        lh = _Height(t.lchild)          # 求左子树高度 lh
        rh = _Height(t.rchild)          # 求右子树高度 rh
        # 递归体：树高 = 左、右子树高度的较大者 + 1（根结点所在层）
        return max(lh, rh) + 1

#设计函数 Level
def Level(bt, x):                       # 接口函数：求值为 x 的结点的层次
    return _Level(bt.b, x, 1)           # 根结点层次为 1，从根开始查找

def _Level(t, x, h):                    # 递归工作函数：h 为当前结点 t 的层次
    if t == None:
        return 0                        # 递归出口：空树中找不到 x，返回 0
    elif t.data == x:
        return h                        # 递归出口：当前结点值恰为 x，返回其层次 h
    else:
        l = _Level(t.lchild, x, h + 1)  # 先在左子树中查找（层次加 1）
        if l != 0:
            return l                    # 左子树中找到了，直接返回其层次 l（剪枝，不再找右子树）
        else:
            # 左子树中未找到（返回 0），再在右子树中查找
            return _Level(t.rchild, x, h + 1)

if __name__ == '__main__':
    s = input().strip()                 # 括号表示法串
    x = input().strip()                 # 待查层次的结点值
    bt = BTree()                        # 二叉树对象
    bt.b = CreateBTree(s)               # 建树并设置根结点
    print(NodeCount(bt))                # 第 1 行：结点个数
    print(LeafCount(bt))                # 第 2 行：叶子结点个数
    print(Height(bt))                   # 第 3 行：二叉树的高度
    print(Level(bt, x))                 # 第 4 行：结点 x 的层次
