class CNode:
    def __init__(self, val):
        self.val = val                  # 数据域
        self.next = None                # 后继指针域

class CLinkList:
    def __init__(self, nums):
        self.head = CNode(0)            # 头结点（哨兵），不存数据
        self.head.next = self.head      # 空表时哨兵自环
        tail = self.head
        for v in nums:                  # 尾插法建表（循环链接）
            q = CNode(v)                # 新结点
            q.next = self.head          # 新结点的后继先回指哨兵
            tail.next = q               # 当前尾结点的后继指向新结点
            tail = q
'''
测试用例：
5 2
期望输出：
2 4 1 5 3
3
'''
# 此处为学生编写代码嵌入点位
# 设计函数 josephus
def josephus(link_list, out_list, m):
    out_tail = out_list.head            # 出列序列链的尾指针
    prev = link_list.head               # 报数者的环上前驱
    cur = prev.next                     # 从首元结点开始报数
    while cur is not link_list.head:
        count = 1
        while count < m:
            prev = cur                  # 前驱推进
            cur = cur.next
            if cur is link_list.head:   # 绕过哨兵继续报数
                cur = cur.next
                prev = link_list.head   # 跨哨兵后前驱是哨兵
            count += 1
        prev.next = cur.next            # 从环上摘下出列者
        out_tail.next = cur             # 出列者尾插到出列链
        out_tail = cur
        cur = cur.next                  # 从出列者的后继继续
        if cur is link_list.head:
            cur = cur.next
    out_tail.next = out_list.head       # 出列序列链封环

if __name__ == '__main__':
    n, m = map(int, input().split())
    nums = []
    for i in range(n):                  # 结点编号依次为 1..n
        nums.append(i + 1)

    link_list = CLinkList(nums)
    out_list = CLinkList([])
    josephus(link_list, out_list, m)

    vals = []
    p = out_list.head.next
    while p is not out_list.head:       # 沿环输出出列顺序
        vals.append(str(p.val))
        p = p.next
    print(' '.join(vals))
    print(vals[n - 1])                  # 优胜者编号（最后一个出列者）