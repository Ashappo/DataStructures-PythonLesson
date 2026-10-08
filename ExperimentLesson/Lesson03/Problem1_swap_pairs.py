class DNode:
    def __init__(self, val):
        self.val = val                  # 数据域
        self.prior = None               # 前驱指针域
        self.next = None                # 后继指针域

class DLinkList:
    def __init__(self, nums):
        self.head = DNode(0)            # 头结点（哨兵），不存数据
        tail = self.head
        for v in nums:                  # 尾插法建表（双向链接）
            q = DNode(v)                # 新结点
            q.prior = tail              # 新结点的前驱指向当前尾结点
            tail.next = q               # 当前尾结点的后继指向新结点
            tail = q
'''
测试用例：
5
1 2 3 4 5
期望输出：
2 1 4 3 5
'''
# 此处为学生编写代码嵌入点位
#设计函数 swap_pairs
def swap_pairs(link_list):
    p = link_list.head                  # p 始终是待交换对的前驱
    while p.next is not None and p.next.next is not None:
        a = p.next                      # 本对第 1 个结点
        b = a.next                      # 本对第 2 个结点
        a.next = b.next                 # a 接到 b 原来的后继
        if b.next is not None:          # 后继存在时回接 prior
            b.next.prior = a
        b.next = a                      # b、a 互指完成换位
        b.prior = p
        a.prior = b
        p.next = b                      # 前驱改指 b
        p = a                           # 前驱推进到本对第 2 个

if __name__ == '__main__':
    n = int(input())
    nums = []
    for v in input().split():
        nums.append(int(v))

    link_list = DLinkList(nums)
    swap_pairs(link_list)

    vals = []
    p = link_list.head.next
    while p is not None:
        vals.append(str(p.val))
        p = p.next
    print(' '.join(vals))