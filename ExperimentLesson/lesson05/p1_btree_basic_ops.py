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
    
1、对外隐藏实现细节，封装性好 用户只调用 NodeCount(bt)，不需要知道内部是递归、不需要传根指针，不用关心 bt.b、左孩子 lchild 这些底层字段；私有 _NodeCount 是内部实现，外部不应该直接调用。 如果以后改成非递归版本，对外函数名不变，上层代码不用改。
2、统一入口，预处理放在接口里 所有公共操作统一先拿到根 bt.b。以后你如果需要：参数校验、空树保护、日志、计时、锁、重置标记，全部写在接口函数，不用在每一处递归调用里重复写。 例如：可以在 NodeCount 先判断 bt 是否合法，再交给递归。
3、递归函数更纯粹，逻辑清晰_NodeCount 只专注一件事：给定子树根指针 t，返回子树结点数量。 参数稳定（永远是结点指针），递归出口、递归体一目了然，没有混杂对外的参数适配，读代码、调试都更容易。
4、避免调用方传错递归起始参数 如果把递归函数直接暴露给用户，用户很可能误传某个子节点而不是整棵树的根；接口强制从整棵树的根 bt.b 启动，保证语义正确：NodeCount 就是统计整棵二叉树，而不是随便一棵子树。
5、便于复用与重载 / 扩展
如果后续新增功能：统计叶子、高度、先序遍历，都沿用这套范式；
如果想要提供两个版本：统计整树 / 统计某棵子树，可以让接口再增加一个版本，内部复用同一个私有递归函数；
如果递归需要辅助变量（标记、计数器、路径数组），也可以放在接口初始化，再传给递归工作函数。
6、降低递归污染 递归函数一般不适合作为公共 API：它的参数是底层结点指针，属于内部结构。分开之后，代码边界清晰，符合 “对外提供操作，内部实现算法” 的面向过程 / 面向对象设计习惯。

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
