from random import randint
from threading import Thread
import time
from keyboard import is_pressed


class SnakeGame:

    empty_field = "[ ]"
    snake_field = "[=]"
    snake_heads = ["[A]", "[>]", "[V]", "[<]"]
    apple_field = "[O]"
    MOVE_CURSOR_UP = "\033[A"
    key_map = "wdsa"
    score = 0

    def __init__(self, field_size=(10, 10), update_delay=0.5) -> None:
        self.field_size = field_size
        self.field = [
            [self.empty_field for _ in range(field_size[0])]
            for _ in range(field_size[1])
        ]
        self.snake_poses = [(0, 0)]
        self.direction = -1
        self.snake_spawn = self.snake_poses[0]
        self.update_delay = update_delay
        self.__printed = False
        self.run = True
        self.key_listener = Thread(target=self.listen_for_input)
        self.spawn_snake()
        self.apple_pos = self.spawn_apple()
        self.key_listener.start()

    def wait_for_start(self):
        while self.direction in (-1, 0, 3):
            time.sleep(0.001)
        self.field_directions = {self.snake_poses[0]: self.direction}

    def listen_for_input(self):
        while self.run:
            for i, c in enumerate(self.key_map):
                if is_pressed(c) and (
                    self.direction == -1 or abs(i - self.direction) != 2
                ):
                    self.direction = i
                    time.sleep(self.update_delay)
            time.sleep(0.0001)

    def __str__(self) -> str:
        out = ""
        for row in self.field:
            out += "".join(row) + "\n"
        return out

    def print(self):
        if self.__printed:
            print(end=self.MOVE_CURSOR_UP * (self.field_size[1] + 1))
        print(self)
        self.__printed = True

    def spawn_snake(self):
        assert self.field[0][0] == self.empty_field
        self.field[0][0] = self.snake_heads[1]

    def spawn_apple(self):
        while True:
            rx, ry = randint(0, self.field_size[0] - 1), randint(
                0, self.field_size[1] - 1
            )
            if self.field[ry][rx] == self.empty_field:
                break
        self.field[ry][rx] = self.apple_field
        return rx, ry

    def check_head(self):
        x, y = self.snake_poses[0]
        nx, ny = x, y

        if self.direction == 0:
            ny -= 1
        elif self.direction == 1:
            nx += 1
        elif self.direction == 2:
            ny += 1
        elif self.direction == 3:
            nx -= 1

        return (
            0 <= nx < self.field_size[0]
            and 0 <= ny < self.field_size[1]
            and (nx, ny) not in self.snake_poses[1:]
        )

    def move_snakepart(self, direction: int, snake_idx: int):
        x, y = self.snake_poses[snake_idx]
        nx, ny = x, y

        if direction == 0:
            ny -= 1
        elif direction == 1:
            nx += 1
        elif direction == 2:
            ny += 1
        elif direction == 3:
            nx -= 1
        else:
            raise Exception

        if snake_idx == 0:
            self.field[ny][nx] = self.snake_heads[direction]
            self.field_directions[x, y] = direction
        else:
            self.field[ny][nx] = self.snake_field

        self.snake_poses[snake_idx] = (nx, ny)
        self.field[y][x] = self.empty_field

    def move_snake(self, direction: int):
        for i, pos in enumerate(self.snake_poses):
            if i == len(self.snake_poses) - 1:
                self.snake_spawn = pos
            if i == 0:
                self.move_snakepart(direction, 0)
                continue
            self.move_snakepart(self.field_directions[pos], i)

    def grow_snake(self):
        self.snake_poses.append(self.snake_spawn)

    def eat_apple(self):
        self.apple_pos = self.spawn_apple()
        self.grow_snake()
        self.score += 1

    def end_game(self):
        self.run = False
        print(f"Score: {self.score}")
        exit()

    def tick(self):

        self.print()
        self.wait_for_start()

        while self.run:

            if not self.check_head():
                self.end_game()

            self.move_snake(self.direction)
            self.print()

            if self.snake_poses[0] == self.apple_pos:
                self.eat_apple()

            time.sleep(self.update_delay)

    def start(self):
        self.tick()


if __name__ == "__main__":
    sg = SnakeGame()
    sg.start()
