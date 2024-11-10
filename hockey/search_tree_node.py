from playground import PlayGround
from munkres import Munkres

class Node:
    def __init__(self, state: PlayGround, parent: "Node" = None, direction: str = "", cost: int = 0):
        self.__parent = parent
        self.__state = state
        self.__direction = direction
        self.__cost_from_root = cost
        self.__heuristic_value = 0
        self.__children: list[Node] = []
        self.__is_final = self.__state.is_final()
        if self.__parent is not None:
            self.__depth: int = self.__parent.__depth + 1
        else:
            self.__depth: int = 0

    def __eq__(self, other: "Node") -> bool:
        return self.__state == other.__state

    def __str__(self) -> str:
        return f"{self.__state}\n{self.__depth}"

    def __hash__(self) -> int:
        return hash(self.__state)

    def __lt__(self, other: "Node") -> bool:
        return self.estimated_cost < other.estimated_cost

    @property
    def children(self):
        return self.__children

    @property
    def is_final(self):
        return self.__is_final

    @property
    def direction(self):
        return self.__direction

    @property
    def cost_from_root(self):
        return self.__cost_from_root
    
    @property
    def estimated_cost(self):
        return self.__cost_from_root + self.__heuristic_value

    @property
    def depth(self):
        return self.__depth

    def get_path(self) -> list:
        if self.__parent is None:
            return []
        return self.__parent.get_path() + [self.__direction]

    def create_children(self) -> None:
        for direction, future_state, move_s_cost in self.__state.successor_func():
            self.__children.append(
                Node(state=future_state,
                     parent=self,
                     direction=direction,
                     cost=self.__cost_from_root + move_s_cost)
            )
        if not self.__children:
            for direction, future_state, move_s_cost in self.__state.successor_func():
                self.__children.append(
                    Node(state=future_state,
                         parent=self,
                         direction=direction,
                         cost=self.__cost_from_root + move_s_cost)
                )


    def __manhattan(self, a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def heuristic_function(self, set_to_zero: bool = False) -> int:
        if set_to_zero:
            self.__heuristic_value = 0
            return 0
        
        h = 0 # heuristic value

        m = Munkres()
        cost_matrix = [[self.__manhattan(puck, goal) for goal in self.__state.goals] for puck in self.__state.pucks]
        indexes = sorted(m.compute(cost_matrix))

        for row, column in indexes:
            h += cost_matrix[row][column]
        
        pucks = self.__state.pucks.copy()
        current = self.__state.player
        while len(pucks) > 1:
            closest_puck = min(pucks, key=lambda x: self.__manhattan(current, x[0]))
            h += self.__manhattan(current, closest_puck[0])
            current = self.__state.goals[indexes[self.__state.pucks.index(closest_puck)][1]] # goal of the puck
            pucks.remove(closest_puck)
        else:
            h += self.__manhattan(current, pucks[0][0])
        
        self.__heuristic_value = h
        return h