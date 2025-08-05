string = input()
move = input()  

chars = [c for c in string]

grid = [["" for _ in range(3)] for _ in range(3)]

hashrow = -1
hashcol = -1

# Fill the grid and check for '#'
index = 0
for i in range(3):
    for j in range(3):
        grid[i][j] = chars[index]
        if chars[index] == "#":
            hashrow = i
            hashcol = j
        index += 1

if move == "LEFT" and hashcol > 0:
    grid[hashrow][hashcol -1], grid[hashrow][hashcol] = grid[hashrow][hashcol], grid[hashrow][hashcol -1]

elif move == "RIGHT" and hashcol < 2:
    grid[hashrow][hashcol + 1], grid[hashrow][hashcol] = grid[hashrow][hashcol], grid[hashrow][hashcol + 1]

elif move == "UP" and hashrow > 0:
    grid[hashrow - 1 ][hashcol], grid[hashrow][hashcol] = grid[hashrow][hashcol], grid[hashrow -1 ][hashcol]

elif move == "DOWN" and hashrow < 2:
    grid[hashrow + 1][hashcol], grid[hashrow][hashcol] = grid[hashrow][hashcol], grid[hashrow + 1][hashcol]
    
# Output
output_string = ""
for i in range(3):
    for j in range(3):
        output_string += grid[i][j]

print(output_string)
