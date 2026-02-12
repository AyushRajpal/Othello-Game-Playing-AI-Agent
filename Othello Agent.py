def read_input_file(file_path):

    input_file = open(file_path)
    player = input_file.readline().strip()
    your_time, opponents_time = input_file.readline().strip().split(' ')

    game_board = []

    for idx in range(12):
        game_board.append(list(input_file.readline().strip()))

    return player, your_time, opponents_time, game_board

def is_valid_move(board, i, j, player, directions):
    opponent = 'O' if player == 'X' else 'X'
    for dx, dy in directions:
        x, y = i + dx, j + dy
        if not (0 <= x < 12 and 0 <= y < 12 and board[x][y] == opponent):
            continue  # Not adjacent to an opponent's piece or out of bounds

        # Move in the direction while it's the opponent's piece
        while 0 <= x < 12 and 0 <= y < 12 and board[x][y] == opponent:
            x += dx
            y += dy

        # Check if we ended up in a valid position
        if 0 <= x < 12 and 0 <= y < 12 and board[x][y] == player and (x - dx != i or y - dy != j):
            return True
    return False


def find_valid_moves(board, player):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    valid_moves = []

    for i in range(12):
        for j in range(12):
            if board[i][j] == '.' and is_valid_move(board, i, j, player, directions):
                valid_moves.append((i, j))

    return valid_moves

def heuristic_evaluation(board, player):
    opponent = 'O' if player == 'X' else 'X'
    player_tiles = 0
    opponent_tiles = 0

    for row in board:
        for tile in row:
            if tile == player:
                player_tiles += 1
            elif tile == opponent:
                opponent_tiles += 1


    # Assuming 'board' is the current board state and 'player' is the current player
    stability_score = edge_stability_heuristic(board, player)

    # print(player_tiles, opponent_tiles, stability_score)

    return player_tiles - opponent_tiles + stability_score

def is_stable_disc(board, x, y, player):
    if board[x][y] != player:
        return False  # The disc is not the player's disc

    # Check if the disc is in the corner
    if (x == 0 or x == len(board) - 1) and (y == 0 or y == len(board[0]) - 1):
        return True

    # Check if the disc is on an edge and has a line of the same color discs ending in a corner
    if x == 0 or x == len(board) - 1:  # Top or bottom edge
        if board[0][y] == player and board[len(board) - 1][y] == player:
            return True
    if y == 0 or y == len(board[0]) - 1:  # Left or right edge
        if board[x][0] == player and board[x][len(board[0]) - 1] == player:
            return True

    # Check rows and columns for stability
    row_stable = all(board[i][y] == player for i in range(len(board)))
    col_stable = all(board[x][j] == player for j in range(len(board[0])))

    return row_stable or col_stable


def edge_stability_heuristic(board, player):
    opponent = 'O' if player == 'X' else 'X'
    stability_score = 0
    board_size = len(board)
    edge_indices = [0, board_size - 1]

    # Combine top/bottom and left/right edges into one loop for simplicity
    for edge in edge_indices:
        # Check top and bottom edges
        for y in range(board_size):
            stability_score += evaluate_stability(board, edge, y, player, opponent)
            stability_score += evaluate_stability(board, y, edge, player, opponent, False)

    return stability_score

def evaluate_stability(board, x, y, player, opponent, is_row=True):
    """Helper function to evaluate stability of a disc at a given position"""
    if is_row:
        if board[x][y] == player:
            return 1
        elif board[x][y] == opponent:
            return -1
    else:
        if board[y][x] == player:
            return 1
        elif board[y][x] == opponent:
            return -1
    return 0

def minimax(board, depth, alpha, beta, maximizingPlayer, player):
    if depth == 0 or (find_valid_moves(board, 'X') or find_valid_moves(board, 'O')):
        return heuristic_evaluation(board, player)

    valid_moves = find_valid_moves(board, player if maximizingPlayer else 'O' if player == 'X' else 'X')

    if not valid_moves:
        return heuristic_evaluation(board, player)

    if maximizingPlayer:
        maxEval = float('-inf')
        for move in valid_moves:
            new_board = make_move(board, move, player)
            eval = minimax(new_board, depth - 1, alpha, beta, False, player)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for move in valid_moves:
            new_board = make_move(board, move, 'O' if player == 'X' else 'X')
            eval = minimax(new_board, depth - 1, alpha, beta, True, player)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def make_move(board, move, player):
    new_board = [row.copy() for row in board]  # More concise deep copy
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    opponent = 'O' if player == 'X' else 'X'
    x, y = move
    new_board[x][y] = player  # Place the player's piece

    # Helper function to check if a position is within the board bounds
    def is_within_board(x, y):
        return 0 <= x < len(new_board) and 0 <= y < len(new_board[0])

    # Helper function to flip pieces in a valid direction
    def flip_pieces_in_direction(dx, dy):
        nx, ny = x + dx, y + dy
        pieces_to_flip = []

        # Collect pieces to flip
        while is_within_board(nx, ny) and new_board[nx][ny] == opponent:
            pieces_to_flip.append((nx, ny))
            nx += dx
            ny += dy

        # Flip pieces if the line ends with a player's piece
        if is_within_board(nx, ny) and new_board[nx][ny] == player:
            for px, py in pieces_to_flip:
                new_board[px][py] = player

    # Check each direction for opponent pieces to flip
    for dx, dy in directions:
        flip_pieces_in_direction(dx, dy)

    return new_board

def choose_best_move_minimax(board, player, depth):
    valid_moves = find_valid_moves(board, player)
    best_move = max(valid_moves, key=lambda move: minimax(make_move(board, move, player), depth, float('-inf'), float('inf'), False, player), default=None)

    if best_move:
        col_no = chr(ord('a') + best_move[1])
        row_no = best_move[0] + 1
        return f"{col_no}{row_no}"
    return 'No move found'

input_data_path = 'input.txt'

my_move, my_time, opp_time, board_state = read_input_file(input_data_path)

my_time = float(my_time)

if my_time>299:depth=2
elif my_time>210:depth=5
elif my_time>165:depth=4
else:depth=3

next_move = choose_best_move_minimax(board_state, my_move, depth)
# print(next_move)

f = open('output.txt', 'w')
f.write(next_move+'\n')
f.close()