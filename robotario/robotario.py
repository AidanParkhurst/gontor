import matplotlib.pyplot as plt

robotario_length = 4 # meters
robotario_width = 6 # meters

def main():
    initial_positions = []
    with open("InitialPositions.txt", "r") as f:
        xs = f.readline().strip().split(",")
        ys = f.readline().strip().split(",")
        for x, y in zip(xs, ys):
            init_x = float(x)
            init_y = float(y)
            initial_positions.append((init_x, init_y))

    num_obstacles = input("How many obstacles do you have? (Default 0) ")
    obstacles = []
    for i in range(int(num_obstacles)):
        corners = []
        # Obstacle positions from file Obstacle_(i+1).txt
        with open(f"Obstacle_{i+1}.txt", "r") as f:
            xs = f.readline().strip().split(",")
            ys = f.readline().strip().split(",")
            for x, y in zip(xs, ys):
                corners.append((float(x), float(y)))
            obstacles.append(corners)

    # Target positions from file TargetPositions.txt
    target_positions = []
    with open("TargetPositions.txt", "r") as f:
        xs = f.readline().strip().split(",")
        ys = f.readline().strip().split(",")
        for x, y in zip(xs, ys):
            target_x = float(x)
            target_y = float(y)
            target_positions.append((float(target_x), float(target_y)))

    # Robot route from ruta.txt
    robot_route = []
    with open("ruta.txt", "r") as f:
        xs = f.readline().strip().split(",")
        ys = f.readline().strip().split(",")
        for x, y in zip(xs, ys):
            robot_x = float(x)
            robot_y = float(y)
            robot_route.append((robot_x, robot_y))
    robot_route2 = []
    with open("ruta2.txt", "r") as f:
        xs = f.readline().strip().split(",")
        ys = f.readline().strip().split(",")
        for x, y in zip(xs, ys):
            robot_x = float(x)
            robot_y = float(y)
            robot_route2.append((robot_x, robot_y))

    # Plot
    fig, ax = plt.subplots()
    ax.set_xlim(-robotario_width/2, robotario_width/2)
    ax.set_ylim(-robotario_length/2, robotario_length/2)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)

    for x, y in initial_positions:
        ax.plot(x, y, 'ro')
    for corners in obstacles:
        xs = [x for x, y in corners]
        ys = [y for x, y in corners]
        ax.fill(xs, ys, 'k')
    for x, y in target_positions:
        ax.plot(x, y, 'go')

    xs = [x for x, y in robot_route2]
    ys = [y for x, y in robot_route2]
    ax.plot(xs, ys, 'r')
    xs = [x for x, y in robot_route]
    ys = [y for x, y in robot_route]
    ax.plot(xs, ys, 'b')

    plt.show()

# def change_format():
#     with open("ruta2.txt", "r") as f:
#         xs = f.readline().strip().split(",")
#         ys = f.readline().strip().split(",")
#         with open("rutamatrix2.txt", "w") as f2:
#             for x, y in zip(xs, ys):
#                 f2.write(f"{x},{y},0\n")

if __name__ == "__main__":
    main()