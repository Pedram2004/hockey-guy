from search_tree_node import Node
from collections import deque
import heapq


class STree:
    def __init__(self, root: Node):
        self.__root = root

    def uninformed_search(self, priority_queue, pop_func, append_func) -> Node | None:

        visited_nodes = {self.__root, }
        while priority_queue:
            current_node = pop_func(priority_queue)
            current_node.create_children()

            for child_node in current_node.children:
                if child_node.is_final:
                    return child_node
                elif child_node not in visited_nodes:
                    visited_nodes.add(child_node)
                    append_func(priority_queue, child_node)

        return None

    def breadth_first_search(self):
        return self.uninformed_search(deque([self.__root]), deque.popleft, deque.append)

    def depth_first_search(self):
        return self.uninformed_search(deque([self.__root]), deque.pop, deque.append)

    def uniform_cost_search(self):
        return self.uninformed_search([self.__root], heapq.heappop, heapq.heappush)

    def iterative_deepening_search(self):
        max_depth = 1000
        for i in range(max_depth):
            pass
        # depth_first_search here with changes


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
    result = tree.uniform_cost_search()
    print("\n\n-------------------------\nresult:\n", result, "\n-------------------------")
    print(result.get_full_direction())
    result = tree.breadth_first_search()
    print("\n\n-------------------------\nresult:\n", result, "\n-------------------------")

    print(result.get_full_direction())
