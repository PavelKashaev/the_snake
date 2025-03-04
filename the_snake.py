from random import choice

import pygame as pg

"""Константы для размеров поля и сетки."""
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

"""Направления движения."""
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

"""Цвет фона - черный."""
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

"""Цвет яблока."""
APPLE_COLOR = (230, 5, 0)

"""Цвет змейки."""
SNAKE_COLOR = (0, 100, 0)

# Скорость движения змейки:
SPEED = 10

"""Настройка игрового окна."""
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

"""Настройка времени."""
clock = pg.time.Clock()


class GameObject:
    """Создание основного класса описания игры."""

    def __init__(self):
        self.position = SCREEN_CENTER
        self.positions = None
        self.body_color = None

    def draw(self):
        """Абстрактный метод."""
        raise NotImplementedError

    def draw_rect(self, position, body_color):
        """Метод отрисовки классов"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Создание класса описания змеи."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def reset(self):
        """Метод сброса состояния змеи после проигрыша."""
        self.positions = [SCREEN_CENTER]
        self.next_direction = None
        self.direction = RIGHT
        self.lenght = 1
        self.last = None
        self.next_direction = None

    def get_head_position(self):
        """Метод возвращает позицию головы змеи."""
        return self.positions[0]

    def move(self):
        """Метод движения змейки"""
        head_position_x, head_position_y = self.get_head_position()
        snake_direction_x, snake_direction_y = self.direction
        new_head_position = (
            (head_position_x + snake_direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_position_y + snake_direction_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        if len(self.positions) <= self.lenght:
            self.last = None
        else:
            self.last = self.positions.pop()

    def draw(self):
        """Метод прорисовки змеи на игровом поле."""
        for position in self.positions[:-1]:
            self.draw_rect(position, self.body_color)
        self.draw_rect(self.get_head_position(), self.body_color)
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновляет направление змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


class Apple(GameObject):
    """Класс описания яблока"""

    def __init__(self, snake_positions=None) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(snake_positions or [])

    def randomize_position(self, snake_positions=None):
        """Метод для определения координат яблока на доске"""
        while True:
            self.position = (
                choice(range(0, SCREEN_WIDTH, 20)),
                choice(range(0, SCREEN_HEIGHT, 20))
            )
            if self.position not in snake_positions:
                break

    def draw(self):
        """Отрисовка яблока на игровом поле"""
        self.draw_rect(self.position, self.body_color)


def handle_keys(game_object):
    """Функция обработки нажатия клавиш управления."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        pg.display.set_caption('Snake')
        snake.move()
        apple.draw()
        snake.draw()
        snake.update_direction()
        pg.display.update()
        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)


if __name__ == '__main__':
    main()
