# Hockey Player (Sokobon) Documentation
## Classes:

- ### `STNode`:
  - Its primary usage is to hold the related information to the state of the playground and how it was reached.
    
  - #### __*Attributes:*__
    1. `__state`: It is a `PlayGround` instance
    2. `__parent`: A [`STNode`](#stnode) instance that current node's `__state` was created based of it
    3. `__direction`: A string (`str` type) made up of only one letter (`U`, `D`, `L` and `R` that represent respectively Up, Down, Left and Right).
       <br> It is made to be the `direction` property.
    5. `__children`: A `list` of future valid states of the playing ground that are resulted from the current node. <br> Their values are assigned using the `create_children`.
       <br> It is made to be the `children` property.
       
  - #### __*Methods:*__
    - `create_children`: assignes a `list` of all children of the current node to `__children`. <br> Uses the `Playground`'s successor function (`successor_func`) to create all the valid possible states and
    the __direction__ to move the player that would lead to it.
    - The two remaining methods are `getter`s for `__direction` and `__children`.
      
> [!warning]
> 
> The `children` property returns the list of children nodes directly, the consequences of object aliasing should be consider before any usage. 
