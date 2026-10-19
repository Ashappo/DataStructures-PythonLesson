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
    # 核心优化：把抽象的优先级规则做成字典，数字越大优先级越高，小学生都能看懂
    priority = {'+':1, '-':1, '*':2, '/':2, '(':0}
    res = []  # 用列表存结果元素，最后统一拼字符串，避免手动补空格漏写
    i = 0
    n = len(exp)
    while i < n:
        ch = exp[i]

        # 分支1：连续数字整段收集成一个操作数（比如'56'是一个数，不是两个字符）
        if ch.isdigit():
            num = []
            while i < n and exp[i].isdigit():
                num.append(exp[i])
                i += 1
            res.append(''.join(num))
            continue  # 已经把游标移到数字末尾，跳过后面的重复步长更新

        # 分支2：左括号直接压栈，是栈里的"优先级挡板"
        if ch == '(':
            st.push(ch)
            i += 1
            continue

        # 分支3：右括号就把栈里的运算符往外倒，直到碰到左括号
        if ch == ')':
            while not st.is_empty() and st.get_top() != '(':
                res.append(st.pop())
            st.pop()  # 把没用的左括号从栈里扔掉，不写进结果
            i += 1
            continue

        # 分支4：普通运算符——原来绕死人的优先级判断，现在就是比大小
        while (not st.is_empty()
               and st.get_top() != '('
               and priority[st.get_top()] >= priority[ch]):
            res.append(st.pop())  # 栈顶运算符优先级更高，必须先算，弹出来记到结果
        st.push(ch)  # 把当前运算符压栈
        i += 1

    # 扫描完所有字符，把栈里剩下的运算符全部弹出来
    while not st.is_empty():
        res.append(st.pop())

    # 统一用空格分隔所有元素，格式和题目要求完全一致
    return ' '.join(res) + ' '


if __name__ == '__main__':
    exp = input().strip()

    st = SqStack()
    print(trans(st, exp).strip())