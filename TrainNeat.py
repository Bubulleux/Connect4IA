import motor
import neat
import random
import numpy as np
import gzip
import pickle


def Train():
	config_path = "./neat_config"
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)

	best_genome = p.run(tournament, 50)
	save_genome(best_genome)


def tournament(genomes, config):
	all_nets = []

	for i, cur_genome in genomes:
		net = neat.nn.FeedForwardNetwork.create(cur_genome, config)
		all_nets.append(net)
		cur_genome.fitness = 0

	nets_alive = all_nets.copy()
	print()
	turn = 0
	while True:
		turn += 1
		nets_qualify = []
		while True:
			if len(nets_alive) < 2:
				break
			plys = []
			for i in range(2):
				ply = random.choice(nets_alive)
				nets_alive.remove(ply)
				plys.append(ply)

			game = motor.Connect4(show_board=False)

			while True:
				ply = plys[(game.plyTurn + 1) // 2]
				output = ply.activate(game.observation() * game.plyTurn)
				best_action = output.index(max(output))
				obs, reward, done = game.play(best_action)
				if done:
					if len(nets_alive) < 2 and len(nets_qualify) == 0:
						game.print()
					winner = plys[(game.win + 1) // 2]
					genomes[all_nets.index(winner)][1].fitness += reward
					nets_qualify.append(winner)
					# print(f"{all_nets.index(plys[0])} Vs {all_nets.index(plys[1])}, {all_nets.index(winner)} Won")
					break
		if len(nets_qualify) == 0:
			break
		else:
			nets_alive = nets_qualify

	# for i, cur_genome in genomes:
	# 	print(f"{i}: {cur_genome[1].fitness}")


def save_genome(genome):
	with open("NeatModel.pkl", "wb") as f:
		pickle.dump(genome, f)
		f.close()


def load_genome():
	with open("winner.pkl", "wb") as f:
		genome = pickle.load(f)
	return genome