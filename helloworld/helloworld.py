class Node(object):

    def __init__(self, data=None, l_child=None, r_child=None):
        self.data = data
        self.l_child = l_child
        self.r_child = r_child


class BinaryTree(object):

    def __init__(self, node=None):
        self.root = node

    def add(self, item=None):
        node = Node(item)
        if not self.root:
            self.root = node
        else:
            node_queue = list()
            node_queue.append(self.root)
            while 1:
                cur_node = node_queue.pop(0)
                if not cur_node.l_child:
                    cur_node.l_child = node
                    return
                elif not cur_node.r_child:
                    cur_node.r_child = node
                    return
                else:
                    node_queue.append(cur_node.l_child)
                    node_queue.append(cur_node.r_child)


a = BinaryTree()
for i in range(10):
    a.add(i)


def print_tree(x):
    if x.data is not None:
        print(x.data)
        if x.l_child:
            print_tree(x.l_child)
        if x.r_child:
            print_tree(x.r_child)


print_tree(a.root)
