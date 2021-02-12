import motor


def launch_game():
    connect4 = motor.Connect4()
    while connect4.win == 0:
        connect4.play(int(input("play: ")))
    print(f"{ 'Red' if connect4.win == -1 else 'Yellow' } Won")
    print("Game End")
    input()
    connect4.close_game()
