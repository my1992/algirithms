# 约瑟夫斯问题
class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None
        self.flag = True


def create_link_list(n):
    head = Node(1)
    pre = head
    for i in range(2, n+1):
        new_node = Node(i)
        pre.next = new_node
        pre = new_node
    pre.next = head
    return head


def test():
    n = 5  # 总的数目
    m = 2  # 数的数目
    if m == 1:  # 如果是1的话，特殊处理，直接输出
        print(n)
    else:
        head = create_link_list(n)
        pre = None
        cur = head
        while cur.next != cur:  # 终止条件是节点的下一个节点指向本身
            for i in range(m-1):
                pre = cur
                cur = cur.next
            print(cur.value)
            pre.next = cur.next
            cur.next = None
            cur = pre.next
        print(cur.value)


if __name__ == '__main__':
    # test()
    head = create_link_list(5)
    pre_head = head.next
    while(pre_head != head):
        print(pre_head.value)
        pre_head = pre_head.next