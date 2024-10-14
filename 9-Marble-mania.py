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

class LinkedListIterator:
    ''' Iterator class '''
    def __init__(self, linkedList: LinkedList):
        self._linkedList = linkedList
        self._index = 0

    def __next__(self):
        ''''Returns the next value from the linked list '''
        if self._index == self._linkedList.length:
            raise StopIteration
        
        tmp: Element = self._linkedList.first
        for _ in range(self._index):
            tmp = tmp._next
        self._index += 1
        return tmp._value

class LinkedList:
    # hardcoded for two-element init list
    def __init__(self, init: list):
        self.length: int = len(init)
        self.cursor: int = 1
        first = Element(init[0], None, None)
        last  = Element(init[1], first, None)
        first._next = last
        self.first: Element = first
        self.last: Element = last
        self.current: Element = last

    def append(self, value):
        self.last.add_after(value)
        self.last = self.last._next
        self.length += 1
        
    def place_at_pos_1(self, value: int):
        self.first.add_after(value)
        self.length += 1

    def __iterate_to_position(self, position: int) -> Element:
        steps_relative = position - self.cursor
        iterated: Element = self.current
        for _ in range(abs(steps_relative)):
            iterated = iterated._next if steps_relative > 0 else iterated._prev
            if iterated is None:
                raise IndexError("premature end of list")

        return iterated
    
    def advance(self, steps_relative: int) -> None:
        if self.cursor + steps_relative >= self.length:
            raise IndexError("Cursor to be placed after the end of the list")
        if self.cursor + steps_relative < 0:
            raise IndexError("Cursor to be placed before the beginning of the list")
        
        tmp: Element = self.current
        for _ in range(abs(steps_relative)):
            tmp = tmp._next if steps_relative > 0 else tmp._prev
        
        self.current = tmp
        self.cursor += steps_relative
        
    def reset_cursor(self, *, offset: int = 0):
        tmp: Element = self.first
        for _ in range(offset):
            tmp = tmp._next
        
        self.current = tmp
        self.cursor = offset

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
    
    def at(self, position: int) -> Element:
        tmp: Element = self.first
        for _ in range(position):
            tmp = tmp._next
        return tmp
    
    def debug_cursor(self) -> bool:
        if self.at(self.cursor)._value == self.current._value:
            return True
        else: return False

    def __repr__(self) -> str:
        iterated: Element = self.first
        out = f'[{iterated._value}, '
        # print(out)
        while iterated._next is not None:
            iterated = iterated._next
            out += f'{iterated._value}, '
            # print(out)
        return f'{out[0:-2]}]'

    def __iter__(self):
        return LinkedListIterator(self)

class Marbles:
    def __init__(self, max_players: int):
        self._marbles: LinkedList = LinkedList([0, 1])
        self._player: int = 1
        self._max_players: int = max_players
        
    def special_operation(self) -> int:
        if self.position() >= 7:
            # deletion on the left of the cursor
            new_index = -7
            removed = self._marbles.pop(self.position() + new_index)
            self._marbles.advance(new_index+1)
            self._marbles.cursor -= 1
        else:
            # deletion on the right of the cursor
            # ...implying a jump from marbles[0] to marbles[end] - can be improved by iterating from marbles.last backwards in much fewer steps
            new_index = -7 + self._marbles.length
            removed = self._marbles.pop(self.position() + new_index)
            if self.position() == 6:
                self._marbles.reset_cursor()
            else:
                self._marbles.advance(new_index)

        self.next_player()
        return removed
    
    
    def add_marble(self, marble: int):
        # position at last element
        if self.position() + 1 == self._marbles.length:
            self._marbles.place_at_pos_1(marble)
            self._marbles.reset_cursor(offset=1)
        else:
            self._marbles.insert(self.position() + 2, marble)
            self._marbles.advance(2)
        
        self.next_player()


    def get_player(self): return self._player
    
    def position(self): return self._marbles.cursor
    
    def next_player(self) -> None:
        next_player_index =  self._player+1 if self._player < self._max_players else 1
        self._player = next_player_index

    def __repr__(self) -> str:
        marbles_marked = [f'({val})' if it == self.position() else str(val) for (it,val) in enumerate(self._marbles)]
        return f'[{next(turn)}/{self._player}] [' + ' '.join(marbles_marked) + ']'
        

if __name__ == "__main__":
    Nplayers = 423
    last_marble_value = 7194400  # AKA last marble's worthness (slightly confusing)
    Nplayers = 30
    last_marble_value = 5807
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