import pygame
import sys
import math
import random
import time

# 初始化 Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT =800,600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("炮兵训练营")

WHITE = (100, 255, 100)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
tree_x, tree_y = 50, HEIGHT - 500
tree_destroyed = False

cannon_x, cannon_y = WIDTH - 150, HEIGHT - 100
cannon_angle = math.pi * 3 / 4
cannon_angle_step = math.pi / 36

cannonball_radius = 15
cannonball_speed = 10
cannonball_fired = False
cannonball_hit_tree = False

random.seed(time.time())
tree_x = random.randint(40, round(WIDTH / 3))
score = 0
gravity = 5

run = True
font = pygame.font.Font("c:/windows/fonts/simsun.ttc", 20)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not cannonball_fired:
                    cannonball_fired = True
                    cannonball_x = cannon_x + 100
                    cannonball_y = cannon_y + 10
                    cannonball_velocity_x = cannonball_speed * math.cos(cannon_angle)
                    cannonball_velocity_y = -cannonball_speed * math.sin(cannon_angle)
            elif event.key == pygame.K_UP:
                cannon_angle -= cannon_angle_step
            elif event.key == pygame.K_DOWN:
                cannon_angle += cannon_angle_step
            elif event.key == pygame.K_LEFT:
                gravity -= 1
                if gravity < 1:
                    gravity = 1
            elif event.key == pygame.K_RIGHT:
                gravity += 1
                if gravity > 5:
                    gravity = 5

    if cannonball_fired and not cannonball_hit_tree:
        cannonball_x += cannonball_velocity_x
        cannonball_velocity_y += 0.2 - (gravity * 0.01)
        cannonball_y += cannonball_velocity_y
        if cannonball_y > HEIGHT:
            cannonball_fired = False

    win.fill(WHITE)

    if not tree_destroyed:
        if cannonball_hit_tree:
            pygame.draw.polygon(win, RED, [(tree_x + 50, tree_y), (tree_x, tree_y + 150), (tree_x + 100, tree_y + 150)])
        else:
            pygame.draw.polygon(win, GREEN,
                                [(tree_x + 50, tree_y), (tree_x, tree_y + 150), (tree_x + 100, tree_y + 150)])

        pygame.draw.rect(win, BLACK, (tree_x + 45, tree_y + 150, 10, 50))
    cannonball_hit_tree = False

    pygame.draw.line(win, BLACK, (cannon_x + 100, cannon_y + 10),
                     (cannon_x + 100 + 50 * math.cos(cannon_angle),
                      cannon_y + 10 - 50 * math.sin(cannon_angle)), 3)

    if cannonball_fired:
        pygame.draw.circle(win, BLACK, (int(cannonball_x), int(cannonball_y)), cannonball_radius)

    if not tree_destroyed and cannonball_fired:
        if tree_x < cannonball_x < tree_x + 100 and tree_y < cannonball_y < tree_y + 200:
            cannonball_x = -50
            score += 1
            cannonball_hit_tree = True
            tree_x = random.randint(40, round(WIDTH / 3))

    score_text = font.render("得分: " + str(score), True, BLACK)
    win.blit(score_text, (10, 10))
    gravity_text = font.render("当前火力: " + str(gravity), True, BLACK)
    win.blit(gravity_text, (WIDTH - 130, HEIGHT - 70))
    gravity_text = font.render("上下键调整角度，左右键火力 ", True, BLACK)
    win.blit(gravity_text, (WIDTH - 280, HEIGHT - 30))

    pygame.display.update()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()