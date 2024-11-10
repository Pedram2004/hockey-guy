from playground import PlayGround
from munkres import Munkres

class Node:
    def __init__(self, state: PlayGround, parent: "Node" = None, direction: str = "", cost: int = 0):
        self.__parent = parent
        self.__state = state
        self.__direction = direction
        self.__cost_from_root = cost
        self.__heuristic_value = None
        self.__children: list[Node] = []
        self.__is_final = self.__state.is_final()
        if self.__parent is not None:
            self.__depth: int = self.__parent.__depth + 1
        else:
            self.__depth: int = 0
        self.__comparison_mode = "g"

    def __eq__(self, other: "Node") -> bool:
        return self.__state == other.__state

    def __str__(self) -> str:
        return f"{self.__state}\n{self.__depth}"

    def __hash__(self) -> int:
        return hash(self.__state)

    def __lt__(self, other: "Node") -> bool:
        if not self.__heuristic_value and self.__comparison_mode == "g":
            self.__heuristic_value = self.__heuristic_function()
        match self.__comparison_mode:
            case "g":
                return self.__cost_from_root < other.__cost_from_root
            case "h":
                return self.__heuristic_value < other.__heuristic_value
            case "f":
                return self.estimated_cost < other.estimated_cost

    def __manhattan(self, a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def __heuristic_function(self) -> int:
        h = 0 # heuristic value
        m = Munkres() # Hungarian algorithm to assign pucks to goals with minimum cost
        cost_matrix = [[self.__manhattan(puck, goal) for goal in self.__state.goals] for puck, _ in self.__state.pucks]
        indexes = sorted(m.compute(cost_matrix)) # tuples of indexes of the pucks and the goals
        for row, column in indexes:
            h += cost_matrix[row][column] # cost of moving the puck to the assigned goal
        pucks = self.__state.pucks.copy()
        current = self.__state.player
        while len(pucks) > 1:
            closest_puck = min(pucks, key=lambda x: self.__manhattan(current, x[0]))
            h += self.__manhattan(current, closest_puck[0]) # cost of moving the player to the closest puck
            goal_index = indexes[self.__state.pucks.index(closest_puck)][1]
            current = self.__state.goals[goal_index] # starting from the assigned goal of the puck
            pucks.remove(closest_puck)
        else:
            h += self.__manhattan(current, pucks[0][0])
        return h

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
        try:
            return self.__cost_from_root + self.__heuristic_value
        except TypeError:
            self.__heuristic_value = self.__heuristic_function()
            return self.__cost_from_root + self.__heuristic_value

    @property
    def depth(self):
        return self.__depth
    
    @property
    def comparison_mode(self):
        return self.__comparison_mode
    
    @comparison_mode.setter
    def comparison_mode(self, mode: str):
        if mode not in ("g", "h", "f"):
            raise ValueError("Invalid comparison mode, should be one of 'g', 'h' or 'f'")
        self.__comparison_mode = mode

    def get_path(self) -> list:
        if self.__parent is None:
            return []
        return self.__parent.get_path() + [self.__direction]

    def create_children(self) -> None:
        if not self.__children:
            for direction, future_state, move_s_cost in self.__state.successor_func():
                self.__children.append(
                    Node(state=future_state,
                         parent=self,
                         direction=direction,
                         cost=self.__cost_from_root + move_s_cost)
                )