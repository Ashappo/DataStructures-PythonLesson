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
1 2 3 2 1
'''
# 此处为学生编写代码嵌入点位
# 设计函数 is_palindrome
def is_palindrome(link_list):
    p = link_list.head.next             # 左指针：首元结点
    q = link_list.head                  # 从哨兵出发定位尾结点
    while q.next is not None:
        q = q.next
    while p is not q and p.prior is not q:
        if p.val != q.val:              # 首尾对撞比较
            return False
        p = p.next                      # 双指针向中间逼近
        q = q.prior
    return True

if __name__ == '__main__':
    n = int(input())
    nums = []
    for v in input().split():
        nums.append(int(v))

    link_list = DLinkList(nums)
    if is_palindrome(link_list):
        print(1)
    else:
        print(0)