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
                    # print(f"\n----------------\n{child_node}\n-----------------------\n")
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


if __name__ == "__main__":
    from playground import PlayGround

    playground = PlayGround(
        player=(0, 0),
        obstacles=[(2, 1), (2, 2)],
        pucks=[((3, 1), False), ((3, 3), False)],
        goals=[(4, 1), (1, 4)]
    )
    playground.set_class_vars(
        cost_matrix=((1, 1, 1, 1, 1),
                     (1, 1, 1, 1, 1),
                     (1, 1, 1, 1, 1),
                     (1, 1, 1, 1, 1),
                     (1, 1, 1, 1, 1)))
    node_root = Node(state=playground)
    tree = STree(root=node_root)
    r1 = tree.uniform_cost_search()

    r = tree.iterative_deepening_search()
    print("\n\n-------------------------\nresult:\n", r, "\n-------------------------")
    print(r1.get_full_direction())
    print(r.get_full_direction())
