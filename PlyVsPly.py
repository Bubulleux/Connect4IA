import motor

def LancheGame():
    connect4 = motor.Connect4()
    while connect4.win == 0:
        connect4.Play(int(input("play: ")))
    print("Game End")
    input()
    connect4.CloseGame()
