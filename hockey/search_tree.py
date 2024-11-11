from collections.abc import Iterable
from playground import PlayGround
from search_tree_node import Node
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
        player: tuple[int, int] = (0, 0)
        pucks: list[tuple[tuple[int, int], bool]] = []
        obstacles: list[tuple[int, int]] = []
        goals: list[tuple[int, int]] = []

        for i in range(num_rows):

            cost_matrix[i] = []
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

    def __search(self, priority_queue: Iterable[Node], pop_func: Callable, append_func: Callable,
                 is_heuristic_based: bool = False, is_cost_based: bool = True) -> Node | None:

        visited_nodes = {self.__root, }

        while priority_queue:
            current_node = pop_func(priority_queue)
            current_node.create_children(_is_heuristic_based=is_heuristic_based,
                                         _is_cost_based=is_cost_based)
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

    def __depth_limited_search(self, max_depth: int) -> tuple[Node | None, int]:
        if self.__root.is_final:
            return self.__root, 0

        visited_nodes = {self.__root, }
        stack = deque([self.__root])
        max_reached_depth = float("-inf")
        while stack:
            current_node = stack.pop()
            if current_node.depth < max_depth:
                current_node.create_children(_is_heuristic_based=False,
                                             _is_cost_based=True)

            for child_node in current_node.children:
                max_reached_depth = max(max_reached_depth, child_node.depth)
                if child_node.is_final:
                    return child_node, max_reached_depth
                elif child_node not in visited_nodes:
                    if child_node.depth < max_depth:
                        visited_nodes.add(child_node)
                        stack.append(child_node)

        return None, max_reached_depth

    def iterative_deepening_search(self) -> Node | None:
        maximum_depth = 0

        while True:
            result, max_reached_depth = self.__depth_limited_search(maximum_depth)

            if result is not None:
                return result
            elif max_reached_depth < maximum_depth:
                return None
            maximum_depth += 1

    def best_first_search(self) -> Node | None:
        return self.__search([self.__root], heapq.heappop, heapq.heappush, is_heuristic_based=True, is_cost_based=False)

    def a_star_search(self) -> Node | None:
        return self.__search([self.__root], heapq.heappop, heapq.heappush, is_heuristic_based=True)

    def __depth_limited_a_star_search(self, threshold: int) -> tuple[Node | None, int]:
        visited_nodes = {self.__root, }
        priority_heap = [self.__root]
        min_threshold = float('inf')

        while priority_heap:
            current_node = heapq.heappop(priority_heap)

            if current_node.estimated_cost <= threshold:
                current_node.create_children(_is_heuristic_based=True,
                                             _is_cost_based=True)

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
        threshold = self.__root.estimated_cost
        while True:
            result, threshold = self.__depth_limited_a_star_search(threshold)
            if result is not None:
                return result
