"""Implementation of the A* algorithm.

This file contains a skeleton implementation of the A* algorithm. It is a single
method that accepts the root node and runs the A* algorithm
using that node's methods to generate children, evaluate heuristics, etc.
This way, plugging in root nodes of different types, we can run this A* to
solve different problems.

"""
import heapq
from node import Node


def Astar(root):
    """Runs the A* algorithm given the root node. The class of the root node
    defines the problem that's being solved. The algorithm either returns the solution
    as a path from the start node to the goal node or returns None if there's no solution.

    Parameters
    ----------
    root: Node
        The start node of the problem to be solved.

    Returns
    -------
        path: list of Nodes or None
            The solution, a path from the initial node to the goal node.
            If there is no solution it should return None
    """

    # TODO: add your code here
    # Some helper pseudo-code:
    # 1. Create an empty fringe and add your root node (you can use lists, sets, heaps, ... )
    # 2. While the container is not empty:
    # 3.      Pop the best? node (Use the attribute `node.f` in comparison)
    # 4.      If that's a goal node, return node.get_path()
    # 5.      Otherwise, add the children of the node to the fringe
    # 6. Return None
    #
    # Some notes:
    # You can access the state of a node by `node.state`. (You may also want to store evaluated states)
    # You should consider the states evaluated and the ones in the fringe to avoid repeated calculation in 5. above.
    # You can compare two node states by node1.state == node2.state

    que = []
    vs = []
    heapq.heapify(que)
    heapq.heappush(que, (0+root.evaluate_heuristic(), root.g,  0, root))
    vs.append(root._get_state())
    ans_node = None
    ans_cost = -1
    while len(que) > 0:
        f, c, id, cur_node = heapq.heappop(que)
        childs = cur_node.generate_children()
        for child in childs:
            if child._get_state() in vs:
                continue
            if ans_cost != -1 and child.g >= ans_cost:
                continue
            if child.is_goal() == True:
                if ans_cost==-1:
                    ans_cost = child.g
                    ans_node = child
                elif ans_cost > child.g:
                    ans_cost = child.g
                    ans_node = child
                continue
            heapq.heappush(que, (child.g+child.evaluate_heuristic(),child.g,  len(vs), child))
            vs.append(child._get_state())
    if ans_cost == -1:
        return []
    ans = []
    ans.append(ans_node)
    while ans_node._get_state() != root._get_state():
        ans_node=ans_node.parent
        ans.append(ans_node)
    res = []
    for node in reversed(ans):
        res.append(node)
    return res
