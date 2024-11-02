import pygame
import sys
import math
import heapq
from collections import deque, defaultdict

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph Traversal Visualization")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

NODE_RADIUS = 20
graph = defaultdict(list)
positions = {}

FONT = pygame.font.SysFont("Arial", 24)

def draw_graph(visited=None, path=None, algorithm_name=""):
    SCREEN.fill(WHITE)
    
    text_surface = FONT.render(f"Algorithm: {algorithm_name}", True, BLACK)
    SCREEN.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 10))
    
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors:
            pygame.draw.line(SCREEN, GRAY, positions[node], positions[neighbor], 2)
    
    for node, pos in positions.items():
        color = BLUE if visited and node in visited else GRAY
        pygame.draw.circle(SCREEN, color, pos, NODE_RADIUS)
        pygame.draw.circle(SCREEN, BLACK, pos, NODE_RADIUS, 2)
    
    if path:
        for node in path:
            pygame.draw.circle(SCREEN, GREEN, positions[node], NODE_RADIUS)
    
    pygame.display.flip()

def dfs(start, end):
    stack = [start]
    visited = set()

    while stack:
        node = stack.pop()
        if node == end:
            return visited, list(visited) + [end]
        if node not in visited:
            visited.add(node)
            stack.extend(neighbor for neighbor, _ in graph[node] if neighbor not in visited)
            draw_graph(visited, algorithm_name="Depth First Search")
            pygame.time.delay(500)

    return visited, []

def bfs(start, end):
    queue = deque([start])
    visited = set()
    parent = {start: None}

    while queue:
        node = queue.popleft()
        if node == end:
            path = []
            while node:
                path.append(node)
                node = parent[node]
            return visited, path[::-1]
        
        if node not in visited:
            visited.add(node)
            for neighbor, _ in graph[node]:
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
                    parent[neighbor] = node
            draw_graph(visited, algorithm_name="Breadth First Search")
            pygame.time.delay(500)

    return visited, []

def dijkstra(start, end):
    visited = set()
    min_heap = [(0, start)]
    distance = {node: float('inf') for node in graph}
    distance[start] = 0
    parent = {start: None}

    while min_heap:
        current_dist, node = heapq.heappop(min_heap)
        if node in visited:
            continue
        visited.add(node)

        if node == end:
            path = []
            while node:
                path.append(node)
                node = parent[node]
            return visited, path[::-1]
        
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                new_dist = current_dist + weight
                if new_dist < distance[neighbor]:
                    distance[neighbor] = new_dist
                    parent[neighbor] = node
                    heapq.heappush(min_heap, (new_dist, neighbor))
        
        draw_graph(visited, algorithm_name="Dijkstra's Algorithm")
        pygame.time.delay(500)

    return visited, []

positions = {
    'A': (100, 100), 'B': (300, 100), 'C': (500, 100),
    'D': (100, 300), 'E': (300, 300), 'F': (500, 300),
    'G': (100, 500), 'H': (300, 500), 'I': (500, 500)
}

edges = [
    ('A', 'B', 1), ('A', 'D', 1), ('B', 'C', 1), ('B', 'E', 1),
    ('C', 'F', 1), ('D', 'E', 1), ('E', 'F', 1), ('D', 'G', 1),
    ('E', 'H', 1), ('F', 'I', 1), ('G', 'H', 1), ('H', 'I', 1)
]

for (node1, node2, weight) in edges:
    graph[node1].append((node2, weight))
    graph[node2].append((node1, weight))

def main():
    start, end = 'A', 'I'
    algorithms = [("Depth First Search", dfs), ("Breadth First Search", bfs), ("Dijkstra's Algorithm", dijkstra)]
    running = True

    for algorithm_name, algorithm in algorithms:
        visited, path = algorithm(start, end)
        draw_graph(visited, path, algorithm_name=algorithm_name)
        pygame.time.delay(2000)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

main()
