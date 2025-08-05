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

if hashrow - 1 >= 0:
    print("UP")
if hashrow + 1 < 3:
    print("DOWN")
if hashcol - 1 >= 0:
    print("LEFT")
if hashcol + 1 < 3:
    print("RIGHT")
