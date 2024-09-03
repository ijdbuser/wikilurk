import json
import time


graph: dict = json.load(open('data.json', 'r'))

def floyd_warshall(graph:dict):
    n = len(graph)
    mem: list[list[float | None]] = []
    pathsL: list[list[list[any]]] = []

    graph_list = list(graph.items())

    for x in range(0, n):
        mem.append([None for i in range(n)])
        x_name, x_vert = graph_list[x]
        for y in range(0, n):
            y_name, y_vert = graph_list[y]
            if x_name == y_name:
                mem[x][y] = 0
            elif y_name in graph[x_name]['links']:
                mem[x][y] = 1
            else:
                mem[x][y] = float("inf")



    for x in range(0, n):
        pathsL.append([[] for _ in range(n)])
        for y in range(0, n):
            if mem[x][y] > 0 and mem[x][y] != float('inf'):
                pathsL[x][y].append("{} -> {}".format(graph_list[x][1]['title'], graph_list[y][1]['title']))

    start = time.time()

    for k in range(0, n):
        print(k, n)
        for x in range(0, n):
            for y in range(0, n):
                if mem[x][y] > mem[x][k] + mem[k][y]:
                    pathsL[x][y] = pathsL[x][k] + pathsL[k][y]

                mem[x][y] = min(mem[x][y], mem[x][k] + mem[k][y])

    end = time.time()

    print(f"Execution time: {start - end}")

    return mem, pathsL


mem, paths = floyd_warshall(graph)

with open("wtf.txt", "w") as output:
    json.dump(paths, output, indent=4)

