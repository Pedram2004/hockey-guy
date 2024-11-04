from search_tree_node import Node
from collections import deque
import heapq


class STree:
    def __init__(self, root: Node):
        self.__root = root

    def uninformed_search(self, priority_queue_class, pop_func, append_func) -> Node | None:

        class PriorityQueue(priority_queue_class):
            def __init__(self, assigned_iter):
                super().__init__(assigned_iter)

            def pop_method(self):
                return pop_func(self)

            def append_method(self, item):
                append_func(self, item)

        priority_queue = PriorityQueue([self.__root])
        visited_nodes = {self.__root, }
        while priority_queue:
            current_node = priority_queue.pop_method()
            current_node.create_children()
            for child_node in current_node.children:
                if child_node.is_final:
                    return child_node
                elif child_node not in visited_nodes:
                    visited_nodes.add(child_node)
                    priority_queue.append_method(child_node)
        return None

    def breadth_first_search(self):
        return self.uninformed_search(deque, deque.popleft, deque.append)

    def depth_first_search(self):
        return self.uninformed_search(deque, deque.pop, deque.append)

    def uniform_cost_search(self):
        return self.uninformed_search(heapq, heapq.heappush, heapq.heappop)


if __name__ == "__main__":
    from playground import PlayGround

    playground = PlayGround(
        player=(0, 0),
        obstacles=[(2, 1), (2, 2)],
        pucks=[((3, 1), False), ((3, 3), False)],
        goals=[(4, 1), (1, 4)]
    )
    playground.set_class_vars(
        cost_matrix=((1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1)))
    node_root = Node(state=playground)
    tree = STree(root=node_root)
    result = tree.depth_first_search()
    print("\n\n-------------------------\nresult:\n", result, "\n-------------------------")

    print(result.get_full_direction())
