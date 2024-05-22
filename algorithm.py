from constant import *
from random import choice
from collections import deque
from math import sqrt

class Node:
    def __init__(self, id: tuple[int, int], prev_id: tuple[int, int] = (-1, -1), depth = 0, cost = 0):
        self.id = id
        self.prev_id = prev_id
        self.depth = depth
        self.cost = cost

    def get_heuristic(self, food_id: tuple[int, int]):
        return int(sqrt((self.id[0] - food_id[0])**2 + (self.id[1] - food_id[1])**2))

class Algorithm:
    def __init__(self, snake_parts_id: list[tuple[int, int]], noises_id: list[tuple[int, int]]) -> None:
        self.snake_parts_id = snake_parts_id
        self.noises_id = noises_id
        self.food_id: tuple[int, int] = ()
        self.other_snake_parts_id: list[tuple[int, int]] = []
        self.frontier: deque[Node] = deque([Node(self.snake_parts_id[0])])
        self.visited: dict[tuple[int, int], Node] = {}
        self.path: list[tuple[tuple[int, int], str]] = []
        self.node_num = 1
        self.max_depth = 0
        self.is_found = False
        self.name = ''
        self.direction_dict: dict[tuple[int, int], str] = {(1, 0) : 'right', (0, 1) : 'down', (-1, 0) : 'left', (0, -1) : 'up'}

    def input_current_state(self, snake_parts_id : list[tuple[int, int]], other_snake_parts_id: list[tuple[int, int]], food_id: tuple[int, int], name: str) -> None:
        self.snake_parts_id = snake_parts_id
        self.other_snake_parts_id = other_snake_parts_id
        self.food_id = food_id
        self.frontier.clear()
        self.frontier.append(Node(self.snake_parts_id[0]))
        self.visited.clear()
        self.path.clear()
        self.node_num = 1
        self.max_depth = 0
        self.is_found = False
        self.name = name

    def find_neighbors(self, node: Node) -> list[Node]:
        neighbors: list[Node] = []
        if node.id[0] + 1 < COLUMNS: #right
            neighbors.append(Node((node.id[0] + 1, node.id[1]), node.id, node.depth + 1, node.cost + 1))
        if node.id[1] + 1 < ROWS: #down
            neighbors.append(Node((node.id[0], node.id[1] + 1), node.id, node.depth + 1, node.cost + 1))
        if node.id[0] - 1 > -1: #left
            neighbors.append(Node((node.id[0] - 1, node.id[1]), node.id, node.depth + 1, node.cost + 1))
        if node.id[1] - 1 > -1: #up
            neighbors.append(Node((node.id[0], node.id[1] - 1), node.id, node.depth + 1, node.cost + 1))

        visited_id: list[tuple[int, int]] = [visited_key for visited_key in self.visited]
        invalid_id: list[tuple[int, int]] = self.snake_parts_id + self.other_snake_parts_id + self.noises_id + visited_id
        if self.name != 'DFS':
            frontier_id: list[tuple[int, int]] = [frontier_node.id for frontier_node in self.frontier]
            invalid_id += frontier_id

        i = 0
        neighbors_num = len(neighbors)
        for _ in range(neighbors_num):
            if neighbors[i].id in invalid_id:
                neighbors.pop(i)
            else:
                i += 1
        return neighbors
    
    def get_path(self, node: Node) -> None:
        while node.prev_id != (-1, -1):
            position: tuple[int, int] = (node.prev_id[0] * CELL_SIZE + BOARD_OFFSET + PART_SIZE, node.prev_id[1] * CELL_SIZE + BOARD_OFFSET + PART_SIZE)
            direction: str = self.direction_dict[(node.id[0] - node.prev_id[0], node.id[1] - node.prev_id[1])]
            self.path.insert(0, (position, direction))
            node = self.visited[node.prev_id]

    def get_key(self, node: Node) -> int:
        if self.name == 'UCS':
            return node.cost
        if self.name == 'Greedy':
            return node.get_heuristic(self.food_id)
        if self.name == 'A Star':
            return node.get_heuristic(self.food_id) + node.cost

    def sort_frontier(self):
        self.frontier = deque(sorted(self.frontier, key = self.get_key))

    def dfs(self) -> None:
        while True:
            if len(self.frontier) == 0:
                self.is_found = False
                return
            
            node: Node = self.frontier.pop()
            if node.id == self.food_id:
                self.is_found = True
                self.get_path(node)
                return
            
            neighbors: list[Node] = self.find_neighbors(node)
            while len(neighbors) != 0:
                neighbor: Node = choice(neighbors)
                self.frontier.append(neighbor)
                neighbors.remove(neighbor)
                self.node_num += 1
                if self.max_depth < neighbor.depth:
                    self.max_depth = neighbor.depth
            self.visited[node.id] = node

    def bfs(self) -> None:
        while True:
            if len(self.frontier) == 0:
                self.is_found = False
                return
            
            node: Node = self.frontier.popleft()
            if node.id == self.food_id:
                self.is_found = True
                self.get_path(node)
                return
            
            neighbors: list[Node] = self.find_neighbors(node)
            for neighbor in neighbors:
                self.frontier.append(neighbor)
                self.node_num += 1
                if self.max_depth < neighbor.depth:
                    self.max_depth = neighbor.depth
            self.visited[node.id] = node

    def ucs(self) -> None:
        while True:
            if len(self.frontier) == 0:
                self.is_found = False
                return
            
            self.sort_frontier()
            node: Node = self.frontier.popleft()
            if node.id == self.food_id:
                self.is_found = True
                self.get_path(node)
                return
            
            neighbors: list[Node] = self.find_neighbors(node)
            for neighbor in neighbors:
                self.frontier.append(neighbor)
                self.node_num += 1
                if self.max_depth < neighbor.depth:
                    self.max_depth = neighbor.depth
            self.visited[node.id] = node

    def greedy(self) -> None:
        while True:
            if len(self.frontier) == 0:
                self.is_found = False
                return
            
            self.sort_frontier()
            node: Node = self.frontier.popleft()
            if node.id == self.food_id:
                self.is_found = True
                self.get_path(node)
                return
            
            neighbors: list[Node] = self.find_neighbors(node)
            for neighbor in neighbors:
                self.frontier.append(neighbor)
                self.node_num += 1
                if self.max_depth < neighbor.depth:
                    self.max_depth = neighbor.depth
            self.visited[node.id] = node

    def a_star(self) -> None:
        while True:
            if len(self.frontier) == 0:
                self.is_found = False
                return
            
            self.sort_frontier()
            node: Node = self.frontier.popleft()
            if node.id == self.food_id:
                self.is_found = True
                self.get_path(node)
                return
            
            neighbors: list[Node] = self.find_neighbors(node)
            for neighbor in neighbors:
                self.frontier.append(neighbor)
                self.node_num += 1
                if self.max_depth < neighbor.depth:
                    self.max_depth = neighbor.depth
            self.visited[node.id] = node
