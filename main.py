from hockey.search_tree import STree

if __name__ == "__main__":
    search_tree = STree.input_conversion()

    res = search_tree.breadth_first_search()
    print("------Breadth First Search------")
    print("Path: ", res.get_path())
    print("Cost: ", res.cost_from_root)
    print("Depth: ", res.depth)

    res = search_tree.uniform_cost_search()
    print("------Uniform Cost Search------")
    print("Path: ", res.get_path())
    print("Cost: ", res.cost_from_root)
    print("Depth: ", res.depth)

    res = search_tree.depth_first_search()
    print("------Depth First Search------")
    print("Path: ", res.get_path())
    print("Cost: ", res.cost_from_root)
    print("Depth: ", res.depth)

    res = search_tree.iterative_deepening_search() 
    print("------Iterative Deepening Search------")
    print("Path: ", res.get_path())
    print("Cost: ", res.cost_from_root)
    print("Depth: ", res.depth)

    res = search_tree.best_first_search()
    print("------Best First Search------")
    print("Path: ", res.get_path())
    print("Cost: ", res.cost_from_root)
    print("Depth: ", res.depth)

    res = search_tree.a_star_search()
    print("------A* Search------")
    print("Path: ", res.get_path())
    print("Cost: ", res.cost_from_root)
    print("Depth: ", res.depth)

    res = search_tree.iterative_deepening_a_star_search()
    print("------Iterative Deepening A* Search------")
    print("Path: ", res.get_path())
    print("Cost: ", res.cost_from_root)
    print("Depth: ", res.depth)