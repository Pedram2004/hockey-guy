from playground import PlayGround


class Node:
    def __init__(self, state: PlayGround, parent: "Node" = None, direction: str = "", cost: int = 0):
        self.__parent = parent
        self.__state = state
        self.__direction = direction
        self.__cost_from_root = cost
        self.__children: list[Node] = []
        self.__is_final = self.__state.is_final()

    def __eq__(self, other: "Node") -> bool:
        return self.__state == other.__state

    def __str__(self) -> str:
        return str(self.__state)
    
    def __hash__(self) -> int:
        return hash(self.__state)

    @property
    def children(self):
        return self.__children

    @property
    def is_final(self):
        return self.__is_final

    @property
    def direction(self):
        return self.__direction
    
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
