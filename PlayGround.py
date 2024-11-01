class PlayGround:
    _cost_matrix: tuple[tuple]
    _num_rows = -1
    _num_columns = -1

    def __init__(self, player: tuple, obstacles: list[tuple], pucks: list[tuple[tuple, bool]], goals: list[tuple], obstacle_cycle: int = 0) -> None:
        """
        Initializes:\n
        __player, __obstacles, __pucks, __goals, __obstacle_cycle

        :param player: a tuple with player[0] the x-coordinate and player[1] the y-coordinate
        :param obstacles: a list of tuples that in each tuple coordinates are stored in similar to the player
        :param pucks: a list of tuples, each containing a tuple with the coordinates of the puck and a boolean value that indicates if the puck is in a goal
        :param goals: similar to obstacles
        :param obstacle_cycle: state of obstacle in a 2 by 2 square
        """

        self.__player = player
        self.__obstacles = obstacles
        self.__pucks = pucks
        self.__goals = goals
        self.__obstacle_cycle = obstacle_cycle

    def __eq__(self, other: "PlayGround") -> bool:
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

    def __str__(self) -> str:
        specifications = f"Player: {self.__player}\nPucks: {self.__pucks}\nObstacles: {self.__obstacles}"
        return specifications

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, player: tuple | list):
        self.__player = tuple(player)

    @property
    def obstacles(self):
        return self.__obstacles

    @obstacles.setter
    def obstacles(self, obstacles: tuple | list):
        self.__obstacles = tuple(obstacles)

    @property
    def pucks(self):
        return self.__pucks

    @pucks.setter
    def pucks(self, pucks: tuple | list):
        self.__pucks = tuple(pucks)

    @property
    def goals(self):
        return self.__goals

    @goals.setter
    def goals(self, goals: tuple | list):
        self.__goals = tuple(goals)

    @property
    def cost_matrix(self):
        return self._cost_matrix

    @classmethod
    def set_class_vars(cls, cost_matrix: tuple[tuple]) -> None:
        """
        Initializes:\n
        the class variables of _cost_matrix, _num_rows and _num_columns
        :param cost_matrix: a tuple of tuples with n tuples that contain m elements (n*m blocks the same size the playground), specifies the cost of each move of the player to any specific point
        """
        if cls._num_rows == -1 and cls._num_columns == -1:
            cls._cost_matrix = cost_matrix
            cls._num_rows = len(cost_matrix)
            cls._num_columns = len(cost_matrix[0])

    @classmethod
    def is_index_within_range(cls, position: list | tuple) -> bool:
        if 0 <= position[0] < cls._num_columns:
            if 0 <= position[1] < cls._num_rows:
                return True
        return False

    def is_playground_valid(self) -> bool:
        """
        Checks the collisions of player and the pucks with obstacles or themselves
        :return: the validity of the current playground state (Boolean value)
        """
        objects = [self.__player] + self.__pucks + self.__obstacles
        for ob in objects:
            if objects.count(ob) > 1:
                return False
        return True

    def successor_func(self) -> list["PlayGround"]:
        """
        Creates all possible successors of the current playground state
        :return: a list of valid future states
        """
        successor_states = []
        obstacle_cycle_direction = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        # each cycle refers to all the obstacles position relative to the 2 by 2 square they rotate counterclockwise
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # UP, DOWN, LEFT, RIGHT
        for direction in directions:
            new_player_position = list(self.player)
            for i in range(0, 2):
                new_player_position[i] += direction[i]
            if not PlayGround.is_index_within_range(new_player_position):
                continue
            new_pucks_positions = []
            for puck_position, in_goal in list(self.__pucks):
                puck_position = list(puck_position)
                if new_player_position == puck_position:
                    if in_goal:
                        new_pucks_positions.append((tuple(puck_position), in_goal))
                        continue # Puck is in goal and cannot be moved
                    for j in range(0, 2):
                        puck_position[j] += direction[j]
                    for goal_position in self.__goals:
                        if puck_position[0] == goal_position[0] and puck_position[1] == goal_position[1]:
                            in_goal = True
                    if not PlayGround.is_index_within_range(puck_position):
                        continue
                new_pucks_positions.append((tuple(puck_position), in_goal))
            new_obstacle_positions = []
            obstacle_direction = obstacle_cycle_direction.get(self.__obstacle_cycle)
            for obstacle in self.__obstacles:
                new_obstacle_positions.append((obstacle[0] + obstacle_direction[0], obstacle[1] + obstacle_direction[1]))
            possible_future_state = PlayGround(
                player=tuple(new_player_position),
                obstacles=new_obstacle_positions,
                pucks=new_pucks_positions,
                goals=self.goals,
                obstacle_cycle=(self.__obstacle_cycle + 1) % 4
            )
            if possible_future_state.is_playground_valid():
                successor_states.append(possible_future_state)
        return successor_states


# test cases here!
if __name__ == '__main__':
    PlayGround.set_class_vars([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    p1 = PlayGround((0, 0), [(1, 1), (2, 1)], [(1, 0), (2, 3)], [[3, 2]])
    p2 = PlayGround((0, 0), [(1, 1), (2, 1)], [(1, 0)], [(3, 2)])
    p3 = PlayGround((0, 1), [(0, 1), (1, 1)], [(2, 0), (0, 2)], [(3, 2)])
    playgrounds = [p1, p2]
    print(p3.is_playground_valid())
    for playground in playgrounds:
        for future in playground.successor_func():
            print(future)
            print()
        print()
