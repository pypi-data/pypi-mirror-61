import os
import io
import sys
import random

def split_train_dev(lines, train_ratio):
	corpus = {i:lines[i] for i range(len(lines))}
	nb_train = len(lines) // train_ratio
	idx_train = []
	while len(idx_train) < nb_train:
		idx_train.append(random.randint(0, len(lines)))
		idx_train = list(set(idx_train))

	train = {i: corpus[i] for i in corpus.keys() if i in idx_train}
	dev = {i: corpus[i] for i in corpus.keys() if i not in idx_train}

	return train, dev