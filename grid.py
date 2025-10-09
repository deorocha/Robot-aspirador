import pygame
from pygame.locals import KEYDOWN, K_q
pygame.init()

# Cria o array de um Grid com 7 linhas por 7 colunas
# grid = [[0 for x in range(num_rows)] for y in range(num_cols)]

# Define objetos do Ambiente
grid = [(1, 0, 0, 0, 0, 0, 0),
        (0, 0, 3, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 2, 0, 3, 0),
        (0, 0, 0, 0, 3, 4, 0),
        (0, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 3)]
# 0 - Empty
# 1 - Robot 1
# 2 - Robot 2
# 3 - Garbage
# 4 - Gold

black = (0, 0, 0)
white = (255, 255, 255)
width = 50
height = 50
margin = 2
num_rows = 7
num_cols = 7
cell_size = 50

# Desenha Janela
screen_width = 366
screen_height = 366
window_size = [screen_width, screen_height]
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Ambiente")

robot11_load = pygame.image.load("./images/robot_1.png")
robot11_image = pygame.transform.scale(robot11_load, (width, height))

robot12_load = pygame.image.load("./images/robot_1.png")
robot12_image = pygame.transform.scale(robot12_load, (width, height))

robot2_load = pygame.image.load("./images/robot_2.png")
robot2_image = pygame.transform.scale(robot2_load, (width, height))

gold_load = pygame.image.load("./images/gold.png")
gold_image = pygame.transform.scale(gold_load, (width, height))

lixo_load = pygame.image.load("./images/lixo_1.png")
lixo_image = pygame.transform.scale(lixo_load, (width, height))

def desenha_grid(num_rows, num_cols, cell_size, width, height, margin):
    screen.fill(black)
    for row in range(num_rows):
        for col in range(num_cols):
            x = col * (cell_size + margin) + margin
            y = row * (cell_size + margin) + margin
            pygame.draw.rect(screen, white, [(margin + width) * col+margin,
                (margin + height) * row + margin, width, height])
    pygame.display.update()

def mostra_imagem(imagem, row, col):
    x = col * (cell_size + margin) + margin
    y = row * (cell_size + margin) + margin
    screen.blit(imagem, (x, y))
    pygame.display.update()

desenha_grid(num_rows, num_cols, cell_size, width, height, margin)
mostra_imagem(robot2_image, 3, 3)
mostra_imagem(lixo_image, 1, 2)
mostra_imagem(lixo_image, 3, 5)
mostra_imagem(lixo_image, 4, 4)
mostra_imagem(lixo_image, 6, 6)
mostra_imagem(gold_image, 4, 5)

col = 0
row = 0
robot1 = robot11_image
while True:
    if grid[col][row] == 3:
        robot1 = robot12_image
    else:
        robot1 = robot11_image
        
    desenha_grid(num_rows, num_cols, cell_size, width, height, margin)
    mostra_imagem(robot1, row, col)
    pygame.time.wait(300) # pygame.time.delay(1000)
    col += 1
    if col >= num_cols:
        col = 0
        row +=1
        if row >= num_rows:
            row = 0


#robot_1 = [(0, 0)]
#robot_2 = [(3, 3)]
#lixo = [(1,2), (3,5), (4,4), (6,6)]
#ouro = [(4,5)]

# Define player properties
robot1_x = 0
robot1_y = 0
robot1_width = 50
robot1_height = 50
robot1_step = 1

"""
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)  # Fill background with white
    for row in range(num_rows):
        for col in range(num_cols):
            x = col * (cell_size + margin) + margin
            y = row * (cell_size + margin) + margin
            pygame.draw.rect(screen, white, [(margin + width) * col+margin,
                (margin + height) * row + margin, width, height])
            screen.blit(robot1_image, (x, y))
            pygame.time.wait(100) # pygame.time.delay(1000)
            pygame.display.update()


    pygame.display.flip()

pygame.quit()
"""

"""
    keys = pygame.key.get_pressed()
    # Update player position based on key presses
    if keys[pygame.K_LEFT]:
        robot1_x -= robot1_step
    if keys[pygame.K_RIGHT]:
        robot1_x += robot1_step
    if keys[pygame.K_UP]:
        robot1_y -= robot1_step
    if keys[pygame.K_DOWN]:
        robot1_y += robot1_step

    # Keep player within screen bounds (optional)
    if robot1_x < 0:
        robot1_x = 0
    if robot1_x + robot1_width > screen_width:
        robot1_x = screen_width - robot1_width
    if robot1_y < 0:
        robot1_y = 0
    if robot1_y + robot1_height > screen_height:
        robot1_y = screen_height - robot1_height
        
    screen.blit(robot1_image, (robot1_x, robot1_y))
"""
    

