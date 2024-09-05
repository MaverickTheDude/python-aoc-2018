def generator_number() -> int:
    n = 1
    while True:
        yield n
        n += 1

class Marbles:
    def __init__(self, max_players: int) -> None:
        self._marbles: list = [0, 1]
        self._position: int = 1
        self._player: int = 1
        self._max_players: int = max_players

    def special_operation(self) -> int:
        if self._position >= 7:
            new_index = self._position - 7
        else:
            new_index = self._position - 7 + len(self._marbles)
        
        removed = self._marbles.pop(new_index)

        if self._position == 6:
            new_index = 0
        self._position = new_index

        self.next_player()
        return removed

    def add_marble(self, marble: int):
        # position at last element
        if self._position + 1 == len(self._marbles):
            self._marbles.insert(1, marble)
            self._position = 1
        # position at pre-last element
        elif self._position + 2 == len(self._marbles):
            self._marbles.append(marble)
            self._position += 2
        else:
            self._marbles.insert(self._position + 2, marble)
            self._position += 2
        
        self.next_player()

    def get_player(self): return self._player

    def next_player(self) -> None:
        next_player_index =  self._player+1 if self._player < self._max_players else 1
        self._player = next_player_index

    def __repr__(self) -> str:
        marbles_marked = [f'({val})' if it == self._position else str(val) for (it,val) in enumerate(self._marbles)]
        return f'[{next(turn)}/{self._player}] [' + ' '.join(marbles_marked) + ']'
        

if __name__ == "__main__":
    Nplayers = 423
    last_marble_value = 71944  # AKA last marble's worthness (slightly confusing)
    turn = generator_number()
    players_score = dict()
    field = Marbles(Nplayers)

    for it in range(2, last_marble_value+2):
        # if it % 23 == 0 or it % 23 == 1:
        #     print(field)
        # else:
        #     next(turn)
        # print(field)

        if it % 23 == 0:
            points = field.special_operation() + it
            current_player = field.get_player()
            if current_player not in players_score:
                players_score[current_player] = points
            else:
                players_score[current_player] += points
        else:
            field.add_marble(it)

    best_score = max(zip(players_score.values(), players_score.keys())) # values before keys to prioritize max-value instead of key
    print(f'player {best_score[1]} got {best_score[0]} points')