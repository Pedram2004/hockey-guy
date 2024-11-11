from playground import PlayGround


class Node:
    def __init__(self, state: PlayGround, parent: "Node" = None, direction: str = "", _cost: int = 0):
        self.__parent = parent
        self.__state = state
        self.__direction = direction
        self.__cost_from_root = _cost
        self.__heuristic_value: int = 0
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
        return self.__cost_from_root + self.__heuristic_value < other.__cost_from_root + other.__heuristic_value

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
        if self.__heuristic_value == 0:
            self.__heuristic_value = self.__state.heuristic_func()
        return self.__cost_from_root + self.__heuristic_value

    @property
    def depth(self):
        return self.__depth

    def get_path(self) -> list:
        if self.__parent is None:
            return []
        return self.__parent.get_path() + [self.__direction]

    def create_children(self, _is_heuristic_based: bool, _is_cost_based : bool) -> None:
        self.__children = []
        for direction, future_state, move_s_cost in self.__state.successor_func():
            if not _is_cost_based:
                move_s_cost = 0
            cost = self.__cost_from_root + move_s_cost
            child_node = Node(state=future_state,
                                parent=self,
                                direction=direction,
                                _cost=cost)
            if _is_heuristic_based:
                child_node.__heuristic_value = child_node.__state.heuristic_func()

            self.__children.append(child_node)
