from playground import PlayGround


class Node:
    def __init__(self, state: PlayGround, parent: "Node", direction: str, cost: int):
        self.__parent = parent
        self.__state = state
        self.__direction = direction
        self.__cost_from_root = cost
        self.__children: list[Node] = []

    @property
    def children(self):
        return self.__children

    def create_children(self) -> None:
        for direction, future_state, move_s_cost in self.__state.successor_func():
            self.__children.append(
                Node(state=future_state,
                     parent=self,
                     direction=direction,
                     cost=self.__cost_from_root + move_s_cost)
            )

    @property
    def direction(self):
        return self.__direction
