class CDNode:
    def __init__(self, val):
        self.val = val                  # 数据域
        self.prior = None               # 前驱指针域
        self.next = None                # 后继指针域

class CDLinkList:
    def __init__(self, nums):
        self.head = CDNode(0)           # 头结点（哨兵），不存数据
        self.head.prior = self.head     # 哨兵自环（前驱方向）
        self.head.next = self.head      # 哨兵自环（后继方向）
        tail = self.head
        for v in nums:                  # 尾插法建表（循环双向链接）
            q = CDNode(v)               # 新结点
            q.prior = tail              # 新结点的前驱指向当前尾结点
            q.next = self.head          # 新结点的后继回指哨兵
            tail.next = q               # 当前尾结点的后继指向新结点
            tail = q
        self.head.prior = tail          # 哨兵的前驱指向尾结点
'''
测试用例：
6 5
5 3 8 1 9 4
期望输出：
3 1 4 5 8 9
'''
# 此处为学生编写代码嵌入点位
# 设计函数 partition_list
def partition_list(link_list, x):
    head = link_list.head
    small_tail = head                   # 前段（值小于 x）的尾指针
    big_head = None                     # 后段（值大于等于 x）的首结点
    big_tail = None                     # 后段的尾指针
    p = head.next
    while p is not head:
        nxt = p.next                    # 暂存后继，防止断链
        if p.val < x:                   # 摘下接到前段尾部（双向）
            small_tail.next = p
            p.prior = small_tail
            small_tail = p
        else:
            if big_head is None:        # 后段尚无结点
                big_head = p
            else:
                big_tail.next = p       # 双向接到后段尾部
                p.prior = big_tail
            big_tail = p
        p = nxt
    if big_head is not None:            # 两段拼接并封环
        small_tail.next = big_head
        big_head.prior = small_tail
        big_tail.next = head
        head.prior = big_tail
    else:                               # 后段为空：前段直接封环
        small_tail.next = head
        head.prior = small_tail

if __name__ == '__main__':
    n, x = map(int, input().split())
    nums = []
    for v in input().split():
        nums.append(int(v))

    link_list = CDLinkList(nums)
    partition_list(link_list, x)

    vals = []
    p = link_list.head.next
    while p is not link_list.head:      # 顺环输出全部结点
        vals.append(str(p.val))
        p = p.next
    print(' '.join(vals))