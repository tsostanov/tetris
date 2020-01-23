import pygame
import random
import time

pygame.init()
sound = pygame.mixer.Sound('Collected_a_number_of_figures.wav')

figure1 = [['00000',
            '00000',
            '00110',
            '01100',
            '00000'],
           ['00000',
            '00100',
            '00110',
            '00010',
            '00000']]

figure2 = [['00000',
            '00000',
            '01100',
            '00110',
            '00000'],
           ['00000',
            '00100',
            '01100',
            '01000',
            '00000']]

figure3 = [['00100',
            '00100',
            '00100',
            '00100',
            '00000'],
           ['00000',
            '11110',
            '00000',
            '00000',
            '00000']]

figure4 = [['00000',
            '00000',
            '01100',
            '01100',
            '00000']]

figure5 = [['00000',
            '00000',
            '01000',
            '01110',
            '00000'],
           ['00000',
            '00110',
            '00100',
            '00100',
            '00000'],
           ['00000',
            '00000',
            '01110',
            '00010',
            '00000'],
           ['00000',
            '00100',
            '00100',
            '01100',
            '00000']]

figure6 = [['00000',
            '00000',
            '00010',
            '01110',
            '00000'],
           ['00000',
            '00100',
            '00100',
            '00110',
            '00000'],
           ['00000',
            '00000',
            '01110',
            '01000',
            '00000'],
           ['00000',
            '01100',
            '00100',
            '00100',
            '00000']]

figure7 = [['00000',
            '00000',
            '00100',
            '01110',
            '00000'],
           ['00000',
            '00100',
            '00110',
            '00100',
            '00000'],
           ['00000',
            '00000',
            '01110',
            '00100',
            '00000'],
           ['00000',
            '00100',
            '01100',
            '00100',
            '00000']]

shapes = [figure1, figure2, figure3, figure4, figure5, figure6, figure7]
shape_colors = [(255, 215, 0), (0, 255, 255), (75, 0, 130), (47, 80, 80), (255, 20, 147), (0, 0, 128), (225, 0, 0)]


class Piece(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def convert_shape(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '1':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def create_mesh(locked_positions={}):
    mesh = [[(255, 255, 255) for _ in range(10)] for _ in range(20)]
    for i in range(len(mesh)):
        for j in range(len(mesh[i])):
            if (j, i) in locked_positions:
                s = locked_positions[(j, i)]
                mesh[i][j] = s
    return mesh


def space(shape, mesh):
    accepted_positions = [j for sub in [[(j, i) for j in range(10) if mesh[i][j] == (255, 255, 255)]
                                        for i in range(20)] for j in sub]
    formatted = convert_shape(shape)

    for position in formatted:
        if position not in accepted_positions:
            if position[1] > -1:
                return False

    return True


def check_lost(positions):
    for position in positions:
        x, y = position
        if y < 1:
            return True
    return False


def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont(None, size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (80, 300))


def draw_mesh(surface, row, col):
    for i in range(row):
        pygame.draw.line(surface, (0, 0, 0), (50, 75 + i * 30), (350, 75 + i * 30))
        for j in range(col):
            pygame.draw.line(surface, (0, 0, 0), (50 + j * 30, 75), (50 + j * 30, 675))


def clear_rows(mesh, locked):
    counter = 0
    score = 0
    for i in range(len(mesh) - 1, -1, -1):
        row = mesh[i]
        if (255, 255, 255) not in row:
            counter += 1
            s = i
            for j in range(len(row)):
                del locked[(j, i)]
                score += 1
                sound.play()
    if counter > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < s:
                newKey = (x, y + counter)
                locked[newKey] = locked.pop(key)
    return counter


def draw_window(surface, score=0):
    surface.fill((255, 255, 255))
    font = pygame.font.SysFont(None, 60)
    label = font.render('ТЕТРИС', 1, (0, 0, 0))
    surface.blit(label, (125, 30))

    for i in range(len(mesh)):
        for j in range(len(mesh[i])):
            pygame.draw.rect(surface, mesh[i][j], (50 + j * 30, 75 + i * 30, 30, 30), 0)

    draw_mesh(surface, 20, 10)
    pygame.draw.rect(surface, (0, 0, 0), (50, 75, 301, 601), 1)

    font = pygame.font.SysFont(None, 50)
    label = font.render('Счет: ' + str(score), 1, (0, 0, 0))
    surface.blit(label, (375, 300))
    font = pygame.font.SysFont('', 80)
    y = font.render('Я', 1, (255, 0, 0))
    surface.blit(y, (370, 500))
    ndex = font.render('ндекс', 1, (0, 0, 0))
    surface.blit(ndex, (410, 500))
    lyceum = font.render('лицей', 1, (0, 0, 0))
    surface.blit(lyceum, (390, 545))


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont(None, 30)
    label = font.render('Следующая фигура:', 1, (0, 0, 0))

    for i, line in enumerate(shape.shape[shape.rotation % len(shape.shape)]):
        row = list(line)
        for j, column in enumerate(row):
            if column == '1':
                pygame.draw.rect(surface, shape.color, (360 + j * 30, 100 + i * 30, 30, 30), 0)

    x = 390
    y = 100
    for _ in range(5):
        pygame.draw.line(surface, (0, 0, 0), (390, y), (480, y))
        y += 30
    for _ in range(4):
        pygame.draw.line(surface, (0, 0, 0), (x, 100), (x, 220))
        x += 30
    surface.blit(label, (370, 70))


def main():
    global mesh
    locked_positions = {}
    mesh = create_mesh(locked_positions)

    change_piece = False
    run = True
    current = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0

    while run:
        if score <= 5:
            fall_speed = 0.25
        elif 5 < score <= 9:
            fall_speed = 0.20
        elif 9 < score <= 13:
            fall_speed = 0.15
        else:
            fall_speed = 0.1

        mesh = create_mesh(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current.y += 1
            if not (space(current, mesh)) and current.y > 0:
                current.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current.x -= 1
                    if not space(current, mesh):
                        current.x += 1

                elif event.key == pygame.K_RIGHT:
                    current.x += 1
                    if not space(current, mesh):
                        current.x -= 1
                elif event.key == pygame.K_UP:
                    current.rotation = current.rotation + 1 % len(current.shape)
                    if not space(current, mesh):
                        current.rotation = current.rotation - 1 % len(current.shape)

                if event.key == pygame.K_DOWN:
                    current.y += 1
                    if not space(current, mesh):
                        current.y -= 1

        shape_pos = convert_shape(current)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                mesh[y][x] = current.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current.color
            current = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(mesh, locked_positions)

        draw_window(win, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle("Поражение", 100, (255, 0, 0), win)
    pygame.mixer.music.load('Game_Over.mp3')
    pygame.mixer.music.play()
    pygame.display.update()
    time.sleep(2)


def main_menu():
    run = True
    while run:
        win.fill((255, 255, 255))
        draw_text_middle('Нажми любую кнопку', 50, (0, 0, 0), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.load('Fon.mp3')
                pygame.mixer.music.play(-1)
                main()
    pygame.quit()


win = pygame.display.set_mode((600, 700))
pygame.display.set_caption('Тетрис')

main_menu()
