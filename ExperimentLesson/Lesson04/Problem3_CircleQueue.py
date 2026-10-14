MaxSize = 1000                          # 环形队列容量（牺牲一个单元区分队空与队满）

class CircQueue:
    def __init__(self):
        self.data = [None] * MaxSize    # 环形存储区
        self.front = 0                  # 队首指针
        self.rear = 0                   # 队尾指针

    def is_empty(self):
        return self.front == self.rear
'''
测试用例：
12345ab6
期望输出：
12
3456
'''

# 此处为学生编写代码嵌入点位
# 设计函数 en_queue、de_queue、fun
'''
    @brief        环形队列入队（在 CircQueue 外部补充的基本运算）
    @details      队满时入队失败并返回 False；否则把队尾指针环形后移一个位置，把元素 e 存入该
                  位置并返回 True。该队列牺牲一个存储单元区分队空与队满，最多容纳 MaxSize - 1 个元素。
    @param[in]    q          环形队列对象，用法见调用示例
    @param[in]    e          待入队的元素
    @return       入队成功返回 True，队满返回 False
    @code         调用示例：
          en_queue(q, '5')              # 把字符 '5' 入队
'''
#设计函数 en_queue
def en_queue(q, e):
# 队满时入队失败（牺牲一个单元区分队空与队满）
    if (q.rear + 1) % MaxSize == q.front:
        return False
    q.rear = (q.rear + 1) % MaxSize     # 队尾指针环形后移
    q.data[q.rear] = e                  # 存入元素 e
    return True

'''
    @brief        环形队列出队（在 CircQueue 外部补充的基本运算）
    @details      队空时出队失败并返回 None；否则把队首指针环形后移一个位置，返回该位置的元素。
    @param[in]    q          环形队列对象
    @return       出队成功返回队首元素；队空返回 None
    @code         调用示例：
          e = de_queue(q)               # 队首元素出队，队空时得到 None
'''
#设计函数 de_queue
def de_queue(q):
    if q.front == q.rear:               # 队空，出队失败
        return None
    q.front = (q.front + 1) % MaxSize   # 队首指针环形后移
    return q.data[q.front]

'''
    @brief        按规则处理输入序列并输出结果
    @details      从左到右扫描序列 s：数字字符入队（队满则丢弃该字符）；小写字母使队首元素出队
                  （队空则忽略）；其他字符结束处理。第一行输出出队序列，第二行输出队列中剩余的
                  字符（从队头到队尾），两行均可能在内容为空时输出空行。
    @param[in]    q          由裁判程序创建的空环形队列对象
    @param[in]    s          待处理的字符序列（不含空白字符）
    @return       无需返回值，直接输出两行结果
    @code         调用示例：
          q = CircQueue()
          fun(q, '12345ab6')            # 依次输出出队序列与队列剩余字符
'''
#设计函数 fun
def fun(q, s):
    for ch in s:
        if '0' <= ch <= '9':
            en_queue(q, ch)             # 数字字符：进队（队满自动丢弃）
        elif 'a' <= ch <= 'z':
            e = de_queue(q)
            # `print()` 默认打印完内容会**自动换行**，也就是默认 `end='\n'`。
            # - `end=''`：把打印结尾改成**空字符串，不换行**
            if e is not None:
                print(e, end='')        # 出队成功才输出该字符
        else:
            break                       # 其他字符：输入结束
    print()                             # 第一行：出队序列（可能为空行）

    while not q.is_empty():             # 第二行：队列中剩余的字符
        print(de_queue(q), end='')
    print()

if __name__ == '__main__':
    s = input().strip()

    q = CircQueue()
    fun(q, s)