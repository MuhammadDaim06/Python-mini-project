import heapq
import math

COORDS = {
    "Downtown":   (0, 0),
    "Airport":    (8, 2),
    "Mall":       (3, 4),
    "Hospital":   (-2, 3),
    "University": (-4, -1),
    "Stadium":    (5, -3),
    "TechPark":   (6, 5),
    "OldTown":    (-1, -4),
    "Suburb_A":   (-6, 4),
    "Suburb_B":   (9, -2),
}

GRAPH = {
    "Downtown":   {"Mall": 5, "Hospital": 4, "OldTown": 4, "Stadium": 6},
    "Mall":       {"Downtown": 5, "TechPark": 4, "Hospital": 5},
    "Hospital":   {"Downtown": 4, "Mall": 5, "Suburb_A": 5, "University": 5},
    "University": {"Hospital": 5, "OldTown": 4, "Suburb_A": 6},
    "Stadium":    {"Downtown": 6, "Airport": 6, "Suburb_B": 6},
    "TechPark":   {"Mall": 4, "Airport": 5},
    "OldTown":    {"Downtown": 4, "University": 4, "Suburb_B": 8},
    "Suburb_A":   {"Hospital": 5, "University": 6},
    "Suburb_B":   {"Stadium": 6, "OldTown": 8, "Airport": 5},
    "Airport":    {"Stadium": 6, "TechPark": 5, "Suburb_B": 5},
}


def heuristic(node, goal):
    x1, y1 = COORDS[node]
    x2, y2 = COORDS[goal]
    return round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2), 2)


def path_cost(path):
    total = 0
    for i in range(len(path) - 1):
        total += GRAPH[path[i]][path[i + 1]]
    return total


def bfs(start, goal):
    queue = [[start]]
    visited = {start}
    explored = 0
    while queue:
        path = queue.pop(0)
        node = path[-1]
        explored += 1
        if node == goal:
            return path, explored
        for neighbor in GRAPH[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None, explored


def dfs(start, goal, path=None, visited=None):
    if path is None:
        path, visited = [start], {start}
    if start == goal:
        return path, len(visited)
    for neighbor in GRAPH[start]:
        if neighbor not in visited:
            visited.add(neighbor)
            result, _ = dfs(neighbor, goal, path + [neighbor], visited)
            if result:
                return result, len(visited)
    return None, len(visited)


def ucs(start, goal):
    pq = [(0, start, [start])]
    visited = set()
    explored = 0
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        explored += 1
        if node == goal:
            return path, cost, explored
        for neighbor, weight in GRAPH[node].items():
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))
    return None, float("inf"), explored


def a_star(start, goal):
    open_list = [(heuristic(start, goal), 0, start, [start])]
    visited = set()
    explored = 0
    while open_list:
        f, g, node, path = heapq.heappop(open_list)
        if node in visited:
            continue
        visited.add(node)
        explored += 1
        if node == goal:
            return path, g, explored
        for neighbor, weight in GRAPH[node].items():
            if neighbor not in visited:
                g_new = g + weight
                f_new = g_new + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_new, g_new, neighbor, path + [neighbor]))
    return None, float("inf"), explored


def ask_for_node(prompt):
    lookup = {name.lower().replace(" ", "_"): name for name in GRAPH}
    while True:
        raw = input(prompt).strip().lower().replace(" ", "_")
        if raw in lookup:
            return lookup[raw]
        print(f"  '{raw}' isn't a valid location. Try one of: {', '.join(GRAPH)}")


def print_city_map():
    print("\nAvailable locations in the city:")
    for place in GRAPH:
        print(f"  - {place}")


def main():
    print("=" * 60)
    print("        SMART CITY ROUTE FINDER")
    print("=" * 60)
    print_city_map()

    start = ask_for_node("\nEnter start location: ")
    goal = ask_for_node("Enter destination: ")

    if start == goal:
        print("You're already there! No route needed.")
        return

    results = []

    bfs_path, bfs_explored = bfs(start, goal)
    results.append(("BFS", bfs_path, path_cost(bfs_path) if bfs_path else None, bfs_explored))

    dfs_path, dfs_explored = dfs(start, goal)
    results.append(("DFS", dfs_path, path_cost(dfs_path) if dfs_path else None, dfs_explored))

    ucs_path, ucs_cost, ucs_explored = ucs(start, goal)
    results.append(("UCS", ucs_path, ucs_cost if ucs_path else None, ucs_explored))

    astar_path, astar_cost, astar_explored = a_star(start, goal)
    results.append(("A*", astar_path, astar_cost if astar_path else None, astar_explored))

    print("\n--- Search Algorithm Comparison ---")
    print(f"{'Algorithm':<10} | {'Path':<45} | {'Cost':<6} | Nodes Explored")
    print("-" * 85)
    for name, path, cost, explored in results:
        path_str = " -> ".join(path) if path else "No route found"
        cost_str = str(cost) if cost is not None else "N/A"
        print(f"{name:<10} | {path_str:<45} | {cost_str:<6} | {explored}")

    valid = [r for r in results if r[2] is not None]
    if valid:
        best = min(valid, key=lambda r: r[2])
        print(f"\nBest route by total distance: {best[0]} "
              f"({' -> '.join(best[1])}, {best[2]} km)")
    else:
        print("\nNo route exists between these two locations.")


if __name__ == "__main__":
    main()
