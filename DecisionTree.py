from sklearn import tree
import numpy as np

def get_x_vector_from_state(state):
	x_vector = []
	x_vector.append(state.agent1.pos.id)
	x_vector.append(state.agent1.pickup.get_target().id)
	x_vector.append(state.agent2.pos.id)
	x_vector.append(state.agent2.pickup.get_target().id)
	for agent in state.agents:
		x_vector.append(agent.pos.id)
	return x_vector

class DecisionTree(object):
	def __init__(self, file_name):
		self.file_name = file_name
		self.tree = tree.DecisionTreeClassifier()
		self.train_tree()


	def train_tree(self):
		file = open(self.file_name, 'r')
		x = []
		y = []
		for line in file:
			elements = line.split()
			one_y = elements.pop()
			one_x = [int(elem) for elem in elements]
			x.append(one_x)
			y.append(one_y)

		number_of_inputs = len(x)
		train_index = int(number_of_inputs*0.8)

		train_x = x[:train_index]
		train_y = y[:train_index]

		test_x = x[train_index:]
		test_y = y[train_index:]
		self.tree.fit(train_x, train_y)

		print("Tree score is: %.3f" % (self.tree.score(test_x, test_y)))

	def get_rule(self, state):
		x = get_x_vector_from_state(state)
		prediction = int(self.tree.predict([x])[0])
		print("The tree predicted rule: %d" % (prediction))
		return prediction