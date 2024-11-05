from search_tree_node import Node
from collections import deque
from math import inf as math_inf
import heapq


class STree:
    def __init__(self, root: Node):
        self.__root = root

    def uninformed_search(self, priority_queue, pop_func, append_func, search_max_depth: float = math_inf) -> Node | None:

        visited_nodes = {self.__root, }
        while priority_queue:
            current_node = pop_func(priority_queue)
            current_node.create_children()
            print(f"\n----------------\n{current_node}\n-----------------------\n")
            for child_node in current_node.children:
                if child_node.depth <= search_max_depth:
                    if child_node.is_final:
                        return child_node
                    elif child_node not in visited_nodes:
                        visited_nodes.add(child_node)
                        append_func(priority_queue, child_node)

        return None

    def breadth_first_search(self) -> Node | None:
        return self.uninformed_search(deque([self.__root]), deque.popleft, deque.append)

    def depth_first_search(self, max_depth=math_inf) -> Node | None:
        return self.uninformed_search(deque([self.__root]), deque.pop, deque.append, search_max_depth=max_depth)

    def uniform_cost_search(self) -> Node | None:
        return self.uninformed_search([self.__root], heapq.heappop, heapq.heappush)

    def iterative_deepening_search(self) -> Node | None:
        max_depth = 1000

        for i in range(max_depth):
            print (f"depth ----> {i}\n")
            result = self.depth_first_search(i)
            if result is not None:
                return result

        return None