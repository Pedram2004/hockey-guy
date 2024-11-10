from playground import PlayGround
from search_tree_node import Node
from collections import deque
import heapq


class STree:
    def __init__(self, initial_state: PlayGround):
        self.__root = Node(initial_state)

    @staticmethod
    def input_conversion() -> "STree":
        num_rows, _ = map(int, input().split(' '))
        cost_matrix: list[list] = []
        player: tuple = (0, 0)
        pucks: list[tuple[tuple, bool]] = []
        obstacles: list[tuple] = []
        goals: list[tuple] = []
        for i in range(num_rows):
            cost_matrix[i] = []
            for j, element in enumerate(input().split(' ')):
                if element.isdigit():
                    cost_matrix[i].append(int(element))
                elif element == 'X':
                    #a hypothetical situation needs to be confirmed
                    cost_matrix[i].append(0)
                    obstacles.append((i, j))
                else:
                    cost_matrix[i].append(int(element[0]))

                    match element[1]:
                        case 'P':
                            player = (i, j)
                        case 'G':
                            goals.append((i, j))
                        case 'B':
                            pucks.append(((i, j), False))

        PlayGround.set_class_vars(cost_matrix)
        initial_state = PlayGround(player=player, pucks=pucks, obstacles=obstacles, goals=goals)
        return STree(initial_state)

    def __search(self, priority_queue, pop_func, append_func) -> Node | None:
        visited_nodes = {self.__root, }
        while priority_queue:
            current_node = pop_func(priority_queue)
            current_node.create_children()
            print(f"\n----------------\n{current_node}\n-----------------------\n")
            for child_node in current_node.children:
                if child_node.is_final:
                    return child_node
                elif child_node not in visited_nodes:
                    visited_nodes.add(child_node)
                    append_func(priority_queue, child_node)

        return None

    def breadth_first_search(self) -> Node | None:
        return self.__search(deque([self.__root]), deque.popleft, deque.append)

    def depth_first_search(self) -> Node | None:
        return self.__search(deque([self.__root]), deque.pop, deque.append)

    def uniform_cost_search(self) -> Node | None:
        return self.__search([self.__root], heapq.heappop, heapq.heappush)

    def __depth_limited_search(self, current_node: Node, depth: int, _visited_nodes: set) -> (Node | None, bool):
        if depth == 0:
            if current_node.is_final:
                return current_node, True
            else:
                return None, True

        elif depth > 0:
            any_remaining_nodes = False
            current_node.create_children()
            for child_node in current_node.children:
                goal_node, is_nodes_remain = self.__depth_limited_search(child_node, depth - 1, _visited_nodes)
                if goal_node is not None:
                    return goal_node, True
                if is_nodes_remain:
                    any_remaining_nodes = True

            return None, any_remaining_nodes

    def iterative_deepening_search(self) -> Node | None:
        max_depth = 0
        is_nodes_remain = True
        while is_nodes_remain:
            visited_nodes = {self.__root, }
            result, is_nodes_remain = self.__depth_limited_search(self.__root, max_depth, visited_nodes)
            max_depth += 1
            if result is not None:
                return result

        return None
