import motor
import tensorflow as tf
from tensorflow.keras import models, layers
import numpy as np
import time
import matplotlib.pyplot as plt

game : motor.Connect4= motor.Connect4(0)
#game._max_episode_steps=500
nbr_action=7

gamma=tf.constant(0.98)
epoch=20000
best_score=0

epsilon=1.
epsilon_min=0.10
start_epsilon=1
end_epsilon=epoch
epsilon_decay_value=epsilon/(end_epsilon-start_epsilon)

def GetModel():
  entree=layers.Input(shape=(42), dtype='float32')
  result=layers.Dense(50, activation='relu')(entree)
  result=layers.Dense(50, activation='relu')(result)
  result=layers.Dense(50, activation='relu')(result)
  sortie=layers.Dense(nbr_action)(result)
    
  model=models.Model(inputs=entree, outputs=sortie)
  return model

def my_loss(target_q, predicted_q):
  loss=tf.reduce_mean(tf.math.square(target_q-predicted_q))
  return loss

#@tf.function
def train_step(reward, action, observation, next_observation, done):
  next_Q_values=model(next_observation)
  best_next_actions=tf.math.argmax(next_Q_values, axis=1)
  next_mask=tf.one_hot(best_next_actions, nbr_action)
  next_best_Q_values=tf.reduce_sum(next_Q_values*next_mask, axis=1)
  target_Q_values=reward+(1-done)*gamma*next_best_Q_values
  target_Q_values=tf.reshape(target_Q_values, (-1, 1))
  mask=tf.one_hot(action, nbr_action)
  with tf.GradientTape() as tape:
    all_Q_values=model(observation)
    Q_values=tf.reduce_sum(all_Q_values*mask, axis=1, keepdims=True)
    loss=my_loss(target_Q_values, Q_values)
  gradients=tape.gradient(loss, model.trainable_variables)
  optimizer.apply_gradients(zip(gradients, model.trainable_variables))
  train_loss(loss)

def train(debug=False):
  global epsilon, best_score
  model=GetModel()
  train_loss=tf.keras.metrics.Mean()
  for e in range(epoch):
    score=0
    tab_observations=[[], []]
    tab_rewards=[[], []]
    tab_actions=[[], []]
    tab_next_observations=[[], []]
    tab_done=[[], []]
    if e % 100 == 0:
      print(f"e: {e}, epsilon: {epsilon}")
    game = motor.Connect4(showBoard= (e% 1000 == 0 and debug))
    observations = game.Observation()
    while True:
      if game.visualBoard != None:
        time.sleep(0.3)
      ply = (game.plyTurn + 1) // 2
      tab_observations[ply].append(observations)    
      if np.random.rand()>epsilon:
        valeurs_q=model(np.expand_dims(observations, axis=0))
        action=int(tf.argmax(valeurs_q[0], axis=-1))
      else:
        action=np.random.randint(0, nbr_action)
      observations, reward, done=game.Play(action)
      #print(f"done: {done}, reward {reward}, action {action}")
      observations *= game.plyTurn
      tab_actions[ply].append(action)
      tab_next_observations[ply].append(observations)
      tab_done[ply].append(done)
      score+=reward
      tab_rewards[ply].append(reward)
      if done:
        tab_done[int(not ply)][-1] = True
        break
    if game.visualBoard != None:
      if tab_rewards[-1] == 10:
        print(game.board)
        time.sleep(3)
    game.CloseGame()
    for i in range(2):
      tab_rewards[i]=np.array(tab_rewards[i], dtype=np.float32)
      tab_actions[i]=np.array(tab_actions[i], dtype=np.int32)
      tab_observations[i]=np.array(tab_observations[i], dtype=np.float32)
      tab_next_observations[i]=np.array(tab_next_observations[i], dtype=np.float32)
      tab_done[i]=np.array(tab_done[i], dtype=np.float32)
      train_step(tab_rewards[i], tab_actions[i], tab_observations[i], tab_next_observations[i], tab_done[i])
      train_loss.reset_states()

    epsilon-=epsilon_decay_value
    epsilon=max(epsilon, epsilon_min)
    if e % 500 == 0:
      model.save("Connect4Model")  
  model.save("Connect4Model")




model=GetModel()
optimizer=tf.keras.optimizers.Adam(learning_rate=1E-4)
train_loss=tf.keras.metrics.Mean()


