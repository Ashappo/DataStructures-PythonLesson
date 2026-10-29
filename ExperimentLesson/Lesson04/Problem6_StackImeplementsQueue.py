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
8
1 a
1 b
2
1 c
2
2
2
2
期望输出：
a
b
c
EMPTY
EMPTY
'''
# 此处为学生编写代码嵌入点位
# 设计函数 en_queue、de_queue
'''
    @brief        用两个顺序栈实现入队
    @details      直接把元素压入用于入队的顺序栈 s1；顺序栈满时入队失败。
    @param[in]    s1         由裁判程序创建的用于入队的顺序栈对象
    @param[in]    e          待入队的元素
    @return       入队成功返回 True，栈满返回 False
    @code         调用示例：
          en_queue(s1, 'a')             # 字符 'a' 入队
'''
#设计函数 en_queue
def en_queue(s1, e):
    return s1.push(e)                   # 入队：直接把元素压入栈 s1

'''
    @brief        用两个顺序栈实现出队
    @details      若 s2 非空则直接弹出 s2 的栈顶元素；否则在 s1 非空时把 s1 中的元素依次弹出并
                  压入 s2（顺序反转，再弹出即为队首元素），然后弹出 s2 的栈顶；s1 与 s2 都为空时
                  队列为空，出队失败。
    @param[in]    s1         由裁判程序创建的用于入队的顺序栈对象
    @param[in]    s2         由裁判程序创建的用于出队的顺序栈对象
    @return       出队成功返回队首元素；队列为空返回 None
    @code         调用示例：
          e = de_queue(s1, s2)          # 队首元素出队，队列为空时得到 None
'''
#设计函数 de_queue
def de_queue(s1, s2):
    if s2.is_empty():                   # 只有 s2 为空时才需要把 s1 倒入
        while not s1.is_empty():
            s2.push(s1.pop())           # s1 的元素依次弹出并压入 s2
    if s2.is_empty():
        return None                     # 两栈都空：队列为空，出队失败
    return s2.pop()                     # 弹出 s2 的栈顶即为队首元素

if __name__ == '__main__':
    n = int(input())

    s1 = SqStack()
    s2 = SqStack()
    for _ in range(n):
        parts = input().split()
        op = int(parts[0])
        if op == 1:                     # 入队
            en_queue(s1, parts[1])
        else:                           # 出队
            c = de_queue(s1, s2)
            if c is None:
                print('EMPTY')          # 队空
            else:
                print(c)