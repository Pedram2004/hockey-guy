# Hockey Player (Sokobon) Documentation

  Utilizing different informed and uninformed searches to find a path taken by the player which can result in an end state.

## Game Description

  On a rectangular grid, which includes obstacles, pucks and goals (the number of pucks and goals are the same). It is the player's aim to put all pucks in goals such that no more than __one__ puck is assigned the same goal.

- ### _Rules:_

  - __Player__ and the __pucks__ must not collide with obstacles (This state is considered invalid).
  - To move a __puck__ towards a particular direction, the __player__ must be on the opposite side of the puck and move towards the intended direction.
  - __Obstacles__ do counter clockwise rotation within a _2_ by _2_ square starting from the top right corner of said square.
      <br> The __obstacles__ rotate based on the given pattern one move at each movement of the player's.
  - Once a __puck__ has reached an available __goal__, the puck act as an immovable object which can not be crossed.

- ## How to Run

  Go to the project folder and run

  ```
  python -m main
  ```

  in the terminal

<h2>External Libraries</h2>
  The list of libraries whcih were imported in this program.
  
- <h3>Standard Libraries</h3>
  
  - `heapq`: It is used as a priority queue to select a [node](#node) with the minimum of cost in [`STree`](#stree).
  - `deque`: The usage is for the stack and queue structure required by `breadth_first_search` and `depth_first_search` in [`STree`](#stree) because of the additional functionality as comapred to a `list`.

    `typing` is imported only to add extra clarification to the type of some functions arguments.
- `munkres`: An external library to solve the delivery problem encoutnering when calculating the minimum moves to assign __pucks__ to a respective __goal__.
    <br> It is used in `heuristic_func` for the calculations.
    <br> To install it, run ```pip install munkres```.

## Requirements

- `munkres`: Implementation of the Hungarian Algorithm.
        <br> To install it, run ```pip install munkres```.

## Classes

- <h3 id="playground"><code>PlayGround</code></h3>
  Encapsulation of the playing ground with all its elements including the player, pucks,   obstacles, goals and the cost of movement.

  - #### _Attributes:_

    - #### _Instance Attributes:_

      - The $x$ and $y$ cooredinates in all attributes is similar to that of $R^{2}$ with the major difference that it is a reflection of the plane along the $x$ axis.
        <br/><br/>
      1. `__player`: A tuple containing the position of the player
      2. `__pucks`: A list of tuples which themselves contain in their _0_ index a tuple with a puck's position and at _1_ index a boolean indicating if the puck has reached a goal.
      3. `__obstacles`: A list of tuples which have position of each obstacle.
      4. `__goals`: Structurely identical to `__obstacles`.
      5. `__obstacle_cycle`: an integer from _0_ to _3_ indicating where the obstacles should move.

    - #### _Class Attributes:_

      1. `__num_rows`: The number of rows in the playing ground. Initilized at first to _-1_.
      2. `__num_columns`: Similar to `__num_rows` but for the columns.
      3. `__cost_matrix`: A tuple of tuples that represent the cost to move to each square from its neighbours by taking its index (e.g. for the cost it takes to move to (0, 3), `__cost_matrix[0][3]` can be used). Its size is the same as the playing ground

  - #### _Methods:_

    - #### _Dunder Methods:_

      - `__eq__`: Checks if position of the player, obstacles, and pucks are the same
      - `__hash__`: hashes the position of the player, obstacles, and pucks

    - #### _Class Methods:_

      - `set_class_vars`: Suggesting of its name set up the class attributes of <a href="#playground">`PlayGround`</a>.
        <br> It takes a tuple of tuples to set its value for `__cost_matrix`. `__num_rows` and `__num_columns` are assigned based on the length of the given argument.
        <br> Only can be used one time to setup the class attributes.
      - `is_index_within_range`: Checks whether a given position cooredinates are positive and are within the playing ground.
        <br> Uses `__num_columns` and `__num_rows` to checks it.

    - `is_playground_valid`: Checks if two objects (the player, pucks and obstacles) cooredinates coincide with eachother.
    - `successor_func`: Creates other possible states that can be reached by one player's move from the available directions.
      <br> It rotates the obstacles, moves the player in an available direction and makes the player to move pucks.
      <br> It also checks if the created state ([`Playground`](#playground) object) is valid using `is_playground_valid`.
      <br> __Returns__ a list of tuples which at _0_ index contain the direction of player's move, at _1_ index the new [`Playground`](#playground) instance and at _2_ index the cost of moving to a new position.
    - `__manhattan`: Calculates the Manhattan distance from two points (square) in the state's grid.
    - `heuristic_func`: Assignes a goal to each puck based on Hungarian Algorithm, then calculates the Manhattan distance of player to the nearest puck, puck to its assigned goal, assigned goal to the nearest puck and so on.
    - `is_final`: Checks if all pucks have reached a goal by checking their _1_ index.

- <h3 id="node"><code>Node</code></h3>

  - Holds the related information to the state of the playground and how it was reached.
    <br> It is primarily used in [`STree`](#stree) to connects each state to others.

  - #### _Attributes:_

    1. `__state`: It is a [`PlayGround`](#playground) instance
    2. `__parent`: A [`Node`](#node) instance that current node's `__state` was created based of it
    3. `__direction`: A string (`str` type) made up of only one letter (`U`, `D`, `L` and `R` that represent respectively Up, Down, Left and Right).
       <br> For usage outside of the class, it is made to be the `direction` property.
    4. `__cost_from_root`: The cumulative cost of movements which the player has made to reach the current node's `__state`.
    5. `__heuristic_value`: The estimated cost to reach a goal from the current state. It is estimated by `heuristic_func` in <a href="#playground">`PlayGround`</a>.
    6. `__children`: A list of future valid states of the playing ground that are resulted from the current node.
       <br> Their values are assigned using the `create_children`.
       <br> For usage outside of the class, it is made to be the `children` property.
    8. `__is_final`: Checks if in its `__state` all pucks have reached some goals.
       <br> It is done by `is_final` function from [`Playground`](#playground).
       <br> For usage outside of the class, it is made to be the `is_final` property.
    9. `__depth`: The depth in the [search tree](#stree) in which the node has been reached (found). It is its `__parent`'s depth plus _1_.
       <br> For usage outside of the class, it is made to be the `depth` property.
    10. `__comparison_mode`: Can be g, h, or f. Used for differentiating between UCS, BestFS, and A*.

  - #### _Methods:_

    - ##### Dunder Methods

      - `__eq__`: Returns the value of `__eq__` from [`Playground`](#playground).
      - `__hash__`: Returns the value of `__hash__` from [`Playground`](#playground).
      - `__lt__`: Comparing `__heuristic_value` plus `__cost_from_root` of nodes with eachother.
      <br> Used in comparisons made in priority queues which are present in various search algorithms (the ones using `heapq` library).

    - `get_path`: A recursive function which step by step adds up the taken directions to a list and returns it.
    - `create_children`: Assigns a list of all children of the current node to `__children`.
      <br> Uses the `Playground`'s successor function (`successor_func`) to create all the valid possible states and the __direction__ to move the player that would lead to it.
      <br> Based on where it is used, it will set the cost of movements to _0_ (i.e. `best_first_search`), or will call `heuristic_func` from <a href="#playground">`Playground`</a> to assign value to
      `__heuristic_value` of the child node (with informed searches).
    - The rest of the methods are `getter`s decorated with `@property` for almost all attributes of the class (except `__state` and `__parent`).

> [!warning]
> The `children` property returns the list of children nodes directly, the consequences of object aliasing should be consider before any usage.

- ### `STree`

   The tree structure that is used in searching the state space of the problem.

  - #### _Attributes:_

     1. `__root`: The initial state that the game starts from, represented by a <a href="#node">`Node`</a> instance.

  - #### _Methods:_

    - `input_conversion`: Parses the input, setting up the initial state of the game by capturing the grid size, obstacles, player, pucks, goals, and costs, then creates and returns an `STree` object with this initial setup.

    - `__search`: A generic search function that operates based on the provided data structure (`deque` for BFS and DFS or a heap-based priority queue for informed searches). This method takes a priority queue (or stack/queue) along with specific append and pop functions for node expansion. It returns the final goal node if found, or `None` if no solution exists.

    - `breadth_first_search`: Implements the Breadth-First Search algorithm to explore the shortest path (in terms of moves, not cost) by expanding nodes level by level until the goal state is found. Uses a `deque` with a queue structure.

    - `depth_first_search`: Implements Depth-First Search, expanding nodes in a last-in, first-out manner. This method uses a `deque` as a stack to explore deeper states first, with no guarantee of finding the shortest path.

    - `uniform_cost_search`: Implements Uniform Cost Search to find the least-cost path to the goal by expanding the node with the lowest path cost at each step. It uses a priority queue (heap) to prioritize nodes with the minimum `g` cost (cost from the root).

    - `__depth_limited_search`: A helper method for Depth-Limited Search, which expands nodes up to a given `max_depth`. It returns a tuple containing either the goal node (if found) or `None` and a boolean indicating if deeper nodes are present for Iterative Deepening purposes.

    - `iterative_deepening_search`: Uses iterative depth limits to search progressively deeper layers of the tree until the goal state is found. This combines the benefits of DFS’s low memory usage and BFS’s completeness in an unbounded search space.

    - `best_first_search`: Executes Best-First Search to find the goal state based on a heuristic, expanding the node estimated to be closest to the goal according to `h` (heuristic cost). A priority queue (heap) is used to manage node selection.

    - `a_star_search`: A search strategy combining UCS and Best-First Search, guided by `f = g + h` (actual cost + heuristic). This ensures it finds an optimal solution when the heuristic is admissible. Uses a priority queue (heap) to expand nodes based on the `f` cost.

    - `__depth_limited_a_star_search`: A helper for Iterative Deepening A*(IDA*) search. It explores nodes within a cost threshold, expanding nodes below or equal to the current threshold and tracking the minimum threshold exceeded by unexplored nodes. Returns a tuple of the goal node (if found) and the next threshold for IDA*.

    - `iterative_deepening_a_star_search`: An adaptation of A* that repeatedly increases the cost threshold to progressively explore nodes closer to the goal. Uses `__depth_limited_a_star_search` for node expansion based on cost thresholds until an optimal solution is found.
