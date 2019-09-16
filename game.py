'''
TODO:
-- implement board, player view and display of player view
-- implement game loop
-- initialize with mines
-- victory
-- fail
-- auto-expand
'''

import random
import re
import time

from display import Display

# board states
MINE = 'm'
EMPTY = 0

# player states
UNDISCOVERED = 'u'
FLAG = 'f'

class Game:
    def __init__(self, n, m, mineCount):
        self.n, self.m, self.mineCount = n, m, mineCount

        self.board = [[EMPTY for _ in xrange(n)] for _ in xrange(m)]
        self.view = [[UNDISCOVERED for _ in xrange(n)] for _ in xrange(m)]

        self.display = Display(self.board, self.view)

    def start(self):
        self.initialize()
        while not self.isOver():
            self.input()
            self.update()
            self.display.display()

    def initialize(self):
        self._generateTopography()

    def update(self):
        pass

    FLAG_RE = re.compile(r'^[fF][lag]*\s*(\d+)\s*,?\s*(\d+)\s*$')
    PLAY_RE = re.compile(r'^[pP][lay]*\s*(\d+)\s*,?\s*(\d+)\s*$')
    EXPAND_RE = re.compile(r'^[eE][xpand]*\s*(\d+)\s*,?\s*(\d+)\s*$')
    END_RE = re.compile(r'^[eE]nd')

    def input(self):
        '''
        Valid commands:
        -- f(lag) R, C: flags the square at (R, C) as a mine
        -- p(lay) R, C: blows the square at (R, C) open
        -- e(xpand) R, C: like left + right click, auto-expands squares around
           (R, C) if the number of flags around (R, C) equals the number at
           (R, C)
        '''
        command = raw_input()
        f = self.FLAG_RE.match(command)
        p = self.PLAY_RE.match(command)
        e = self.EXPAND_RE.match(command)
        ee = self.END_RE.match(command)

        if f:
            print 'flag'
        elif p:
            print 'play'
        elif e:
            print 'expand'
        elif ee:
            print 'end'

    def _generateTopography(self):
        indices = range(self.n * self.m)
        random.shuffle(indices)
        mineLocations = map(
            lambda x: (x // self.n, x % self.n),
            indices[:self.mineCount])
        for r, c in mineLocations:
            self.board[r][c] = MINE
            # update topography around mine
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == j == 0:
                        continue
                    elif not self._inBounds(r + i, c + j):
                        continue
                    elif self.board[r + i][c + j] is MINE:
                        continue
                    self.board[r + i][c + j] += 1

    def _inBounds(self, r, c):
        return 0 <= r < self.n and 0 <= c < self.m

    def isOver(self):
        return False

    # === PLAYER ACTIONS ===

    def doFlag(self, r, c):
        self.view[r][c] = FLAG

    def doPlay(self, r, c):
        '''
        1. Reveal the current square, if not revealed.
        2. If blow up, you lose.
        3. Otherwise, if is 0, run expand on the current square.
        '''
        visited = set()

    def doExpand(self, r, c):
        '''
        1. Check the number of mines and flags around this square and compare
        with the number on this square. If match, reveal this square.
        '''
        # 1. for each square around square, see if satisfy.
        # 1.5. if satisfy, "expand"
        #
        pass

    def _reveal(self, r, c):
        '''
        "Reveal" is used both for the player "play" action and the "expand"
        action. It's algorithm is as follows:

        1. Shows the number on this square.
        2. If bomb, you die.
        3. If 0, recursively reveal surrounding squares.
        '''
        value = self.board[r][c]
        if value is EMPTY:
            pass

        visited = set()

    def doEnd(self):
        pass

if __name__ == '__main__':
    game = Game(10, 10, 10)
    game.start()
