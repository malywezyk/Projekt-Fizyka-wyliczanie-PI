import pygame
import math

class Square(object):
    def __init__(self, size, XY, mass, velocity):
        self.init_x = XY[0]
        self.init_y = XY[1]
        self.x = self.init_x
        self.y = self.init_y
        self.mass = mass
        self.init_v = velocity
        self.v = self.init_v
        self.size = size

    def collision(self, otherblock):
        if self.x + self.size < otherblock.x or self.x > otherblock.x + otherblock.size:
            return False
        else:
            return True

    def NewVelocity(self, otherblock):
        sumM = self.mass + otherblock.mass
        newV = (self.mass - otherblock.mass) / sumM * self.v
        newV += (2 * otherblock.mass / sumM) * otherblock.v
        return newV

    def collide_wall(self):
        if self.x <= 0:
            self.v *= -1
            return True

    def update(self):
        self.x += self.v

    def draw(self, background, otherblock):
        if self.x < 10:
            pygame.draw.rect(background, czerwony, [10, self.y, self.size, self.size])
            pygame.draw.rect(background, czerwony, [0, otherblock.y, otherblock.size, otherblock.size])
        else:
            pygame.draw.rect(background, czerwony, [self.x, self.y, self.size, self.size])
            pygame.draw.rect(background, czerwony, [otherblock.x, otherblock.y, otherblock.size, otherblock.size])

    def reset(self):
        self.x = self.init_x
        self.y = self.init_y
        self.v = self.init_v

def redraw():
    background.fill(szary)
    pygame.draw.rect(background, czarny, [0, 0, 800, 250])
    SquareBig.draw(background, SquareSmall)
    font = pygame.font.SysFont(None, 50)
    text = font.render(f"{count:,}", True, (0, 0, 0))
    background.blit(text, [100, 270])
    n_text = font.render(f"Masa = 100^{n} [kg]", True, (0, 0, 0))
    background.blit(n_text, [100, 320])
    pygame.display.update()

width, height = 800, 400
szary = (107, 107, 107)
czarny = (5, 2, 3)
czerwony = (200, 0, 0)

pygame.init()
n = 5
power = math.pow(100, n)
background = pygame.display.set_mode((width, height))

SquareBig = Square(50, (320, 200), power, -0.9 / 10500)
SquareSmall = Square(20, (100, 230), 1, 0)

count = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                SquareBig.reset()
                SquareSmall.reset()
                count = 0
            elif event.key == pygame.K_UP:
                n += 1
                power = math.pow(100, n)
                SquareBig.mass = power
            elif event.key == pygame.K_DOWN:
                n = max(0, n - 1)
                power = math.pow(100, n)
                SquareBig.mass = power

    for i in range(10000):
        if SquareSmall.collision(SquareBig):
            count += 1
            v1 = SquareSmall.NewVelocity(SquareBig)
            v2 = SquareBig.NewVelocity(SquareSmall)
            SquareBig.v = v2
            SquareSmall.v = v1
        if SquareSmall.collide_wall():
            count += 1
        SquareBig.update()
        SquareSmall.update()

    redraw()

pygame.quit()
