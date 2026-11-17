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
# 题目 2：由遍历序列重建二叉树 —— CreateBTree1 / CreateBTree2
# ============================================================
'''
设计思路（整体）：
    重建的核心是"先/后序定根，中序分左右"：
      * 先序序列 pres 的第一个字符一定是根；
      * 后序序列 posts 的最后一个字符一定是根；
      * 在中序序列 ins 中定位根，根左侧的 k 个字符是左子树的中序序列，
        右侧是右子树的中序序列；再按长度 k 切分先/后序中对应的左右子树
        部分，递归重建。

    为避免每次递归都复制子串（n≤62 虽然复制也可行，但教材采用下标法），
    递归工作函数统一使用四个参数刻画"当前要重建的子树"：
        _CreateBTree1(pres, i, ins, j, n)
        含义：当前子树共有 n 个结点，其先序序列为 pres[i..i+n-1]，
              对应的中序序列为 ins[j..j+n-1]。
    每层递归：
        1) 取根 d = pres[i]（或 posts[i+n-1]）；
        2) p = ins.index(d)，k = p - j 即左子树结点个数；
        3) 先序法：左子树先序起点为 i+1，右子树先序起点为 i+k+1；
           后序法：左子树后序起点为 i，右子树后序起点为 i+k
                   （根在末尾 i+n-1，右子树紧挨在根之前）；
        4) 中序区间：左子树为 ins[j..p-1]（起点 j，长度 k），
                     右子树为 ins[p+1..j+n-1]（起点 p+1，长度 n-k-1）。

    接口函数把结果包进 BTree 对象（属性 b 为根），与裁判程序约定一致。

测试用例：
ABDEHJKLMNCFGI
DBJHLKMNEAFCGI
DJLNMKHEBFIGCA
期望输出：
A(B(D,E(H(J,K(L,M(,N))))),C(F,G(,I)))
A(B(D,E(H(J,K(L,M(,N))))),C(F,G(,I)))
'''
# 此处为学生编写代码嵌入点位
# 设计函数 CreateBTree1、CreateBTree2

#设计函数 CreateBTree1
def CreateBTree1(pres, ins):            # 由先序序列 pres 和中序序列 ins 构造二叉链
    bt = BTree()                        # 新建 BTree 包装对象
    bt.b = _CreateBTree1(pres, 0, ins, 0, len(pres))
    return bt                           # 返回包装对象（其属性 b 为根结点）

def _CreateBTree1(pres, i, ins, j, n):  # 递归工作函数：pres[i..i+n-1] 与 ins[j..j+n-1] 是同一棵子树
    if n <= 0: return None              # 递归出口：序列为空，对应空树
    d = pres[i]                         # 先序序列的第一个字符即根结点值 d
    t = BTNode(d)                       # 创建根结点（结点值为 d）
    p = ins.index(d)                    # 在中序序列 ins 中找到根结点的索引 p
    k = p - j                           # 中序中根左侧的字符个数 = 左子树结点个数 k
    # 递归构造左子树：先序从 i+1 起长 k；中序从 j 起长 k
    t.lchild = _CreateBTree1(pres, i + 1, ins, j, k)
    # 递归构造右子树：先序从 i+k+1 起长 n-k-1；中序从 p+1 起长 n-k-1
    t.rchild = _CreateBTree1(pres, i + k + 1, ins, p + 1, n - k - 1)
    return t                            # 返回重建好的子树根结点

#设计函数 CreateBTree2
def CreateBTree2(posts, ins):           # 由后序序列 posts 和中序序列 ins 构造二叉链
    bt = BTree()                        # 新建 BTree 包装对象
    bt.b = _CreateBTree2(posts, 0, ins, 0, len(posts))
    return bt                           # 返回包装对象（其属性 b 为根结点）

def _CreateBTree2(posts, i, ins, j, n): # 递归工作函数：posts[i..i+n-1] 与 ins[j..j+n-1] 是同一棵子树
    if n <= 0: return None              # 递归出口：序列为空，对应空树
    d = posts[i + n - 1]                # 后序序列的最后一个字符即根结点值 d
    t = BTNode(d)                       # 创建根结点（结点值为 d）
    p = ins.index(d)                    # 在中序序列 ins 中找到根结点的索引 p
    k = p - j                           # 中序中根左侧的字符个数 = 左子树结点个数 k
    # 递归构造左子树：后序从 i 起长 k（左子树段在前）；中序从 j 起长 k
    t.lchild = _CreateBTree2(posts, i, ins, j, k)
    # 递归构造右子树：后序从 i+k 起长 n-k-1（紧挨在根之前）；中序从 p+1 起长 n-k-1
    t.rchild = _CreateBTree2(posts, i + k, ins, p + 1, n - k - 1)
    return t                            # 返回重建好的子树根结点

if __name__ == '__main__':
    pres = input().strip()              # 先序序列
    ins = input().strip()               # 中序序列
    posts = input().strip()             # 后序序列
    bt1 = CreateBTree1(pres, ins)       # 先序 + 中序重建
    bt2 = CreateBTree2(posts, ins)      # 后序 + 中序重建
    print(bt1.DispBTree())              # 第 1 行：括号表示法
    print(bt2.DispBTree())              # 第 2 行：括号表示法
