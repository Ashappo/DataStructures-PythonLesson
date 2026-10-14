MaxSize = 1000                          # 顺序栈与顺序队列的容量

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

class SqQueue:
    def __init__(self):
        self.data = [None] * MaxSize    # 定长存储区
        self.front = -1                 # 队头指针
        self.rear = -1                  # 队尾指针

    def is_empty(self):
        return self.front == self.rear

    def en_queue(self, e):
        if self.rear == MaxSize - 1:    # 队满，即队上溢出
            return False
        self.rear += 1
        self.data[self.rear] = e
        return True

    def de_queue(self):
        if self.front == self.rear:     # 队空，即队下溢出
            return None
        self.front += 1
        return self.data[self.front]
'''
测试用例：
abcda
期望输出：
no
'''

# 此处为学生编写代码嵌入点位
# 设计函数 palindrome
'''
    @brief        仅借助栈和队列判断字符串是否为回文
    @details      先把 s 中的每个字符依次进栈、入队；再反复出栈与出队各取一个字符并比较，出现不同
                  即不是回文；栈空时全部对应字符都相同则为回文。全程只允许使用裁判程序提供的
                  SqStack 与 SqQueue，不得用下标直接比较首尾字符。
    @param[in]    st          由裁判程序创建的空顺序栈对象
    @param[in]    q           由裁判程序创建的空顺序队列对象
    @param[in]    s           待判断的字符串（不含空白字符）
    @return       是回文返回 True，否则返回 False
    @code         调用示例：
          st = SqStack()
          q = SqQueue()
          palindrome(st, q, 'abcba')        # 返回 True
'''
#设计函数 palindrome
def palindrome(st, q, s):
    same = True                         # 先假定是回文
    for ch in s:
        st.push(ch)                     # 每个字符依次进栈
        q.en_queue(ch)                  # 每个字符依次入队
    while same and not st.is_empty():
        e1 = st.pop()                   # 出栈：从后向前取字符
        e2 = q.de_queue()               # 出队：从前向后取字符
        if e1 != e2:
            same = False                # 对应位置的字符不同，不是回文
    return same

if __name__ == '__main__':
    s = input().strip()

    st = SqStack()
    q = SqQueue()
    if palindrome(st, q, s):
        print('yes')
    else:
        print('no')