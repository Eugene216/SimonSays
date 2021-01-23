import pygame
import time
import random
import sys
import os
import shelve
from pygame.locals import *

FPS = 50


def draw_rect(x, y, border_color, color):  # Рисуем кнопки
    pygame.draw.rect(screen, border_color, (x + 15, y + 15, 200, 150), width=10)
    pygame.draw.rect(screen, color, (x + 16, y + 16, 198, 148))


def load_image(name, colorkey=None):  # Загрузка картинки
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():  # Выход из игры
    pygame.quit()
    sys.exit()


def start_screen():  # Стартовый экран
    intro_text = ["                                             Саймон говорит", "",
                  "Правила:",
                  "Запоминайте порядок выделенных кнопок и нажимайте их.",
                  "Цель игры: набрать как можно больше очков.",
                  "", "", "", "", "", "",
                  "Нажмите esc чтобы выйти.",
                  "Чтобы начать, нажмите любую кнопку на клавиатуре."]

    fon = pygame.transform.scale(load_image('fon 3.png'), (950, 600))
    screen.blit(fon, (0, 0))
    logo = pygame.transform.scale(load_image('logo.png'), (300, 300))
    screen.blit(logo, (650, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def Quit_Check():  # Проверка на выход из игры
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def Get_Button(x, y):  # Получение кнопки
    if Rect_Yellow.collidepoint((x, y)):
        return pygame.Color("Yellow")
    elif Rect_Blue.collidepoint((x, y)):
        return pygame.Color("Blue")
    elif Rect_Red.collidepoint((x, y)):
        return pygame.Color("Red")
    elif Rect_Green.collidepoint((x, y)):
        return pygame.Color("Green")
    return None


def Animation_button(color, Animation_Speed=50, mistake=False):  # Анимация нажатия кнопок
    if color == pygame.Color("Yellow"):
        flashColor = (251, 255, 207)
        rectangle = Rect_Yellow
    elif color == pygame.Color("Blue"):
        flashColor = (179, 241, 255)
        rectangle = Rect_Blue
    elif color == pygame.Color("Red"):
        flashColor = (255, 181, 211)
        rectangle = Rect_Red
    elif color == pygame.Color("Green"):
        flashColor = (163, 255, 205)
        rectangle = Rect_Green
    if mistake == True:
        flashColor = (80, 80, 80)
    # Звук нажатия
    beep_sound.play()
    Orig_screen = screen.copy()
    Another_screen = pygame.Surface((200, 150))
    Another_screen = Another_screen.convert_alpha()
    r, g, b = flashColor
    # цикл анимации
    for Start, End, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(Start, End, Animation_Speed * step):
            Quit_Check()
            screen.blit(Orig_screen, (0, 0))
            Another_screen.fill((r, g, b, alpha))
            screen.blit(Another_screen, rectangle.topleft)
            pygame.display.update()
            fps_clock.tick(FPS)
    screen.blit(Orig_screen, (0, 0))


def Loop_Animation(color=(255, 50, 50), Animation_Speed=35, win=False):  # Анимация после игрового круга
    if win is True:
        color = (102, 255, 0)
    Orig_screen = screen.copy()
    Another_screen = pygame.Surface(screen.get_size())
    Another_screen = Another_screen.convert_alpha()
    r, g, b = color
    for i in range(2):  # Моргание 2 раза
        for Start, End, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(Start, End, Animation_Speed * step):
                Quit_Check()
                Another_screen.fill((r, g, b, alpha))
                screen.blit(Orig_screen, (0, 0))
                screen.blit(Another_screen, (0, 0))
                draw_rect(485, 110, (255, 130, 130), pygame.Color("Red"))
                draw_rect(235, 110, (158, 255, 188), (0, 224, 0))
                draw_rect(485, 310, (151, 238, 255), (0, 0, 255))
                draw_rect(235, 310, (243, 255, 151), pygame.Color("Yellow"))
                pygame.display.update()
                fps_clock.tick(FPS)
    # Обновляем экран
    screen.fill((random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)))
    draw_rect(485, 110, (255, 130, 130), pygame.Color("Red"))
    draw_rect(235, 110, (158, 255, 188), (0, 224, 0))
    draw_rect(485, 310, (151, 238, 255), (0, 0, 255))
    draw_rect(235, 310, (243, 255, 151), pygame.Color("Yellow"))
    make_label('Score: ', (940, 10), score)
    make_label('Record: ', (130, 10), score_r)
    make_label('Total Score: ', (930, 570), score_t)
    make_label('Press Esc to Quit', (200, 570), None)
    pygame.display.flip()


def make_label(name, coordinates, score):  # создание надписей
    if score is None:
        label = MAIN_FONT.render(name, 1, pygame.Color("White"))
    else:
        label = MAIN_FONT.render(name + str(score), 1, pygame.Color("White"))
    rect = label.get_rect()
    rect.topright = coordinates
    screen.blit(label, rect)


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    # Создаем экран и кнопки
    size = width, height = 950, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Simon says')
    start_screen()
    screen.fill((0, 0, 0))
    pygame.display.flip()
    draw_rect(485, 110, (255, 130, 130), pygame.Color("Red"))
    draw_rect(235, 110, (158, 255, 188), (0, 224, 0))
    draw_rect(485, 310, (151, 238, 255), (0, 0, 255))
    draw_rect(235, 310, (243, 255, 151), pygame.Color("Yellow"))
    pygame.display.flip()
    score = 0
    fps_clock = pygame.time.Clock()
    # Достаем рекорд и общие очки
    try:
        d = shelve.open('score.txt')
        score_r = d['score_r']
    except:
        score_r = 0
    try:
        d = shelve.open('score_total.txt')
        score_t = d['score_t']
    except:
        score_t = 0
    # Создаем звук
    beep_sound = pygame.mixer.Sound('data/beep.wav')
    # Создаем надписи
    MAIN_FONT = pygame.font.Font('freesansbold.ttf', 22)
    make_label('Score: ', (940, 10), score)
    make_label('Record: ', (130, 10), score_r)
    make_label('Total Score: ', (930, 570), score_t)
    make_label('Press Esc to Quit', (200, 570), None)
    # Вводим необходимые переменные
    Last_Click = 0
    Color_Pattern = []
    Step = 0
    waiting = False
    Rect_Yellow = pygame.Rect(235 + 15, 310 + 15, 200, 150)
    Rect_Blue = pygame.Rect(485 + 15, 310 + 15, 200, 150)
    Rect_Red = pygame.Rect(485 + 15, 110 + 15, 200, 150)
    Rect_Green = pygame.Rect(235 + 15, 110 + 15, 200, 150)
    # Основной игровой цикл
    while True:
        Button_click = None
        Quit_Check()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                Button_click = Get_Button(mouse_x, mouse_y)

        if not waiting:
            # Проигрывание кнопок
            pygame.display.update()
            pygame.time.wait(1000)
            Color_Pattern.append(random.choice((pygame.Color("Yellow"), pygame.Color("Blue"), pygame.Color("Red"), pygame.Color("Green"))))
            for button in Color_Pattern:
                Animation_button(button)
                pygame.time.wait(200)
            waiting = True
        else:
            # Ожидание действия игрока
            if Button_click and Button_click == Color_Pattern[Step]:
                # Если кнопка нажата првильно
                Animation_button(Button_click)
                Step += 1
                Last_Click = time.time()

                if Step == len(Color_Pattern):
                    pygame.display.flip()
                    waiting = False
                    Step = 0
                    score += 1
                    score_t += 1
                    if score >= score_r:  # Сохраняем рекорд
                        score_r = score
                        d = shelve.open('score.txt')
                        d['score_r'] = score_r
                        d.close()
                    d = shelve.open('score_total.txt')  # Сохраняем общие очки
                    d['score_t'] = score_t
                    d.close()
                    Loop_Animation(win=True)  # Анимация после одного круга игры(при верном выборе)
            # Если кнопка нажата непрвильно
            elif (Button_click and Button_click != Color_Pattern[Step]) or (Step != 0 and time.time() - 4 > Last_Click):
                score = 0
                Animation_button(Button_click)
                Loop_Animation()  # Анимация при неверном выборе
                # Обнуляем переменные:
                Color_Pattern = []
                Step = 0
                waiting = False
                pygame.time.wait(1000)
        pygame.display.update()
        fps_clock.tick(FPS)
