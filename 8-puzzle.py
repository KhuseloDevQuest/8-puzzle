class Node:
    def __init__(self, value):
        self.value = value
        self._next = None
        self._prev = None

class DoublyLinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._N = 0
     
    def add_first(self, value):
        new_node = Node(value)
        if not self._head:
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
            self._head = new_node
            self._tail = new_node
        else:
            new_node._prev = self._tail
            self._tail._next = new_node
            self._tail = new_node
        self._N += 1
     
    def remove_first(self):
        ret = None
        if self._head:
            ret = self._head.value
            if self._head is self._tail:
                self._head = None
                self._tail = None
            else:
                self._head = self._head._next
                self._head._prev = None
            self._N -= 1
        return ret

    def __len__(self):
        return self._N

class State:
    def __init__(self, tiles):
        self.tiles = tiles
        self.prev = None
    
    def __repr__(self):
        s = ""
        for row in self.tiles:
            for val in row:
                s += "{} ".format(val)
            s += "\n"
        return s
    
    def __eq__(self, other):
        return self.tiles == other.tiles
    
    def __hash__(self):
        return hash(tuple([tuple(row) for row in self.tiles]))

    def __lt__(self, other):
        return str(self) < str(other)
    
    def copy(self):
        return State([row[:] for row in self.tiles])
    
    def get_neighbs(self):
        N = len(self.tiles)
        neighbs = []
        row, col = -1, -1
        
        for i in range(N):
            for j in range(N):
                if self.tiles[i][j] == " ":
                    row, col = i, j
                    break
        
        for (i, j) in [(row-1,col), (row+1,col), (row,col-1), (row,col+1)]:
            if 0 <= i < N and 0 <= j < N:
                n = self.copy()
                n.tiles[row][col], n.tiles[i][j] = n.tiles[i][j], n.tiles[row][col]
                neighbs.append(n)
        return neighbs

    def solve(self, goal_state=None):
        frontier = DoublyLinkedList()
        frontier.add_last(self)
        visited = set()
        on_frontier = set([self])
        v = None

        while len(frontier) > 0:
            v = frontier.remove_first()
            visited.add(v)
            on_frontier.remove(v)
            if goal_state is not None and v.tiles == goal_state.tiles:
                break
            elif goal_state is None and v.is_goal():
                break
            for n in v.get_neighbs():
                if n not in visited and n not in on_frontier:
                    on_frontier.add(n)
                    n.prev = v
                    frontier.add_last(n)

        if v is None or (goal_state and v.tiles != goal_state.tiles):
            return []

        solution = [v]
        while v.prev:
            v = v.prev
            solution.append(v)
        solution.reverse()
        return solution

    def is_goal(self):
        N = len(self.tiles)
        counter = 1
        for i in range(N):
            for j in range(N):
                if i == N-1 and j == N-1:
                    if self.tiles[i][j] != " ":
                        return False
                else:
                    if self.tiles[i][j] != counter:
                        return False
                    counter += 1
        return True

def parse_input(string):
    chars = list(string)
    grid = [["" for _ in range(3)] for _ in range(3)]
    index = 0
    for i in range(3):
        for j in range(3):
            grid[i][j] = " " if chars[index] == "#" else chars[index]
            index += 1
    return [[int(cell) if cell.isdigit() else cell for cell in row] for row in grid]

def is_solvable(tiles):
    flat = [x for row in tiles for x in row if x != " "]
    inv_count = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inv_count += 1
    return inv_count % 2 == 0

# === MAIN CODE ===
string = input().strip()
destination = input().strip()

converted_grid = parse_input(string)
converted_grid2 = parse_input(destination)

if not is_solvable(converted_grid):
    print("Unsolvable puzzle.")
else:
    state1 = State(converted_grid)
    goal_state = State(converted_grid2)
    solution = state1.solve(goal_state)

    if not solution:
        print("No solution found.")
    else:
        #for step in solution:
            #print(step)
        print( len(solution) - 1)
