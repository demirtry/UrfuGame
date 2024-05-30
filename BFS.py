import numpy as np
from collections import deque


class BreadthFirstSearch:
    def __init__(self, platforms):
        tile = (32, 24)
        self.rows = 32
        self.columns = 32
        self.tiles = np.zeros((self.rows, self.columns), dtype=np.int16)
        self.visited = {}
        self.way = []
        for platform in platforms:
            platform_size = platform.get_rect().size[0] // 32
            platform_tile_row_index = platform.get_coordinates()[1] // tile[1]
            platform_tile_column_index = platform.get_coordinates()[0] // tile[0]

            for i in range(platform_size):
                self.tiles[platform_tile_row_index][platform_tile_column_index] = 1
                platform_tile_column_index += 1

    def get_next_tiles(self, row, column):
        ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, 1], [1, -1], [-1, 1]
        return [(row + d_row, column + d_column) for d_row, d_column in ways if self.check_next_tile(row + d_row, column + d_column)]

    def check_next_tile(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns and not self.tiles[row][column]:
            return True
        return False

    def find_way(self, start, end):

        if start == end:
            return None

        queue = deque([start])
        self.visited = {start:  None}

        while queue:
            current_tile = queue.popleft()
            if current_tile == end:
                break
            next_tiles = self.get_next_tiles(current_tile[0], current_tile[1])
            for next_tile in next_tiles:
                if next_tile not in self.visited:
                    queue.append(next_tile)
                    self.visited[next_tile] = current_tile
        return self.get_current_action(start, end)

    def get_current_action(self, start, end):
        self.way = [end]
        cur = end
        while self.visited:
            self.way.append(self.visited.get(cur))
            cur = self.visited.get(cur)
            if cur == start:
                break

        return self.call_current_action(start, self.way[-2])

    @staticmethod
    def call_current_action(start, way):
        if start[0] > way[0]:
            if start[1] > way[1]:
                return 'up left'
            elif start[1] < way[1]:
                return 'up right'
            else:
                return 'up'
        elif start[0] < way[0]:
            if start[1] > way[1]:
                return 'down left'
            elif start[1] < way[1]:
                return 'down right'
            else:
                return 'down'
        else:
            if start[1] > way[1]:
                return 'left'
            else:
                return 'right'
