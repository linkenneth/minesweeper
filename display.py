class Display:
    '''
    Display.
    '''

    def __init__(self, board, view):
        self.board = board
        self.view = view
        self.n = len(board)
        self.m = len(board[0])

    def display(self):
        print ' ', ' '.join(str(i) for i in range(self.m))
        for r in range(self.n):
            print r, ' '.join(str(x) for x in self.view[r])
        # for r in range(self.n):
        #     print r, ' '.join(str(x) for x in self.board[r])
