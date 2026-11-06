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
# 题目 5：层次遍历与分层输出 —— LevelOrder / DispLevel
# ============================================================
'''
设计思路（整体）：
    两题均基于队列实现层次遍历（BFS）：用 collections.deque 作
    普通队列（append 进队、popleft 出队，两端操作均 O(1)）。

    【LevelOrder 层次遍历序列】
      根结点先进队；队不空时循环：出队一个结点并访问（输出其值），
      若有左孩子则左孩子进队，若有右孩子则右孩子进队。
      队列为空时所有结点恰好按"从上到下、从左到右"的层次次序输出一遍。

    【DispLevel 按层分行输出】
      在 LevelOrder 的队列框架上增加"层末标记 last"：
        * last 始终记录"当前层最右边的结点"（初始为根）；
        * 每当出队的结点恰好是 last（p is last，用身份比较而非值比较），
          说明本层已全部处理完毕：换行、层号 curl 加 1、输出新层号，
          并把 last 更新为此时队尾元素 qu[-1] —— 队尾正是下一层
          最后进队的结点，即下一层的最右结点；
        * 重复直到队空。
      注意先输出层号 "k:"，之后每个结点值前带一个空格，恰好构成
      "k: v1 v2 v3" 的格式。

    时间复杂度均为 O(n)，空间复杂度 O(n)（队列最多存一层结点，
    最坏约 O(n/2)）。

测试用例：
A(B(D,E(H(J,K(L,M(,N))))),C(F,G(,I)))
期望输出：
A B C D E F G H I J K L M N
1: A
2: B C
3: D E F G
4: H I
5: J K
6: L M
7: N
'''
from collections import deque           # 引入双端队列模块，作普通队列使用

# 此处为学生编写代码嵌入点位
# 设计函数 LevelOrder、DispLevel

# 普通层次遍历：所有结点输出在一行
def LevelOrder(bt):
    if bt.b is None:
        return
    qu = deque()
    qu.append(bt.b)                # 根结点入队
    while len(qu) > 0:             # 队列不为空循环
        p = qu.popleft()           # 队头结点出队
        print(p.data, end=' ')     # 访问该结点
        if p.lchild is not None:   # 如果有左孩子，左孩子入队
            qu.append(p.lchild)
        if p.rchild is not None:   # 如果有右孩子，右孩子入队
            qu.append(p.rchild)
    print()                        # 遍历完成，换行

# 按层分行输出二叉树，带层号
def DispLevel(bt):
    if bt.b is None:
        return
    qu = deque()                   # 创建队列
    curl = 1                       # 当前层号，根为第 1 层
    last = bt.b                    # last：标记本层最右侧结点
    qu.append(bt.b)                # 根结点入队
    # print('%d:' % curl, end='')
    print(f"{curl}:", end="")      # 先输出第一层的层号，不换行
    while len(qu) > 0:             # 队列非空
        p = qu.popleft()           # 队头结点出队
        print(' ' + p.data, end='')# 输出结点数据，前面带空格
        # 左孩子存在则入队
        if p.lchild is not None:
            qu.append(p.lchild)
        # 右孩子存在则入队
        if p.rchild is not None:
            qu.append(p.rchild)
        # 判断：刚出队的结点是不是本层最右结点
        if p is last:
            if len(qu) > 0:         # 队列还有结点，说明存在下一层
                print()            # 当前层输出完毕，换行
                curl += 1          # 层号 +1
                print(f"{curl}:", end="")  # 打印新一层层号
                last = qu[ len(qu) - 1 ]
                # last = qu[-1]      # qu[-1]：下一层最后入队结点，即下一层最右
    print()                        # 最后一层结束后换行

if __name__ == '__main__':
    s = input().strip()                 # 括号表示法串
    bt = BTree()                        # 二叉树对象
    bt.b = CreateBTree(s)               # 建树并设置根结点
    LevelOrder(bt)                      # 第 1 行：层次遍历序列
    DispLevel(bt)                       # 后续 h 行：分层输出
