from __future__ import annotations


def generator_number() -> int:
    n = 1
    while True:
        yield n
        n += 1

class Element:
    def __init__(self, value: int, prev: Element, next: Element):
        self._value: int = value
        self._prev: Element = prev
        self._next: Element = next

    def add_after(self, value: int) -> None:
        next_tmp = self._next
        self._next = Element(value, self, next_tmp)
        if next_tmp is not None:
            next_tmp._prev = self._next

    def add_before(self, value: int) -> None:
        prev_tmp = self._prev
        self._prev = Element(value, prev_tmp, self)
        if prev_tmp is not None:
            prev_tmp._next = self._prev

    def __repr__(self) -> str:
        if self._prev == None:
            previous = "[x]"
        else:
            previous = self._prev._value
        
        if self._next == None:
            next = "[x]"
        else:
            next = self._next._value
        return f'{previous}--{self._value}--{next}'


class LinkedList:
    # hardcoded for two-element init list
    def __init__(self, init: list):
        self.length: int = len(init)
        # self.cursor: int = len(init)
        first = Element(init[0], None, None)
        last  = Element(init[1], first, None)
        first._next = last
        self.first: Element = first
        self.last: Element = last

    def append(self, value):
        self.last.add_after(value)
        self.last = self.last._next
        self.length += 1

    def __iterate_to_position(self, position: int) -> Element:
        iterated: Element = self.first
        cnt = 0
        while (cnt != position):
            cnt += 1
            iterated = iterated._next
            if iterated is None:
                raise IndexError("premature end of list")

        return iterated

    def insert(self, position: int, value: int):
        if position < 0:
            raise IndexError("position is negative")
        if position > self.length:
            raise IndexError("position is longer than the list size")
        if position == self.length:
            self.append(value)
            return
        
        iterated: Element = self.__iterate_to_position(position)
        iterated.add_before(value)
        if position == 0:
            self.first = self.first._prev
        self.length += 1

    def pop(self, position: int | None) -> int:
        if position < 0:
            raise IndexError("position is negative")
        if position > self.length:
            raise IndexError("position is longer than the list size")

        removed: Element = self.__iterate_to_position(position)
        if removed._prev is not None:
            removed._prev._next = removed._next     # (prev)--[xxx]-->(next)
        else:
            self.first = removed._next              # [xxx]--(new-first)

        if removed._next is not None:
            removed._next._prev = removed._prev     # (prev)<--[xxx]--(next)
        else:
            self.last = removed._prev               # (new-last)--[xxx]

        self.length -= 1
        removed._next = None
        removed._prev = None
        return removed._value


    def __repr__(self) -> str:
        iterated: Element = self.first
        out = f'[{iterated._value}, '
        # print(out)
        while iterated._next is not None:
            iterated = iterated._next
            out += f'{iterated._value}, '
            # print(out)
        return f'{out[0:-2]}]'


class Marbles:
    def __init__(self, max_players: int):
        # self._marbles: list = [0, 1]
        self._marbles: LinkedList = LinkedList([0, 1])
        self._position: int = 1
        self._player: int = 1
        self._max_players: int = max_players

    def special_operation(self) -> int:
        if self._position >= 7:
            new_index = self._position - 7
        else:
            # new_index = self._position - 7 + len(self._marbles)
            new_index = self._position - 7 + self._marbles.length
        
        removed = self._marbles.pop(new_index)

        if self._position == 6:
            new_index = 0
        self._position = new_index

        self.next_player()
        return removed

    def add_marble(self, marble: int):
        # position at last element
        # if self._position + 1 == len(self._marbles):
        if self._position + 1 == self._marbles.length:
            self._marbles.insert(1, marble)
            self._position = 1
        # position at pre-last element
        # elif self._position + 2 == len(self._marbles):
        elif self._position + 2 == self._marbles.length:
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
    # Nplayers = 423
    # last_marble_value = 71944  # AKA last marble's worthness (slightly confusing)
    Nplayers = 30
    last_marble_value = 5807  # AKA last marble's worthness (slightly confusing)
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