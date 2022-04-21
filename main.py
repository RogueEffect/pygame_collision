
import math
import random

import pygame


WIDTH = 500
HEIGHT = 400
SCALE = 2
SWIDTH = WIDTH * SCALE
SHEIGHT = HEIGHT * SCALE

MOVE_KEYS = [pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a]

DIRS = {
    0: [0, -1],
    1: [1, 0],
    2: [0, 1],
    3: [-1, 0]
}

MAGENTA = (255, 0, 255)
SPEED = 2

def randpos(x=0, y=0, width=WIDTH, height=HEIGHT):
    xx = random.randint(x, width)
    yy = random.randint(y, height)
    return xx, yy


class Player:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.radius = 16
        self.surface = pygame.Surface((32, 32))
        self.surface.fill(MAGENTA)
        pygame.draw.circle(self.surface, (255, 0, 0), (self.radius, self.radius), self.radius)
        self.surface.set_colorkey(MAGENTA)
        self.tick_count = 0
    
    def tick(self):
        self.tick_count += 1
        
    def render(self, surface, xoffset, yoffset):
        surface.blit(self.surface, (xoffset, yoffset))
    
    def move(self, direction):
        dx, dy = DIRS[direction]
        self.x += dx * SPEED
        self.y += dy * SPEED
    
    def collided(self, other):
        dx = (other.x + other.radius) - (self.x + self.radius)
        dy = (other.y + other.radius) - (self.y + self.radius)
        dist = math.sqrt((dx * dx) + (dy * dy))
        if dist <= self.radius + other.radius:
            return True
        return False

class Food:
    def __init__(self, x=0, y=0):
        global curfood
        self.name = hash(self)
        self.x = x
        self.y = y
        self.radius = 4
        self.surface = pygame.Surface((8, 8))
        self.surface.fill(MAGENTA)
        pygame.draw.circle(self.surface, (0, 255, 0), (self.radius, self.radius), self.radius)
        self.surface.set_colorkey(MAGENTA)
    
    def tick(self):
        ...
    
    def render(self, surface, xoffset, yoffset):
        surface.blit(self.surface, (xoffset + self.x, yoffset + self.y))

class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((SWIDTH, SHEIGHT))
        pygame.display.set_caption("Collision Test")
        pygame.key.set_repeat(10, 10)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.tick_count = 0
        
        self.player = Player(10, 10)
        self.foods = [Food(*randpos(width=WIDTH-4, height=HEIGHT-4)) for _ in range(100)]

    def run(self):
        while self.running:
            self.tick()
            self.render()
        pygame.quit()
        print("Goodbye")

    def tick(self):
        self.clock.tick(60)
        
        if not self.foods:
            print('You ate all the food!')
            self.running = False
        
        pressed = pygame.key.get_pressed()
        for i, key in enumerate(MOVE_KEYS):
            if pressed[key]:
                self.player.move(i)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        for i, food in enumerate(self.foods):
            if self.player.collided(food):
                self.foods.pop(i)
        
        if self.tick_count % 60 == 0 and random.getrandbits(len(self.foods) // 2) == 0:
            self.foods.append(Food(*randpos(width=WIDTH-4, height=HEIGHT-4)))
        
        self.player.tick()
        self.tick_count += 1

    def render(self):
        self.screen.fill((0, 0, 0))
        
        self.player.render(self.screen, self.player.x, self.player.y)
        for food in self.foods:
            food.render(self.screen, 0, 0)
        
        self.display.blit(pygame.transform.scale(self.screen, (SWIDTH, SHEIGHT)), (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run()
