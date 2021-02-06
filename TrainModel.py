import motor
import tensorflow as tf
from tensorflow.keras import models, layers
import numpy as np
import time

nbr_action = 7

gamma = tf.constant(0.98)
epoch = 100000
best_score = 0

epsilon = 1.
epsilon_min = 0.10
start_epsilon = 1
end_epsilon = epoch
epsilon_decay_value = epsilon / (end_epsilon - start_epsilon)


def get_model():
	entree = layers.Input(shape=42, dtype='float32')
	result = entree
	for i in range(6):
		result = layers.Dense(200, activation='relu')(result)
	sortie = layers.Dense(nbr_action)(result)

	return models.Model(inputs=entree, outputs=sortie)


def my_loss(target_q, predicted_q):
	loss = tf.reduce_mean(tf.math.square(target_q - predicted_q))
	return loss


# @tf.function
def train_step(reward, action, observation, next_observation, done):
	next_q_values = model(next_observation)
	best_next_actions = tf.math.argmax(next_q_values, axis=1)
	next_mask = tf.one_hot(best_next_actions, nbr_action)
	next_best_q_values = tf.reduce_sum(next_q_values * next_mask, axis=1)
	target_q_values = reward + (1 - done) * gamma * next_best_q_values
	target_q_values = tf.reshape(target_q_values, (-1, 1))
	mask = tf.one_hot(action, nbr_action)
	with tf.GradientTape() as tape:
		all_q_values = model(observation)
		q_values = tf.reduce_sum(all_q_values * mask, axis=1, keepdims=True)
		loss = my_loss(target_q_values, q_values)
	gradients = tape.gradient(loss, model.trainable_variables)
	optimizer.apply_gradients(zip(gradients, model.trainable_variables))
	train_loss(loss)


def train():
	global epsilon, best_score, model, train_loss
	model = get_model()
	train_loss = tf.keras.metrics.Mean()
	last_time = time.time()
	for e in range(epoch):
		score = 0
		tab_observations = [[], []]
		tab_rewards = [[], []]
		tab_actions = [[], []]
		tab_next_observations = [[], []]
		tab_done = [[], []]
		if e % 500 == 0:
			ops_left = epoch - e
			time_need = (time.time() - last_time)
			print(f"e: {e}, epsilon: {epsilon}, time: {(ops_left * (time_need / 500)) / 60} m")
			last_time = time.time()
		game = motor.Connect4(showBoard=False)
		observations = game.Observation()
		while True:
			ply = (game.plyTurn + 1) // 2
			tab_observations[ply].append(observations)
			if np.random.rand() > epsilon:
				value_q = model(np.expand_dims(observations, axis=0))
				action = int(tf.argmax(value_q[0], axis=-1))
			else:
				action = np.random.randint(0, nbr_action)
			observations, reward, done = game.Play(action)
			# print(f"done: {done}, reward {reward}, action {action}")
			observations *= game.plyTurn
			tab_actions[ply].append(action)
			tab_next_observations[ply].append(observations)
			tab_done[ply].append(done)
			score += reward
			tab_rewards[ply].append(reward)
			if done:
				tab_done[int(not ply)][-1] = True
				break
		if e % 200 == 0:
			game.Print()
			print(f"Start: {game.plyStart}, Win: {game.win}, reward: {tab_rewards[ply][-1]}")
		game.CloseGame()
		for i in range(2):
			tab_rewards[i] = np.array(tab_rewards[i], dtype=np.float32)
			tab_actions[i] = np.array(tab_actions[i], dtype=np.int32)
			tab_observations[i] = np.array(tab_observations[i], dtype=np.float32)
			tab_next_observations[i] = np.array(tab_next_observations[i], dtype=np.float32)
			tab_done[i] = np.array(tab_done[i], dtype=np.float32)
			train_step(tab_rewards[i], tab_actions[i], tab_observations[i], tab_next_observations[i], tab_done[i])
			train_loss.reset_states()

		epsilon -= epsilon_decay_value
		epsilon = max(epsilon, epsilon_min)
		if e % 500 == 0:
			model.save("Connect4Model")
	model.save("Connect4Model")


# model = get_model()
model = tf.keras.models.load_model("Connect4Model")
optimizer = tf.keras.optimizers.Adam(learning_rate=1E-4)
train_loss = tf.keras.metrics.Mean()
