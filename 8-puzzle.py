class Node:
    def __init__(self, value):
        self.value = value
        self._next = None # Python's version of "null" is "None"
        self._prev = None

class DoublyLinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._N = 0
     
    def add_first(self, value):
        """
        Parameters
        ----------
        value: any
            Add a new node to the beginning with this value
        """
        new_node = Node(value)
        if not self._head:
            # If there's nothing there yet, this
            # new element is both the head and the tail
            self._head = new_node
            self._tail = new_node
        else:
            new_node._next = self._head
            self._head._prev = new_node
            self._head = new_node
        self._N += 1
     
    def add_last(self, value):
        new_node = Node(value)
        if not self._tail:
            # If there's nothing there yet, this
            # new element is both the head and the tail
            self._head = new_node
            self._tail = new_node
        else:
            new_node._prev = self._tail
            self._tail._next = new_node
            self._tail = new_node
        self._N += 1
     
    def remove_first(self):
        """
        Remove and return the first value from the linked list
        or do nothing and return None if it's already empty
        """
        ret = None
        if self._head: # If the head is not None
            ret = self._head.value
            if self._head is self._tail:
                self._head = None
                self._tail = None
            else:
                self._head = self._head._next
                self._head._prev = None
            self._N -= 1
        return ret

    def remove_last(self):
        """
        Remove and return the last value from the linked list
        or do nothing and return None if it's already empty
        """
        ret = None
        if self._tail: # If the head is not None
            ret = self._tail.value
            if self._head is self._tail:
                self._head = None
                self._tail = None
            else:
                self._tail = self._tail._prev
                self._tail._next = None
            self._N -= 1
        return ret
         
    def __str__(self):
        # This is like the to-string method
        s = "DoublyLinkedList: "
        node = self._head
        while node: #As long as the node is not None
            s += "{} ==> ".format(node.value)
            node = node._next
        return s
     
    def __len__(self):
        # This allows us to use len() on our object to get its length!
        return self._N

class State:
    def __init__(self, tiles):
        """
        Parameters
        ----------
        tiles: 2d list
            A list of list of tiles.  All are numbers except for
            the blank, which is a " "
            Ex) [[2, 6, 1], [7, " ", 3], [5, 8, 4]]
        """
        self.tiles = tiles
        self.prev = None
    
    def __repr__(self):
        """
        Returns
        -------
        A printable string representation of the board
        """
        s = ""
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                s += "{} ".format(self.tiles[i][j])
            s += "\n"
        return s
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __hash__(self):
        return hash(tuple([tuple(x) for x in self.tiles]))

    def __lt__(self, other):
        """
        Overload the less than operator so that ties can
        be broken automatically in a heap without crashing
        Parameters
        ----------
        other: State
            Another state
        
        Returns
        -------
        Result of < on string comparison of __str__ from self
        and other
        """
        return str(self) < str(other)
    
    def copy(self):
        """
        Return a deep copy of this state
        """
        tiles = []
        for i in range(len(self.tiles)):
            tiles.append([])
            for j in range(len(self.tiles[i])):
                tiles[i].append(self.tiles[i][j])
        return State(tiles)
    
    def is_goal(self):
        """
        Returns
        -------
        True if this is a goal state, False otherwise
        """
        res = True
        N = len(self.tiles)
        counter = 1
        for i in range(N):
            for j in range(N):
                if i != N-1 or j != N-1:
                    if self.tiles[i][j] != counter:
                        res = False
                counter += 1
        return res

    def get_neighbs(self):
        """
        Get the neighboring states

        Returns
        -------
        list of State
            A list of the neighboring states
        """
        N = len(self.tiles)
        neighbs = []
        
        ## Step 1: Find the row and col of the blank
        row = 0
        col = 0
        for i in range(N):
            for j in range(N):
                if self.tiles[i][j] == " ":
                    row = i
                    col = j
        
        ## Step 2: Swap this index with every neighbor
        ## that it can be swapped with
        for [i, j] in [[row-1, col], [row+1, col], [row, col-1], [row, col+1]]:
            if i >= 0 and j >= 0 and i < N and j < N:
                n = self.copy()
                ## Swap (row, col) with (i, j)
                n.tiles[row][col], n.tiles[i][j] = n.tiles[i][j], n.tiles[row][col]
                neighbs.append(n)
        return neighbs
    
    def solve(self):
        """
        Find a shortest path from this state to a goal state

        Returns
        -------
        list of State
            A path from this state to a goal state, where the first 
            element is this state and the last element is the goal
        """
        finished = False
        
        frontier = DoublyLinkedList()
        frontier.add_last(self)

        on_frontier = set([self])
        visited = set([])

        # Each vertex passes through the frontier exactly once
        v = None
        while not finished and len(frontier) > 0: # O(V) iterations
            v = frontier.remove_first() #O(1)
            visited.add(v) # O(1)
            on_frontier.remove(v)
            if v.is_goal():
                finished = True
            else:
                # Look at each neighbor of v
                for n in v.get_neighbs(): # 2E, or O(E) iterations over all
                    # iterations of the outer loop
                    # As many iterations as neighbors of v
                    # Put a neighbor on the frontier
                    # if it hasn't been visited yet
                    if n not in on_frontier and n not in visited:
                        # Switch to being on frontier, and add
                        # to the back of the frontier
                        on_frontier.add(n) # O(1)
                        n.prev = v
                        frontier.add_last(n) # O(1)
        # TODO: Fill this in
        solution = [v]
        while v.prev:
            v = v.prev
            solution.append(v)
        solution.reverse()
        return solution

state = State([[5, 6, 8], [" ", 4, 7], [1, 3, 2]])
solution = state.solve()

for x in solution:
    print(x, end="\n\n")

print(len(solution))