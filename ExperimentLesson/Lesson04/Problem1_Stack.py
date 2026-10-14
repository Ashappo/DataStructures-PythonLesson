class Node:
    def __init__(self, data):
        self.data = data                # 数据域
        self.next = None                # 指针域

class LinkStack:
    def __init__(self):
        self.top = Node(None)           # 头结点（哨兵），不存数据

    def is_empty(self):
        return self.top.next is None

    def get_top(self):
        if self.top.next is None:       # 栈空
            return None
        return self.top.next.data
'''
测试用例：
([)]
期望输出：
no
'''
# 此处为学生编写代码嵌入点位
# 设计函数 push、pop、match
#设计函数 push
def push(st, e):
    p = Node(e)                         # 新建结点存放元素 e
    p.next = st.top.next                # 新结点接在头结点之后（栈顶）
    st.top.next = p

    #设计函数 pop
def pop(st):
    if st.top.next is None:             # 栈空，出栈失败
        return None
    p = st.top.next                     # p 指向栈顶结点
    st.top.next = p.next                # 从栈中摘下栈顶结点
    return p.data

    #设计函数 match
def match(st, s):
    flag = True                           # 先假定表达式中的括号配对
    for ch in s:
        if ch == '(' or ch == '[' or ch == '{':
            push(st, ch)                # 左括号：进栈
        elif ch == ')':
            if pop(st) != '(':          # 出栈元素与 ')' 不成对
                flag = False
        elif ch == ']':
            if pop(st) != '[':          # 出栈元素与 ']' 不成对
                flag = False
        elif ch == '}':
            if pop(st) != '{':          # 出栈元素与 '}' 不成对
                flag = False
        if not flag:
            break                       # 已判定不配对，提前结束扫描
    if flag:
        flag = st.is_empty()              # 扫描结束，栈空才算配对
    return flag

if __name__ == '__main__':
    s = input().strip()

    st = LinkStack()
    if match(st, s):
        print('yes')
    else:
        print('no')