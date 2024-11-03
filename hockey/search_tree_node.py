from .playground import PlayGround


class Node:
    def __init__(self, state: PlayGround, parent: "Node", direction: str, cost: int):
        self.__parent = parent
        self.__state = state
        self.__direction = direction
        self.__cost_from_root = cost
        self.__children: list[Node] = []
        self.__is_final = self.__state.is_final()

    @property
    def children(self):
        return self.__children

    @property
    def is_final(self):
        return self.__is_final

    @property
    def direction(self):
        return self.__direction

    def create_children(self) -> None:
        for direction, future_state, move_s_cost in self.__state.successor_func():
            self.__children.append(
                Node(state=future_state,
                     parent=self,
                     direction=direction,
                     cost=self.__cost_from_root + move_s_cost)
            )
