import random
import re
import time

from display import Display

# board states
MINE = 'M'
EMPTY = 0

# player states
UNDISCOVERED = 'u'
FLAG = 'F'

class Game:
    def __init__(self, n, m, mineCount):
        self.n, self.m, self.mineCount = n, m, mineCount

        self.board = [[EMPTY for _ in xrange(n)] for _ in xrange(m)]
        self.view = [[UNDISCOVERED for _ in xrange(n)] for _ in xrange(m)]

        self.display = Display(self.board, self.view)

        self.revealedCount = 0
        self.gameOver = False

    def start(self):
        self.initialize()
        while not self.gameOver:
            self.input()
            self.update()
            self.display.display()
        if self.revealedCount == self.n * self.m - self.mineCount:
            print 'Game Over! You win!'
        else:
            print 'Game Over! You blew up!'

    def initialize(self):
        self._generateTopography()

    def update(self):
        if self.revealedCount == self.n * self.m - self.mineCount:
            self.gameOver = True

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
            r, c = (int(x) for x in f.groups())
            self.doFlag(r, c)
        elif p:
            r, c = (int(x) for x in p.groups())
            self.doPlay(r, c)
        elif e:
            r, c = (int(x) for x in e.groups())
            self.doExpand(r, c)
        elif ee:
            self.doEnd()

    def _generateTopography(self):
        indices = range(self.n * self.m)
        random.shuffle(indices)
        mineLocations = map(
            lambda x: (x // self.n, x % self.n),
            indices[:self.mineCount])
        for r, c in mineLocations:
            self.board[r][c] = MINE
            # update topography around mine
            for r2, c2 in self._neighbors(r, c):
                if self.board[r2][c2] is MINE:
                    continue
                self.board[r2][c2] += 1

    def _inBounds(self, r, c):
        return 0 <= r < self.n and 0 <= c < self.m

    def _neighbors(self, r, c):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                elif not self._inBounds(r + i, c + j):
                    continue
                yield r + i, c + j

    # === PLAYER ACTIONS ===

    def doFlag(self, r, c):
        if self.view[r][c] is UNDISCOVERED:
            self.view[r][c] = FLAG

    def doPlay(self, r, c):
        self._reveal(r, c)

    def doExpand(self, r, c):
        '''
        1. Check the number of mines and flags around this square and compare
        with the number on this square. If match, reveal this square.
        '''
        if self.view[r][c] is UNDISCOVERED:
            return
        flagCount = sum(
            self.view[r2][c2] is FLAG for r2, c2 in self._neighbors(r, c))
        if flagCount == self.view[r][c]:
            for r2, c2 in self._neighbors(r, c):
                self._reveal(r2, c2)

    def _reveal(self, r, c):
        '''
        "Reveal" is used both for the player "play" action and the "expand"
        action. It's algorithm is as follows:

        1. Shows the number on this square.
        2. If bomb, you die.
        3. If 0, recursively reveal surrounding squares.
        '''
        if self.view[r][c] is not UNDISCOVERED:
            return
        value = self.board[r][c]
        self.view[r][c] = value
        if value is MINE:
            self.gameOver = True
            return
        self.revealedCount += 1
        if value is EMPTY:
            for r2, c2 in self._neighbors(r, c):
                self._reveal(r2, c2)

    def doEnd(self):
        self.gameOver = True

if __name__ == '__main__':
    game = Game(10, 10, 10)
    game.start()
