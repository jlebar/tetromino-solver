import sys

tile_map = {
  'i': ((0, 0), (0, 1), (0, 2), (0, 3)),
  'o': ((0, 0), (0, 1), (1, 0), (1, 1)),
  't': ((0, 0), (1, 0), (2, 0), (1, 1)),
  'j': ((0, 0), (1, 0), (1, 1), (1, 2)),
  'l': ((0, 0), (1, 0), (0, 1), (0, 2)),
  's': ((0, 0), (1, 0), (1, 1), (2, 1)),
  'z': ((0, 0), (0, 1), (1, 1), (1, 2)),
}

def rotate_90(rot):
    return tuple((-y, x) for (x, y) in rot)

rotations_map = {}
for tile in tile_map.keys():
    rot = tile_map[tile]
    rotations = set()
    for i in range(4):
        rotations.add(rot)
        rot = rotate_90(rot)
    rotations_map[tile] = rotations

def piece_fits(board, x, y, rot):
    for coord in rot:
        try:
            xc = x + coord[0]
            yc = y + coord[1]
            if xc < 0 or yc < 0 or board[xc][yc] != '':
                return False
        except IndexError:
            return False
    return True

def set_board(board, x, y, rot, val):
    for coord in rot:
        if board[x + coord[0]][y + coord[1]] == val:
            print_board(board)
            raise Exception('Unexpected value in board at (%d, %d).  '
                            'Expected anything other than %s.' %
                            (x + coord[0], y + coord[1], val))
        board[x + coord[0]][y + coord[1]] = val

def print_board(board):
    for y in range(len(board[0])):
        for x in range(len(board)):
            print board[x][y],
        print

def solve(width, height, tiles):
    """
    >>> solve(2, 2, ['o'])
    o o
    o o

    >>> solve(2, 2, ['j'])
    No solution

    >>> solve(2, 4, ['o', 'o'])
    o o
    o o
    o o
    o o

    >>> solve(2, 4, ['l', 'l'])
    l l
    l l
    l l
    l l

    >>> solve(6, 2, ['o', 'l', 'l'])
    o o l l l l
    o o l l l l

    >>> solve(8, 4, ['l', 'l', 'j', 'j', 't', 't', 't', 't'])
    l l j j t t t t
    l l j j t t t t
    l l j j t t t t
    l l j j t t t t

    #>>> solve(5, 8, ['l', 'o', 's', 't', 't', 'i', 'i', 'o', 'l', 's'])

    """
    board = [['' for h in range(height)] for w in range(width)]
    if not solve_recursive(board, tiles):
        print 'No solution'
    else:
        print_board(board)

def solve_recursive(board, tiles):
    """
    >>> solve_recursive([['', ''], ['', '']], ['o'])
    True
    """
    if not tiles:
        return True
    tile = tiles[0]
    for x in range(len(board)):
        for y in range(len(board[x])):
            # Try all rotations of the current tile.
            for rot in rotations_map[tile]:
                if piece_fits(board, x, y, rot):
                    set_board(board, x, y, rot, tile)
                    if solve_recursive(board, tiles[1:]):
                        return True
                    set_board(board, x, y, rot, '')
    return False

if __name__ == '__main__':
    import doctest
    doctest.testmod()
