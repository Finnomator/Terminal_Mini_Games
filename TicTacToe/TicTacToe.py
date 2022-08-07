class TicTacToeRules:
    empty_field = " "
    player_field = "X"
    opponent_field = "O"


class TicTacToe(TicTacToeRules):

    STOP = "\x1B[0m"
    BLUE = "\u001b[34m"
    RED = "\u001b[31m"
    GRAY = "\u001b[38;2;90;90;90m"
    MOVE_CURSOR_UP = "\033[A"
    __printed = False
    empty_field_to_print = list(
        """\
     |     |
  E  |  E  |  E 
     |     |
-----------------
     |     |
  E  |  E  |  E 
     |     |
-----------------
     |     |
  E  |  E  |  E 
     |     |\
"""
    )

    def __init__(self, opponent: str = None) -> None:
        self.field = [self.empty_field for _ in range(9)]
        self.opponent_names = ["Player 2", "Computer"]
        self.player_name = "Player 1"
        if opponent is None:
            self.opponent_name = self.select_opponent()
        elif opponent in self.opponent_names:
            self.opponent_name = opponent
        else:
            raise Exception
        self.player_map = {
            self.player_name: self.player_field,
            self.opponent_name: self.opponent_field,
        }
        self.player_names = list(self.player_map.keys())

        if self.opponent_name == "Computer":
            self.tttBot = TicTacToeBot()

    def __str__(self) -> str:
        out = ""

        empty_field = self.empty_field_to_print.copy()

        base_idx = 0

        for i, field in enumerate(self.field):

            if field == self.player_field:
                field = self.RED + field + self.STOP
            elif field == self.opponent_field:
                field = self.BLUE + field + self.STOP
            else:
                field = str(i + 1)

            x, y = i % 3, i // 3

            if x == 0:
                if y == 0:
                    base_idx = 15
                elif y == 1:
                    base_idx = 76
                elif y == 2:
                    base_idx = 137
            else:
                base_idx += 6

            if base_idx != 0:
                empty_field[base_idx] = field

        out = "".join(empty_field)

        return out

    def print(self):

        if self.__printed:
            print(end=self.MOVE_CURSOR_UP * (self.empty_field_to_print.count("\n") + 3))
        else:
            print()

        print(str(self) + "\n")
        self.__printed = True

    def get_valid_input(
        self,
        prompt: str,
        typ: type,
        max_val: int = None,
        min_val: int = None,
        *type_args,
    ):
        inp = input(prompt + (" \b" if self.__printed else ""))
        while True:
            try:
                typ_inp = typ(inp, *type_args)

                if max_val is not None and type(typ_inp) == int and typ_inp > max_val:
                    raise ValueError

                if min_val is not None and type(typ_inp) == int and typ_inp < min_val:
                    raise ValueError

            except ValueError:
                print(end=f"{self.MOVE_CURSOR_UP}")
                inp = input(f"{prompt}{' ' * len(inp)}" + "\b" * len(inp))
            else:
                break
        return typ_inp

    def select_opponent(self):
        for i, op in enumerate(self.opponent_names):
            print(f"{i+1}. {op}")
        return self.opponent_names[
            self.get_valid_input("Select opponent: ", int, len(self.opponent_names), 1)
            - 1
        ]

    def player_move(self, player_name):

        if player_name != "Computer":
            while True:
                selected_field = (
                    self.get_valid_input(
                        f"{self.RED if player_name == self.player_name else self.BLUE}{player_name}s move: {self.STOP}",
                        int,
                        9,
                        1,
                    )
                    - 1
                )
                if self.field[selected_field] == self.empty_field:
                    break
                print(end=self.MOVE_CURSOR_UP)
        else:
            self.tttBot.set_field(self.field)
            selected_field = self.tttBot.find_best_move(self.field)
            print()

        self.field[selected_field] = self.player_map[player_name]

    def check_field(self):
        for player in self.player_names:
            player_field = self.player_map[player]

            if [player_field] * 3 in (self.field[:3], self.field[3:6], self.field[6:9]):
                return player

            for i in range(3):
                if (
                    self.field[i]
                    == self.field[i + 3]
                    == self.field[i + 6]
                    == player_field
                ):
                    return player

            if self.field[0] == self.field[4] == self.field[8] == player_field:
                return player

            if self.field[2] == self.field[4] == self.field[6] == player_field:
                return player

    def end_game(self, winner_name: str = None):
        print("\n")
        if winner_name is not None:
            print(f"{winner_name} won!")
        else:
            print("Draw!")
        exit()

    def mainloop(self):
        self.print()
        for i in range(9):
            self.player_move(self.player_names[i % 2])
            self.print()
            if (winner := self.check_field()) is not None:
                self.end_game(winner)
        self.end_game(self.check_field())

    def start(self):
        self.mainloop()


class TicTacToeBot(TicTacToeRules):
    def __init__(self) -> None:
        self.ttt = TicTacToe("Player 2")
        self.com_wins = 0
        self.player_wins = 0
        self.draws = 0

    def set_field(self, field: list):
        self.ttt.field = field

    def generate_all_possibilities(self, field, is_player_move=True):

        possible_poses = {}

        self.ttt.field = field

        if (winner := self.ttt.check_field()) is not None:
            if winner == "Player 1":
                self.player_wins += 1
            else:
                self.com_wins += 1
            return winner
        elif " " not in field:
            self.draws += 1
            return "Draw"

        for i in range(9):

            if field[i] != self.empty_field:
                continue

            field[i] = self.player_field if is_player_move else self.opponent_field

            possible_poses[i] = self.generate_all_possibilities(
                field, not is_player_move
            )

            field[i] = self.empty_field

        return possible_poses

    def find_best_move(self, field: list) -> int:

        moves_map = {}

        for i in range(9):

            if field[i] != self.empty_field:
                continue

            field[i] = self.opponent_field

            self.ttt.field = field

            if self.ttt.check_field() is not None:
                return i

            field[i] = self.empty_field

        for i in range(9):

            if field[i] != self.empty_field:
                continue

            field[i] = self.player_field

            self.ttt.field = field

            if self.ttt.check_field() is not None:
                return i

            field[i] = self.empty_field

        for i in range(9):

            if field[i] != self.empty_field:
                continue

            field[i] = self.opponent_field

            self.com_wins = 0
            self.player_wins = 0
            self.draws = 0

            self.generate_all_possibilities(field)

            moves_map[i] = (self.player_wins, self.com_wins, self.draws)

            field[i] = self.empty_field

        # move_with_most_wins = max(moves_map, key=lambda x: moves_map[x][1])
        # move_with_least_losses = min(moves_map, key=lambda x: moves_map[x][0])
        # move_with_most_draws = max(moves_map, key=lambda x: moves_map[x][2])
        best_move = max(
            moves_map,
            key=lambda x: -moves_map[x][0] + moves_map[x][0] + moves_map[x][2],
        )

        return best_move


if __name__ == "__main__":
    t = TicTacToe()
    t.start()
