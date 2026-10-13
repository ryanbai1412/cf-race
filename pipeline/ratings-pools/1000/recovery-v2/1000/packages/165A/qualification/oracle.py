no_of_points = int(input())
points_coordinate_list = list( list(map(int, input().split()[:2])) for _ in range(no_of_points) )

# Initializing counters for each type of neighbors
left, right, lower, upper = [False]*no_of_points, [False]*no_of_points, [False]*no_of_points, [False]*no_of_points

for i in range(no_of_points):
    x, y = points_coordinate_list[i]
    for j in range(no_of_points):
        if points_coordinate_list[j][0] < x and points_coordinate_list[j][1] == y:
            left[i] = True
        elif points_coordinate_list[j][0] > x and points_coordinate_list[j][1] == y:
            right[i] = True
        elif points_coordinate_list[j][0] == x and points_coordinate_list[j][1] < y:
            lower[i] = True
        elif points_coordinate_list[j][0] == x and points_coordinate_list[j][1] > y:
            upper[i] = True

supercentral_count = 0
for i in range(no_of_points):
    if left[i] and right[i] and lower[i] and upper[i]:
        supercentral_count += 1

print(supercentral_count)