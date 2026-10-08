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
8
1 2 1 3 2 1 5 3
期望输出：
1 2 3 5
'''
# 此处为学生编写代码嵌入点位
#设计函数 remove_duplicates
def remove_duplicates(link_list):
    p = link_list.head.next             # 基准结点（首次出现者）
    while p is not None:
        q = p.next                      # 待查重结点
        while q is not None:
            nxt = q.next                # 暂存后继，防止断链
            if q.val == p.val:          # 与基准值重复
                q.prior.next = q.next   # 双向摘除重复结点
                if q.next is not None:  # 后继存在时回接 prior
                    q.next.prior = q.prior
            q = nxt                     # 推进到下一个待查结点
        p = p.next                      # 下一个基准结点

if __name__ == '__main__':
    n = int(input())
    nums = []
    for v in input().split():
        nums.append(int(v))

    link_list = DLinkList(nums)
    remove_duplicates(link_list)

    vals = []
    p = link_list.head.next
    while p is not None:
        vals.append(str(p.val))
        p = p.next
    print(' '.join(vals))