class DataNode:
    def __init__(self, data):
        self.data = data                # 数据域
        self.next = None                # 指针域

class LinkQueue:
    def __init__(self):
        self.front = None               # 队头指针
        self.rear = None                # 队尾指针

    def is_empty(self):
        return self.rear is None
'''
测试用例：
8
1 101
2
3
1 202
2
2
3
4
期望输出：
101

202
-1

END
'''
# 此处为学生编写代码嵌入点位
# 设计函数 en_queue、de_queue
'''
    @brief        链队列入队（在 LinkQueue 外部补充的基本运算）
    @details      新建一个数据结点存放元素 e；若队列为空（rear 为 None），入队后队头与队尾都指向
                  该结点；否则把新结点链到队尾并更新队尾指针。
    @param[in]    q          链队列对象，用法见调用示例
    @param[in]    e          待入队的元素
    @return       入队成功返回 True
    @code         调用示例：
          en_queue(q, 101)              # 病例号 101 排队
'''
#设计函数 en_queue
def en_queue(q, e):
    p = DataNode(e)                     # 新建数据结点存放元素 e
    if q.rear is None:                  # 原队列为空
        q.front = p                     # 队头指向新结点
        q.rear = p                      # 队尾指向新结点
    else:
        q.rear.next = p                 # 新结点链到队尾
        q.rear = p                      # 更新队尾指针
    return True

'''
    @brief        链队列出队（在 LinkQueue 外部补充的基本运算）
    @details      队列为空（rear 为 None）时出队失败并返回 None；否则摘下队头结点，返回其数据域，
                  并在出队后队列变空时把 rear 置为 None，以保证 is_empty 判断正确。
    @param[in]    q          链队列对象
    @return       出队成功返回队首元素；队空返回 None
    @code         调用示例：
          e = de_queue(q)               # 队首病例号出队，队空时得到 None
'''
#设计函数 de_queue
def de_queue(q):
    if q.rear is None:                  # 队空，出队失败
        return None
    p = q.front                         # p 指向队头结点
    q.front = p.next                    # 队头后移一个结点
    if q.front is None:
        q.rear = None                   # 出队后队列变空，队尾必须置回 None
    return p.data

if __name__ == '__main__':
    n = int(input())

    q = LinkQueue()
    for _ in range(n):
        parts = input().split()
        op = int(parts[0])
        if op == 1:                     # 排队
            en_queue(q, int(parts[1]))
        elif op == 2:                   # 就诊
            x = de_queue(q)
            if x is None:
                print(-1)               # 队空：无人就诊
            else:
                print(x)
        elif op == 3:                   # 查看排队
            vals = []
            p = q.front
            while p is not None:
                vals.append(str(p.data))
                p = p.next
            print(' '.join(vals))
        else:                           # 下班：结束运行
            print('END')
            break