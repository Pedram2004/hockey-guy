# Hockey Player (Sokobon) Documentation

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
    
    - #### *Dunder Methods:*
      - `__eq__`: 
      - `__hash__`:
        
    - #### *Class Methods:*
      - `set_class_vars`: Suggesting of its name set up the class attributes of <a href="#playground">`PlayGround`</a>.
        <br> It takes a tuple of tuples to set its value for `__cost_matrix`. `__num_rows` and `__num_columns` are assigned based on the length of the given argument.
        <br> Only can be used one time to setup the class attributes.
      - `is_index_within_range`: Checks whether a given position cooredinates are positive and are within the playing ground.
        <br> Uses `__num_columns` and `__num_rows` to checks it.
        
    - `is_playground_valid`: Checks if two objects (the player, pucks and obstacles) cooredinates coincide with eachother.
    - `successor_func`: Creates other possible states that can be reached by one player's move from the available directions.
      <br> It rotates the obstacles, moves the player in an available direction and makes the player to move pucks.
      <br> It also checks if the created state ([`Playground`](#playground) object) is valid using `is_playground_valid`.
      <br> **Returns** a list of tuples which at _0_ index contain the direction of player's move, at _1_ index the new [`Playground`](#playground) instance and at _2_ index the cost of moving to a new position.
    - `__manhattan`: Calculates the Manhattan distance from two points (square) in the state's grid.
    - `heuristic_func`:
    - `is_final`: Checks if all pucks have reached a goal by checking their _1_ index.
      
- ### `Node`

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
> [!warning]
> The `children` property returns the list of children nodes directly, the consequences of object aliasing should be consider before any usage.

  - #### _Methods:_
    
    - ##### Dunder Methods:
      - `__eq__`:
      - `__hash__`:
      - `__lt__`: Comparing `__heuristic_value` plus `__cost_from_root` of nodes with eachother.
      <br> Used in comparisons made in priority queues which are present in various search algorithms (the ones using `heapq` library).
 
    - `get_path`: A recursive function which step by step adds up the taken directions to a list and returns it.
    - `create_children`: Assigns a list of all children of the current node to `__children`. 
      <br> Uses the `Playground`'s successor function (`successor_func`) to create all the valid possible states and the __direction__ to move the player that would lead to it.
      <br> Based on where it is used, it will set the cost of movements to _0_ (i.e. `best_first_search`), or will call `heuristic_func` from <a href="#playground">`Playground`</a> to assign value to       
      `__heuristic_value` of the child node (with informed searches).
      - *Parameters:*
        - `_is_heuristic_based`: Used to call the `heuristic_func` when `True` and assign some value to `__heuristic_value`.
        - `_is_cost_based`: Similar to `_is_heuristic_cost`, but will set cost of movements to _0_ when is `False` (in other words, the search is only heuristic based i.e. `best_first_search`).
    - The rest of the methods are `getter`s decorated with `@property` for almost all attributes of the class (except `__state` and `__parent`).

 - ### `STree`
   The tree structure that is used in searching the state space of the problem.
   - #### _Attributes:_
     1. `__root`: The initial state that the game starts from, represented by a <a href="#node">`Node`</a> instance.
   - #### _Methods:_
     - `input_conversion`:
     - `__search`:
     - `breadth_first_search`:
     - `depth_first_search`:
     - `uniform_cost_search`:
     - `__depth_limited_search`:
     - `iterative_deepening_search`:
     - `best_first_search`:
     - `a_star_search`:
