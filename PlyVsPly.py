import motor

def launch_game():
    connect4 = motor.Connect4()
    while connect4.win == 0:
        connect4.play(int(input("play: ")))
    print("Game End")
    input()
    connect4.close_game()
