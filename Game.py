import random
import numpy as np

#game fonksiyonu oyunu başlatıp rastgele 2 adet 2 sayısı ekler.
def game():

    board = []
    for i in range(4):
        board.append([0] * 4)
    new_2_board(board)
    new_2_board(board)

    return board

#bu fonksiyon oyuna rastgele bir noktaya 2 ekler. Diğer fonksiyonlar tarafından çağırılır.
def new_2_board(board):

    row = random.randint(0, 3)
    column = random.randint(0, 3)

    while(board[row][column] != 0):

        row = random.randint(0,3)
        column = random.randint(0,3)

    board[row][column] = 2


#bu fonksiyon oyunun bitip bitmediğini kontrol eder.
def game_over(board):
    for i in range(4):
        for j in range(4):
            if (board[i][j] == 2048):
                return 'WON'


    for i in range(4):
        for j in range(4):
            if (board[i][j] == 0):
                return 'GAME NOT OVER, Empty'

    for i in range(3):
        for j in range(3):
            if (board[i][j] == board[i + 1][j] or board[i][j] == board[i][j + 1]):
                return 'GAME NOT OVER'
    for j in range(3):
        if (board[3][j] == board[3][j + 1]):
            return 'GAME NOT OVER'

    for i in range(3):
        if (board[i][3] == board[i + 1][3]):
            return 'GAME NOT OVER'

    return 'LOST'
# bu fonksiyon oyunu 4 yönden hangi yön seçildiyse o tarafa doğru kaydırır.
def new_board_compressed(board):

    new_board = []
    for j in range(4):
        partial_new = []
        for i in range(4):
            partial_new.append(0)
        new_board.append(partial_new)

    for i in range(4):
        pos = 0
        for j in range(4):
            if board[i][j] != 0:
                new_board[i][pos] = board[i][j]

                pos += 1

    return new_board
#bu fonksiyon herhangi bir yöne kaydırılmış oyunda yan yana iki aynı sayı varsa toplar ve birleştirir
def merge(board):
    score = 0
    for i in range(4):
        for j in range(3):
            if (board[i][j] == board[i][j + 1] and board[i][j] != 0):
                board[i][j] = board[i][j] * 2
                board [i][j+1] = 0
                score = board[i][j]


    return board, score
#aşağıdaki iki fonksiyon 4 yönden 3 ünü diğer yöne benzetmek için matrisi rotate etmede kullanılır.
def reverse(board):
    new_board = []
    for i in range(4):
        new_board.append([])
        for j in range(4):
            new_board[i].append(board[i][3-j])
    return new_board

def transpose(board):
    new_board = []
    for i in range(4):
        new_board.append([])
        for j in range(4):
            new_board[i].append(board[j][i])
    return new_board
#sol yön seçildiği zaman çağırılır.
def left(game_board):

    new_game_board_compressed_1 = new_board_compressed(game_board)
    new_game_board_merged, score = merge(new_game_board_compressed_1)
    new_game_board_compressed_2 = new_board_compressed(new_game_board_merged)
    for i in range(4):
        for j in range(4):
            if (new_game_board_compressed_2[i][j] != new_game_board_compressed_1[i][j]):
                return new_game_board_compressed_2,score
    return new_game_board_compressed_2,0

#sağ yön seçildiği zaman çağırılır
def right(game_board):

    new_game_board = reverse(game_board)
    new_game_board, score = left(new_game_board)
    new_game_board = reverse(new_game_board)

    return new_game_board, score
#yukarı yönü seçildiği zaman çağırılır
def up(game_board):

    new_game_board = transpose(game_board)
    new_game_board, score = left(new_game_board)
    new_game_board = transpose(new_game_board)

    return new_game_board, score
#aşağı yönü seçildiği zaman çağırılır
def down(game_board):

    new_game_board = transpose(game_board)
    new_game_board, score = right(new_game_board)
    new_game_board = transpose(new_game_board)

    return new_game_board,score
#bu fonksiyon monte carlo tree nin oluşturulduğu fonksiyondur. Her bir yön için oyun sonuna kadar random bir şekilde oynar. Seçileb simulation_number değişkeni kadar oynayıp toplam score'u en yüksek yönü seçer
def monte_carlo(deep,state,simulation_number):

    first_moves = [left,right,up,down]
    scores = np.zeros(4)

    for first_index in range(4):
        different = False
        first_move = first_moves[first_index]
        new_state, score = first_move(state)
        is_game_over = game_over(new_state)
        for i in range(4):
            for j in range(4):
                if (state[i][j] != new_state[i][j]):
                    different = True
        if different is True:
            for i in range(simulation_number):
                    move_number = 1
                    copy_state = np.copy(new_state)
                    while (is_game_over == 'GAME NOT OVER, Empty' and move_number <= deep):
                        is_game_over = game_over(copy_state)
                        if is_game_over == 'GAME NOT OVER, Empty':
                            new_2_board(copy_state)
                        index = random.randint(0,3)

                        move = first_moves[index]
                        copy_state, score = move(copy_state)
                        if score != 0:
                            scores[first_index] += score
                        move_number += 1
                    while (is_game_over == 'GAME NOT OVER' and move_number <= deep):
                        is_game_over = game_over(copy_state)
                        index = random.randint(0,3)
                        move = first_moves[index]
                        copy_state, score = move(copy_state)
                        if score != 0:
                            scores[first_index] += score
                        move_number += 1

    choose = np.argmax(scores)
    result = np.all((choose==0.))
    if result:
        chosen = first_moves[3]
    chosen = first_moves[choose]
    print(scores)
    return chosen




