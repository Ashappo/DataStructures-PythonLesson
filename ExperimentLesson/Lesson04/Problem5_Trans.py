MaxSize = 1000                          # 顺序栈的容量

class SqStack:
    def __init__(self):
        self.data = [None] * MaxSize    # 定长存储区
        self.top = -1                   # 栈指针

    def is_empty(self):
        return self.top == -1

    def push(self, e):
        if self.top == MaxSize - 1:     # 栈满，即栈上溢出
            return False
        self.top += 1
        self.data[self.top] = e
        return True

    def pop(self):
        if self.top == -1:              # 栈空，即栈下溢出
            return None
        e = self.data[self.top]
        self.top -= 1
        return e

    def get_top(self):
        if self.top == -1:              # 栈空
            return None
        return self.data[self.top]

'''
测试用例：
(56-20)/(4+2*3)
期望输出：
56 20 - 4 2 3 * + /
'''
# 此处为学生编写代码嵌入点位
# 设计函数 trans

'''
    @brief        中缀表达式转换为后缀表达式
    @details      借助顺序栈暂存运算符：操作数整段追加到结果串并以空格分隔；左括号直接进栈；
                  右括号把左括号之上的运算符依次弹出并追加；其余运算符先弹出栈中所有优先级不低于
                  它的运算符，再进栈；扫描结束后弹出栈中剩余的运算符。结果作为返回值返回。
    @param[in]    st         由裁判程序创建的空顺序栈对象（用作运算符栈）
    @param[in]    exp        中缀表达式字符串（不含空白字符）
    @return       转换得到的后缀表达式字符串，各操作数与运算符之间以一个空格分隔
    @code         调用示例：
          st = SqStack()
          trans(st, '(56-20)/(4+2)')    # 返回 '56 20 - 4 2 + / '
'''
#设计函数 trans
def trans(st, exp):
    post = ''                           # 后缀表达式结果串
    i = 0
    while i < len(exp):
        ch = exp[i]
        if ch >= '0' and ch <= '9':
            while i < len(exp) and exp[i] >= '0' and exp[i] <= '9':
                post += exp[i]          # 操作数整段复制
                i += 1
            post += ' '                 # 操作数之间以空格分隔
        elif ch == '(':                 # 左括号：直接进栈
            st.push(ch)
            i += 1
        elif ch == ')':
            while not st.is_empty() and st.get_top() != '(':
                e = st.pop()            # 弹出左括号之上的运算符
                post += e + ' '
            st.pop()                    # 弹出左括号，不写入后缀表达式
            i += 1
        else:
            while not st.is_empty() and st.get_top() != '(':
                top = st.get_top()
                if (ch == '*' or ch == '/') and (top == '+' or top == '-'):
                    break               # 栈顶运算符优先级更低，暂不弹出
                e = st.pop()            # 栈顶运算符优先级不低于当前运算符
                post += e + ' '
            st.push(ch)                 # 当前运算符进栈
            i += 1
    while not st.is_empty():
        e = st.pop()                    # 弹出栈中剩余的运算符
        post += e + ' '
    return post

if __name__ == '__main__':
    exp = input().strip()

    st = SqStack()
    print(trans(st, exp).strip())