import motor
import numpy as np
import tensorflow as tf

def LancheGame():
    model=tf.keras.models.load_model("Connect4Model")
    connect4 = motor.Connect4()
    while connect4.win == 0:
        if connect4.plyTurn == -1:
            connect4.Play(int(input("play: ")))
        else:
            observations = connect4.Observation() * connect4.plyTurn
            valeurs_q=model(np.expand_dims(observations, axis=0))
            action=int(tf.argmax(valeurs_q[0], axis=-1))
            connect4.Play(action)
    print("Game End")
    input()
    connect4.CloseGame()





    