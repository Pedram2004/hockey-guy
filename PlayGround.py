import copy


class PlayGround:
    _cost_matrix = []
    _num_rows = -1
    _num_columns = -1

    def __init__(self, player: list, obstacles: list, pucks: list, goals: list):
        """
        Initializes:\n
        _player, _obstacles, _pucks, _goals

        :param player: player[0] the x-coordinate and player[1] the y-coordinate
        :param obstacles: a list of lists that coordinates are stored in similar to the player
        :param pucks: similar to obstacles
        :param goals: similar to obstacles
        """
        self.__player = player
        self.__obstacles = obstacles
        self.__pucks = pucks
        self.__goals = goals

    def __eq__(self, other) -> bool:
        """Checks if the state of two playground objects are the same in a search algorithm
        :return: Boolean value"""
        if isinstance(other, PlayGround):
            if self.__player != other.player:
                return False
            elif self.__obstacles != other.obstacles:
                return False
            elif self.__pucks != other.pucks:
                return False
            else:
                return True

    @property
    def player(self):
        return copy.copy(self.__player)

    @player.setter
    def player(self, player):
        self.__player = copy.copy(player)

    @property
    def obstacles(self):
        return copy.copy(self.__obstacles)

    @obstacles.setter
    def obstacles(self, obstacles):
        self.__obstacles = copy.copy(obstacles)

    @property
    def pucks(self):
        return copy.copy(self.__pucks)

    @pucks.setter
    def pucks(self, pucks):
        self.__pucks = copy.copy(pucks)

    @property
    def goals(self):
        return copy.copy(self.__goals)

    @goals.setter
    def goals(self, goals):
        self.__goals = copy.copy(goals)

    @property
    def cost_matrix(self):
        return copy.copy(self._cost_matrix)

    @classmethod
    def set_class_vars(cls, cost_matrix: list) -> None:
        """
        Initializes:\n
        the class variables of _cost_matrix, _num_rows and _num_columns
        :param cost_matrix: a list of lists with n lists that contain m elements (n*m blocks the same size the playground), specifies the cost of each move of the player to any specific point
        """
        if cls._num_rows == -1 and cls._num_columns == -1:
            cls._cost_matrix = copy.copy(cost_matrix)
            cls._num_rows = len(cost_matrix)
            cls._num_columns = len(cost_matrix[0])

    def is_playground_valid(self) -> bool:
        """
        Checks the collisions of player and the pucks with obstacles or themselves
        :return: the validity of the current playground state (Boolean value)
        """
        #may need improvements!!!
        player_and_pucks = [self.__player] + self.__pucks
        obstacles_and_pucks = self.__obstacles + self.__pucks

        for player_or_puck in player_and_pucks:
            try:
                obstacles_and_pucks.remove(player_or_puck)
            except ValueError:
                if player_or_puck != self.__player:
                    print(f"{player_or_puck} not in list {player_and_pucks} to be removed")
            for obstacle_or_puck in obstacles_and_pucks:
                if player_or_puck == obstacle_or_puck:
                    return False
            obstacles_and_pucks.append(player_or_puck)

        return True

#test case here!
if __name__ == '__main__':
    p1 = PlayGround([1, 2], [[1, 2], [2, 3]], [[3, 4]], [[4, 5]])
    print(p1.is_playground_valid())
