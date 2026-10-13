n = int(input())
board = [input() for _ in range(n)]

# Define the four possible adjacent directions
directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def count_adjacent_o(x, y):
    count = 0
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < n and 0 <= new_y < n and board[new_x][new_y] == 'o':
            count += 1
    return count

# Check if all cells have an even number of adjacent 'o' cells
for i in range(n):
    for j in range(n):
        if count_adjacent_o(i, j) % 2 != 0:
            print("NO")
            exit()

print("YES")