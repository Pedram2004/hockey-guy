import PlayGround


class STNode:
    def __init__(self, state : PlayGround, parent : "STNODE", direction : str):
        self.parent = parent
        self.__state = state
        self.__direction = direction
        self.__children : list[STNode] = []

    @property
    def children(self):
        return self.__children

    def create_children(self) -> None:
        for direction, future_state in self.__state.successor_func():
            self.__children.append(STNode(future_state, self, direction))

    @property
    def direction(self):
        return self.__direction


