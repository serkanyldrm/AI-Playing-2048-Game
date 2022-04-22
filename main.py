import Game

is_game_over = ''
game_start_board = Game.game()
print(game_start_board)
total_score = 0
chosen = Game.monte_carlo(5, game_start_board, 10)
game_board, score = chosen(game_start_board)
status = Game.game_over(game_board)
print(status)
if(status == 'GAME NOT OVER, Empty'):
        Game.new_2_board(game_board)
else:
    exit()
while (True):
    for i in range(4):
        for j in range(4):
            print(game_board[i][j], end=" ")
        print()
    chosen = Game.monte_carlo(5, game_board, 1000)
    game_board, score = chosen(game_board)
    total_score += score
    print(total_score)
    status = Game.game_over(game_board)
    print(chosen)
    print(status)
    if(status == 'GAME NOT OVER, Empty'):
        Game.new_2_board(game_board)
    elif(status == 'GAME NOT OVER'):
        continue
    else:
        break




