import gym
import tensorflow as tf
from tensorflow.keras import models, layers
import numpy as np

env = gym.make("CartPole-v0")
env._max_episode_steps=500
nbr_action=7

gamma=tf.constant(0.98)
# epoch=20000
# best_score=0

# epsilon=1.
# epsilon_min=0.10
# start_epsilon=1
# end_epsilon=epoch//2
# epsilon_decay_value=epsilon/(end_epsilon-start_epsilon)

def model():
  entree=layers.Input(shape=(42), dtype='float32')
  result=layers.Dense(30, activation='relu')(entree)
  result=layers.Dense(30, activation='relu')(result)
  sortie=layers.Dense(nbr_action)(result)
    
  model=models.Model(inputs=entree, outputs=sortie)
  return model

def my_loss(target_q, predicted_q):
  loss=tf.reduce_mean(tf.math.square(target_q-predicted_q))
  return loss


def train_step():
  global tab_rewards, tab_actions, tab_observations, tab_next_observations, tab_done
  tab_rewards=np.array(tab_rewards, dtype=np.float32)
  tab_actions=np.array(tab_actions, dtype=np.int32)
  tab_observations=np.array(tab_observations, dtype=np.float32)
  tab_next_observations=np.array(tab_next_observations, dtype=np.float32)
  tab_done=np.array(tab_done, dtype=np.float32)
  
  next_Q_values=model(tab_next_observations)
  best_next_actions=tf.math.argmax(next_Q_values, axis=1)
  next_mask=tf.one_hot(best_next_actions, nbr_action)
  next_best_Q_values=tf.reduce_sum(next_Q_values*next_mask, axis=1)
  target_Q_values=tab_rewards+(1-tab_done)*gamma*next_best_Q_values
  target_Q_values=tf.reshape(target_Q_values, (-1, 1))
  mask=tf.one_hot(tab_actions, nbr_action)
  
  with tf.GradientTape() as tape:
    all_Q_values=model(tab_observations)
    Q_values=tf.reduce_sum(all_Q_values*mask, axis=1, keepdims=True)
    loss=my_loss(target_Q_values, Q_values)
  gradients=tape.gradient(loss, model.trainable_variables)
  optimizer.apply_gradients(zip(gradients, model.trainable_variables))
  train_loss(loss)
  
  tab_observations=[]
  tab_rewards=[]
  tab_actions=[]
  tab_next_observations=[]
  tab_done=[]

# def train(debug=False):
#   global epsilon, best_score, tab_score
#   for e in range(epoch):
#     if e % 100 == 0:
#         print("EPOCH:", e, "epsilon", epsilon, end=("\r"))
#     score=0
#     tab_observations=[]
#     tab_rewards=[]
#     tab_actions=[]
#     tab_next_observations=[]
#     tab_done=[]
    
#     observations=env.reset()
#     while True:
#       tab_observations.append(observations)    
#       if np.random.random()>epsilon:
#         valeurs_q=model(np.expand_dims(observations, axis=0))
#         action=int(tf.argmax(valeurs_q[0], axis=-1))
#       else:
#         action=np.random.randint(0, nbr_action)
#       observations, reward, done, info=env.step(action)
#       tab_actions.append(action)
#       tab_next_observations.append(observations)
#       tab_done.append(done)
#       if done:
#         tab_rewards.append(-10.)
#         #print("FIN, score:", score, end=("\r"))
#         tab_score.append(score)
#         score=0
#         break
#       score+=1
#       tab_rewards.append(reward)

#     tab_rewards=np.array(tab_rewards, dtype=np.float32)
#     tab_actions=np.array(tab_actions, dtype=np.int32)
#     tab_observations=np.array(tab_observations, dtype=np.float32)
#     tab_next_observations=np.array(tab_next_observations, dtype=np.float32)
#     tab_done=np.array(tab_done, dtype=np.float32)
#     train_step(tab_rewards, tab_actions, tab_observations, tab_next_observations, tab_done)
#     train_loss.reset_states()

#     epsilon-=epsilon_decay_value
#     epsilon=max(epsilon, epsilon_min)
#     if np.mean(tab_score[-20:])>best_score:
#       #print("Sauvegarde du modele")
#       model.save("my_model")
#       best_score=np.mean(tab_score[-20:])
#       if best_score==499:
#         return

def ChoiseAction(observation, epsilon):
    if np.random.random()>epsilon:
        valeurs_q=model(np.expand_dims(observation, axis=0))
        action=int(tf.argmax(valeurs_q[0], axis=-1))
    else:
        action=np.random.randint(0, nbr_action)
    return action

def ActionReturn(observation, action, next_observation, done, reward):
    global tab_observations, tab_rewards ,tab_actions, tab_next_observations, tab_done
    tab_observations.append(observation)
    tab_actions.append(action)
    tab_next_observations.append(next_observation)
    tab_done.append(done)
    tab_rewards.append(reward)

    
tab_observations=[]
tab_rewards=[]
tab_actions=[]
tab_next_observations=[]
tab_done=[]
    
model=model()
optimizer=tf.keras.optimizers.Adam(learning_rate=1E-4)
train_loss=tf.keras.metrics.Mean()
tab_s=[]

tab_score=[]
#train()

np.save("tab_score", tab_score)

