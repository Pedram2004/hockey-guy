from playground import PlayGround


class Node:
    def __init__(self, state: PlayGround, parent: "Node" = None, direction: str = "", cost: int = 0):
        self.__parent = parent
        self.__state = state
        self.__direction = direction
        self.__cost_from_root = cost
        self.__children: list[Node] = []
        self.__is_final = self.__state.is_final()
        if self.__parent is not None:
            self.__depth: int = self.__parent.__depth + 1
        else:
            self.__depth: int = 0

    def __eq__(self, other: "Node") -> bool:
        return self.__state == other.__state

    def __str__(self) -> str:
        return str(self.__state)

    def __hash__(self) -> int:
        return hash(self.__state)

    def __lt__(self, other: "Node") -> bool:
        return self.__cost_from_root < other.cost_from_root

    def __le__(self, other: "Node") -> bool:
        return self.__cost_from_root <= other.cost_from_root

    def __gt__(self, other: "Node") -> bool:
        return self.__cost_from_root > other.cost_from_root

    def __ge__(self, other: "Node") -> bool:
        return self.__cost_from_root >= other.cost_from_root

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

    def get_full_direction(self) -> str:
        if self.__parent is None:
            return self.__direction
        return self.__parent.get_full_direction() + self.__direction

    def create_children(self) -> None:
        for direction, future_state, move_s_cost in self.__state.successor_func():
            self.__children.append(
                Node(state=future_state,
                     parent=self,
                     direction=direction,
                     cost=self.__cost_from_root + move_s_cost)
            )
