import copy

from node import Node


class FifteensNode(Node):
    """Extends the Node class to solve the 15 puzzle.

    Parameters
    ----------
    parent : Node, optional
        The parent node. It is optional only if the input_str is provided. Default is None.

    g : int or float, optional
        The cost to reach this node from the start node : g(n).
        In this puzzle it is the number of moves to reach this node from the initial configuration.
        It is optional only if the input_str is provided. Default is 0.

    board : list of lists
        The two-dimensional list that describes the state. It is a 4x4 array of values 0, ..., 15.
        It is optional only if the input_str is provided. Default is None.

    input_str : str
        The input string to be parsed to create the board.
        The argument 'board' will be ignored, if input_str is provided.
        Example: input_str = '1 2 3 4\n5 6 7 8\n9 10 0 11\n13 14 15 12' # 0 represents the empty cell

    Examples
    ----------
    Initialization with an input string (Only the first/root construction call should be formatted like this):
    >>> n = FifteensNode(input_str=initial_state_str)
    >>> print(n)
      5  1  4  8
      7     2 11
      9  3 14 10
      6 13 15 12

    Generating a child node (All the child construction calls should be formatted like this) ::
    >>> n = FifteensNode(parent=p, g=p.g+c, board=updated_board)
    >>> print(n)
      5  1  4  8
      7  2    11
      9  3 14 10
      6 13 15 12

    """

    def __init__(self, parent=None, g=0, board=None, input_str=None):
        # NOTE: You shouldn't modify the constructor
        if input_str:
            self.board = []
            for i, line in enumerate(filter(None, input_str.splitlines())):
                self.board.append([int(n) for n in line.split()])
        else:
            self.board = board

        super(FifteensNode, self).__init__(parent, g)

    def generate_children(self):
        """Generates children by trying all 4 possible moves of the empty cell.

        Returns
        -------
            children : list of Nodes
                The list of child nodes.
        """

        # TODO: add your code here
        # You should use self.board to produce children. Don't forget to create a new board for each child
        # e.g you can use copy.deepcopy function from the standard library.

        ax = [0, 1, 0, -1]
        ay = [1, 0, -1, 0]

        def check(x, y):
            ans = ( x>= 0 and x<=3 and y>=0 and y<=3 )
            return ans

        boards = []
        for x, line in enumerate(self.board):
            for y, num in enumerate(line):
                if num == 0:
                    for i in range(len(ax)):
                        xx = x + ax[i]
                        yy = y + ay[i]
                        if check(xx, yy):
                            cur = FifteensNode(parent=self, g=self.g+1, board=copy.deepcopy(self.board))
                            temp = cur.board[x][y]
                            cur.board[x][y] = cur.board[xx][yy]
                            cur.board[xx][yy] = temp
                            boards.append(cur)
        return boards
        pass

    def is_goal(self):
        """Decides whether this search state is the final state of the puzzle.

        Returns
        -------
            is_goal : bool
                True if this search state is the goal state, False otherwise.
        """

        # TODO: add your code here
        # You should use self.board to decide.

        for x, line in enumerate(self.board):
            for y, num in enumerate(line):
                if num != (x*4+y+1)%16:
                    return False
        return True
        pass

    def evaluate_heuristic(self):
        """Heuristic function h(n) that estimates the minimum number of moves
        required to reach the goal state from this node.

        Returns
        -------
            h : int or float
                The heuristic value for this state.
        """

        # TODO: add your code here
        # You may want to use self.board here.
        dic = {}
        for i in range(1,16):
            cur = [(i-1)//4,(i-1)%4]
            dic[i]=cur
        dic[0]=[3,3]

        ans = 0

        for x, line in enumerate(self.board):
            for y, num in enumerate(line):
                cur = dic[num]
                ans += abs(x-cur[0])+abs(y-cur[1])
        ans=ans/2
        return ans
        pass

    def _get_state(self):
        """Returns an hashable representation of this search state.

        Returns
        -------
            state: tuple
                The hashable representation of the search state
        """
        # NOTE: You shouldn't modify this method.
        return tuple([n for row in self.board for n in row])

    def __str__(self):
        """Returns the string representation of this node.

        Returns
        -------
            state_str : str
                The string representation of the node.
        """
        # NOTE: You shouldn't modify this method.
        sb = []  # String builder
        for row in self.board:
            for i in row:
                sb.append(' ')
                if i == 0:
                    sb.append('  ')
                else:
                    if i < 10:
                        sb.append(' ')
                    sb.append(str(i))
            sb.append('\n')
        return ''.join(sb)


class SuperqueensNode(Node):
    """Extends the Node class to solve the Superqueens problem.

    Parameters
    ----------
    parent : Node, optional
        The parent node. Default is None.

    g : int or float, optional
        The cost to reach this node from the start node : g(n).
        In this problem it is the number of pairs of superqueens that can attack each other in this state configuration.
        Default is 1.

    queen_positions : list of pairs
        The list that stores the x and y positions of the queens in this state configuration.
        Example: [(q1_y,q1_x),(q2_y,q2_x)]. Note that the upper left corner is the origin and y increases downward
        Default is the empty list [].
        ------> x
        |
        |
        v
        y

    n : int
        The size of the board (n x n)

    Examples
    ----------
    Initialization with a board size (Only the first/root construction call should be formatted like this):
    >>> n = SuperqueensNode(n=4)
    >>> print(n)
         .  .  .  .
         .  .  .  .
         .  .  .  .
         .  .  .  .

    Generating a child node (All the child construction calls should be formatted like this):
    >>> n = SuperqueensNode(parent=p, g=p.g+c, queen_positions=updated_queen_positions, n=p.n)
    >>> print(n)
         Q  .  .  .
         .  .  .  .
         .  .  .  .
         .  .  .  .

    """

    def __init__(self, parent=None, g=0, queen_positions=[], n=1):
        # NOTE: You shouldn't modify the constructor
        self.queen_positions = queen_positions
        self.n = n
        super(SuperqueensNode, self).__init__(parent, g)

    def generate_children(self):
        """Generates children by adding a new queen.

        Returns
        -------
            children : list of Nodes
                The list of child nodes.
        """
        # TODO: add your code here
        # You should use self.queen_positions and self.n to produce children.
        # Don't forget to create a new queen_positions list for each child.
        # You can use copy.deepcopy function from the standard library.

        ax = [-2,-1,1,2,2,1,-1,-2]
        ay = [-1,-2,-2,-1,1,2,2,1]

        def check(x,y):
            return x>=0 and y>=0 and x<self.n and y<self.n

        def is_attack(lt, y, x):
            cnt = 0
            for i in range(-self.n, self.n+1):
                yy = y+i
                xx = x+i
                if check(yy, xx) and (yy, xx) in lt:
                    cnt = cnt+1
                xx = x-i
                if check(yy, xx) and (yy, xx) in lt:
                    cnt = cnt+1

            for i in range(len(ax)):
                yy = y+ay[i]
                xx = x+ax[i]
                if check(yy, xx) and (yy, xx) in lt:
                    cnt = cnt+1

            return cnt

        vs = []
        for item in self.queen_positions:
            vs.append(item[1])

        row = len(self.queen_positions)
        childs = []
        for i in range(self.n):
            y = row
            x = i
            if x in vs:
                continue
            cost = is_attack(self.queen_positions, y, x)
            cur = SuperqueensNode(parent=self, g=self.g+cost, queen_positions=copy.deepcopy(self.queen_positions), n=self.n)
            cur.queen_positions.append((y, x))
            childs.append(cur)
        return childs

    def is_goal(self):
        """Decides whether all the queens are placed on the board.

        Returns
        -------
            is_goal : bool
                True if all the queens are placed on the board, False otherwise.
        """
        # You should use self.queen_positions and self.n to decide.
        # TODO: add your code here
        return len(self.queen_positions) == self.n

    def evaluate_heuristic(self):
        """Heuristic function h(n) that estimates the minimum number of conflicts required to reach the final state.

        Returns
        -------
            h : int or float
                The heuristic value for this state.
        """
        # If you want to design a heuristic for this problem, you should use self.queen_positions and self.n.
        # TODO: add your code here (optional)
        return 0

    def _get_state(self):
        """Returns an hashable representation of this search state.

        Returns
        -------
            state: tuple
                The hashable representation of the search state
        """
        # NOTE: You shouldn't modify this method.
        return tuple(self.queen_positions)

    def __str__(self):
        """Returns the string representation of this node.

        Returns
        -------
            state_str : str
                The string representation of the node.
        """
        # NOTE: You shouldn't modify this method.
        sb = [[' . '] * self.n for i in range(self.n)]  # String builder
        for i, j in self.queen_positions:
            sb[i][j] = ' Q '
        return '\n'.join([''.join(row) for row in sb])
