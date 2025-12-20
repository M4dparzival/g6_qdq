from collections import deque

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, source, target):
        if source not in self.adj_list:
            self.add_vertex(source)
        if target not in self.adj_list:
            self.add_vertex(target)
        if target not in self.adj_list[source]:
            self.adj_list[source].append(target)
        if source not in self.adj_list[target]:
            self.adj_list[target].append(source)

    def get_neighbors(self, vertex):
        return self.adj_list.get(vertex, [])

    def bfs_shortest_path(self, start, goal):
        if start not in self.adj_list or goal not in self.adj_list:
            return None
        visited = set()
        queue = deque([start])
        visited.add(start)
        parent = {start: None}

        while queue:
            current = queue.popleft()
            if current == goal:
                # Reconstruct path
                path = []
                while current is not None:
                    path.append(current)
                    current = parent[current]
                path.reverse()
                return path
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent[neighbor] = current
        return None


if __name__ == "__main__":
    g = Graph()

    # MRT-3 stations
    mrt3 = ["North Avenue", "Quezon Avenue", "GMA-Kamuning", "Araneta Center-Cubao", "Anonas", "Katipunan", "Santolan", "Ortigas", "Shaw Boulevard", "Boni", "Guadalupe", "Buendia", "Ayala", "Magallanes", "Taft Avenue"]
    for i in range(len(mrt3) - 1):
        g.add_edge(mrt3[i], mrt3[i + 1])

    # LRT-1 stations
    lrt1 = ["Baclaran", "EDSA", "Libertad", "Gil Puyat", "Vito Cruz", "Quirino", "Pedro Gil", "UN Avenue", "Central Terminal", "Carriedo", "Doroteo Jose", "Bambang", "Tayuman", "Blumentritt", "Abad Santos", "R. Papa", "5th Avenue", "Monumento", "Balintawak", "Roosevelt"]
    for i in range(len(lrt1) - 1):
        g.add_edge(lrt1[i], lrt1[i + 1])

    # LRT-2 stations
    lrt2 = ["Recto", "Legarda", "Pureza", "V. Mapa", "J. Ruiz", "Gilmore", "Betty Go-Belmonte", "Araneta Center-Cubao", "Anonas", "Katipunan", "Santolan", "Antipolo"]
    for i in range(len(lrt2) - 1):
        g.add_edge(lrt2[i], lrt2[i + 1])

    # Test shortest path from Boni to V. Mapa
    path = g.bfs_shortest_path("Boni", "V. Mapa")
    print("Shortest path from Boni to V. Mapa:", path)
