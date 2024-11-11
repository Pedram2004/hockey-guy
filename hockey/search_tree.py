from .playground import PlayGround
from .search_tree_node import Node
from collections import deque
import heapq
from typing import Callable


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

            cost_matrix.append([])
            for j, element in enumerate(input().split(' ')):
                if element.isdigit():
                    cost_matrix[i].append(int(element))
                elif element == 'X':
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

    def __search(self, priority_queue: list[Node], pop_func: Callable[[list[Node]], Node], append_func: Callable[[list[Node], Node], None]) -> Node | None:
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

    def breadth_first_search(self) -> Node | None:
        return self.__search(deque([self.__root]), deque.popleft, deque.append)

    def depth_first_search(self) -> Node | None:
        return self.__search(deque([self.__root]), deque.pop, deque.append)

    def uniform_cost_search(self) -> Node | None:
        self.__root.comparison_mode = "g"
        return self.__search([self.__root], heapq.heappop, heapq.heappush)

    def __depth_limited_search(self, max_depth : int) -> tuple[Node | None, bool]:
        visited_nodes = {self.__root, }
        stack = deque([self.__root])
        is_nodes_remaining = False

        while stack:
            current_node = stack.pop()

            if current_node.depth <= max_depth:
                current_node.create_children()

            for child_node in current_node.children:
                if child_node.is_final:
                    return child_node, False
                elif child_node not in visited_nodes:

                    if child_node.depth <= max_depth:
                        visited_nodes.add(child_node)
                        stack.append(child_node)
                    elif child_node.depth == max_depth + 1:
                        is_nodes_remaining = True

        return None, is_nodes_remaining

    def iterative_deepening_search(self) -> Node | None:
        maximum_depth = 0
        is_nodes_remain = True

        while is_nodes_remain:
            result, is_nodes_remain= self.__depth_limited_search(maximum_depth)
            maximum_depth += 1

            if result is not None:
                return result

        return None
    
    def best_first_search(self) -> Node | None:
        self.__root.comparison_mode = "h"
        return self.__search([self.__root], heapq.heappop, heapq.heappush)

    def a_star_search(self) -> Node | None:
        self.__root.comparison_mode = "f"
        return self.__search([self.__root], heapq.heappop, heapq.heappush)
    
    def __depth_limited_a_star_search(self, threshold: int) -> tuple[Node | None, int]:
        visited_nodes = {self.__root, }
        priority_heap = [self.__root]
        min_threshold = float('inf')

        while priority_heap:
            current_node = heapq.heappop(priority_heap)

            if current_node.estimated_cost <= threshold:
                current_node.create_children()

            for child_node in current_node.children:
                if child_node.is_final:
                    return child_node, threshold
                elif child_node not in visited_nodes:
                    if child_node.estimated_cost <= threshold:
                        visited_nodes.add(child_node)
                        heapq.heappush(priority_heap, child_node)
                    else:
                        min_threshold = min(min_threshold, child_node.estimated_cost)

        return None, min_threshold
    
    def iterative_deepening_a_star_search(self) -> Node | None:
        self.__root.comparison_mode = "f"
        threshold = self.__root.estimated_cost
        while True:
            result, threshold = self.__depth_limited_a_star_search(threshold)
            if result is not None:
                return result