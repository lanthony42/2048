import pygame
from pygame.locals import *
import random

WIDTH = 4
HEIGHT = 4
TILE_WIDTH = 200
TILE_HEIGHT = 200
SCREEN_WIDTH = WIDTH * TILE_WIDTH
SCREEN_HEIGHT = HEIGHT * TILE_HEIGHT
PADDING = 10


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('2048')

        self.font = pygame.font.SysFont('arial', 45)
        self.grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.moves = {K_UP: self.up, K_RIGHT: self.right, K_DOWN: self.down,
                      K_LEFT: self.left}
        self.game_over = False
        self.new_block()

    def run(self):
        while True:
            self.inputs()
            self.draw()

            if self.game_over:
                pygame.quit()
                return

            pygame.display.update()
            self.clock.tick(60)

    def inputs(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in self.moves.keys():
                    if self.moves[event.key]():
                        self.new_block()
            elif event.type == QUIT:
                self.game_over = True

    def draw(self):
        self.screen.fill((0, 0, 0))
        for y, row in enumerate(self.grid):
            for x, num in enumerate(row):
                if num:
                    colour = (200, 150, 120)
                else:
                    colour = (100, 100, 100)
                    num = ''

                pygame.draw.rect(self.screen, colour,
                                 Rect(x * TILE_WIDTH + PADDING, y * TILE_WIDTH + PADDING,
                                      TILE_WIDTH - 2 * PADDING, TILE_HEIGHT - 2 * PADDING))

                text = self.font.render(str(num), True, (0, 0, 0))
                w, h = text.get_size()
                self.screen.blit(text, (x * TILE_WIDTH + TILE_WIDTH // 2 - w // 2,
                                        y * TILE_HEIGHT + TILE_HEIGHT // 2 - h // 2))

    def new_block(self):
        try:
            n = random.randrange(sum(num == 0 for row in self.grid
                                     for num in row))
        except ValueError:
            self.game_over = True
            return

        r = (sum(num == 2 for row in self.grid for num in row) /
             (WIDTH * HEIGHT))
        if random.random() > 1 - 0.4 * r:
            num = 4
        else:
            num = 2

        for i, row in enumerate(self.grid):
            for j, _ in enumerate(row):
                if not self.grid[i][j]:
                    if not n:
                        self.grid[i][j] = num
                        return
                    else:
                        n -= 1

    def left(self):
        changed = False
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if self.grid[i][j] == 0:
                    continue

                new = j
                for k in range(j - 1, -1, -1):
                    if self.grid[i][k] == 0:
                        new = k
                    elif self.grid[i][j] == self.grid[i][k]:
                        self.grid[i][j] *= 2
                        new = k
                        break

                if new != j:
                    self.grid[i][new] = self.grid[i][j]
                    self.grid[i][j] = 0
                    changed = True
        return changed

    def right(self):
        changed = False
        for i in range(HEIGHT):
            for j in range(WIDTH - 1, -1, -1):
                if self.grid[i][j] == 0:
                    continue

                new = j
                for k in range(j + 1, WIDTH):
                    if self.grid[i][k] == 0:
                        new = k
                    elif self.grid[i][j] == self.grid[i][k]:
                        self.grid[i][j] *= 2
                        new = k
                        break

                if new != j:
                    self.grid[i][new] = self.grid[i][j]
                    self.grid[i][j] = 0
                    changed = True
        return changed

    def up(self):
        changed = False
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if self.grid[j][i] == 0:
                    continue

                new = j
                for k in range(j - 1, -1, -1):
                    if self.grid[k][i] == 0:
                        new = k
                    elif self.grid[j][i] == self.grid[k][i]:
                        self.grid[j][i] *= 2
                        new = k
                        break

                if new != j:
                    self.grid[new][i] = self.grid[j][i]
                    self.grid[j][i] = 0
                    changed = True
        return changed

    def down(self):
        changed = False
        for i in range(WIDTH):
            for j in range(HEIGHT - 1, -1, -1):
                if self.grid[j][i] == 0:
                    continue

                new = j
                for k in range(j + 1, HEIGHT):
                    if self.grid[k][i] == 0:
                        new = k
                    elif self.grid[j][i] == self.grid[k][i]:
                        self.grid[j][i] *= 2
                        new = k
                        break

                if new != j:
                    self.grid[new][i] = self.grid[j][i]
                    self.grid[j][i] = 0
                    changed = True
        return changed


if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
