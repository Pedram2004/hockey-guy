from .playground import PlayGround

class Node:
    def __init__(self, state: PlayGround, parent: "Node", direction: str):
        self.__parent = parent
        self.__state = state
        self.__direction = direction
        self.__children : list[Node] = []

    @property
    def children(self):
        return self.__children

    def create_children(self) -> None:
        for direction, future_state in self.__state.successor_func():
            self.__children.append(Node(future_state, self, direction))

    @property
    def direction(self):
        return self.__direction


