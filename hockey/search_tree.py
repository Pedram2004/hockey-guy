from search_tree_node import Node
from collections import deque
import heapq



class STree:
    def __init__(self, root: Node):
        self.__root = root

    def breadth_first_search(self) -> Node:
        queue = deque([self.__root])
        visited = set()
        visited.add(self.__root)
        while queue:
            current_node = queue.popleft()
            print("\n-------------------------\ncurrent_node:\n", current_node, "\n-------------------------")
            current_node.create_children()
            for child in current_node.children:
                if child.is_final:
                    return child
                elif child not in visited:
                    print("child:\n", child)
                    visited.add(child)
                    queue.append(child)
        return None

if __name__ == "__main__":
    from playground import PlayGround
    playground = PlayGround(
        player=(0, 0),
        obstacles=[(2, 1), (2, 2)],
        pucks=[((3, 1), False), ((3, 3), False)],
        goals=[(4, 1), (1, 4)]
    )
    playground.set_class_vars(cost_matrix=((1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1), (1, 1, 1, 1, 1)))
    root = Node(state=playground)
    tree = STree(root=root)
    result = tree.bfs()
    print("\n\n-------------------------\nresult:\n", result, "\n-------------------------")

    print(result.get_full_direction())