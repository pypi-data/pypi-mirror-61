import sys
import io
from pickle import dump
from pickle import load

def convert_txt_as_raw_txt(txt):
	"""This function takes a string as input and returns it but the separators as replaced
	by spaces.
	@param: txt (string)
	@return: txt (string)
	"""
	txt = txt.split()
	txt = ' '.join(txt)
	return txt

def get_absolute_language_model(txt, length):
	"""This function returns a dictionnary that has as keys all the characters sequencies (length-ngrams)
	found in the text and as values others dictionnaries. These dictionnaries have as keys all the characters 
	found after the previous character sequencies and as keys the absolute count of this pair.  
	@param: txt (string): raw text to extract language model
	@param: length (integer): length of the ngrams
	@return: model (dictionary): language model
	"""
	length = length - 1 
	model = {}
	raw_text = convert_txt_as_raw_txt(txt) # Make sure there is not line separations
	sequences = []
	for i in range(length, len(raw_text)):
		seq = raw_text[i-length:i+1] # A sequence of characters
		sequences.append(seq)
	sequences = list(set(sequences))
	vocab = list(set(raw_text)) # all the different characters found in <txt>

	for seq in sequences:
		if seq not in model.keys():
			model[seq] = {}
		for char in vocab:
			if char not in model[seq].keys():
				model[seq][char] = 0
			str_to_test = seq + char
			model[seq][char] += raw_text.count(str_to_test)
	return model

def convert_onto_proba_language_model(abs_model):
	"""This function transforms an absolute count of the proba into a relative count (in [0 ; 1]).
	@param: abs_model: a model given by the function <get_absolute_language_model>
	@return: proba_model: the same model but with probabilities
	"""
	proba_model = {}
	for seq in abs_model.keys():
		nb = 0
		for char in abs_model[seq].keys(): # We count the number of characters after the current char.
			nb += abs_model[seq][char]
		proba_model[seq] = {} 
		for char in abs_model[seq].keys():
			if nb != 0:
				proba_model[seq][char] = abs_model[seq][char] / nb
			else:
				proba_model[seq][char] = 0
	return proba_model

def get_intersection(model1, model2):
	same = {}
	for seq in model1.keys():
		if seq in model2.keys():
			same[seq] = {}
			for char in model1[seq].keys():
				if char in model2[seq].keys():
					same[seq][char] = (model1[seq][char], model2[seq][char])
	return same

def get_proba(intersection_model):
	values1, values2 = ([], [])
	for seq in intersection_model.keys():
		for char in intersection_model[seq].keys():
			values1.append(intersection_model[seq][char][0])
			values2.append(intersection_model[seq][char][1])
	if len(values1) < 2:
		print('Impossible to get the probabities because there is not enough similarities between the two models.')
		return -1
	else:
		return (values1, values2)


class CharBasedSimpleProbaLanguageModel():
	"""This class is used to learn, save, load and use character based language model."""

	def __init__(self, txt='', length=0, model_path=''):
		"""In order to create a language model, we can give:
		@param: txt (string): a raw txt
		@param: length (int): an interger = the character sequence length needed to learn the model
		@param: model_p (string): path to the model in case we prefer load a model rather learn another one
		"""
		self._txt = txt
		self._length = length
		self._modelPath = model_path
		if self._txt != '' and self._length != 0: # That means we have to learn a model
			self._model = self.learn_language_model(self._txt, self._length)
			if self._modelPath != '': # That means the uses want to save his model
				self.save_model()
		elif self._modelPath != '': # That means we hate to load a model
			self._model, self._length = self.load_model()
		else:
			print('In order to create a CharBasedSimpleProbaLanguageModel Object, you need to:'
				+ '\n- or give a raw text and a length ;'
				+ '\n- or give a path to a model to load and a length.')


	def learn_language_model(self, txt, length):
		"""This function allows to create learn a character based language model. 
		@param: txt (string): a raw text
		@param: length (int): the character sequence length needed to learn the model
		@return: proba_model (dictionary): the model (keys=sequences, values=proba)
		"""
		print('Learning...')
		abs_model = get_absolute_language_model(txt, length)
		proba_model = convert_onto_proba_language_model(abs_model)
		print('Done.')
		return proba_model

	def save_model(self):
		"""Function to save the model (dictionary).
		@param: model: the model
		@param: model_path (string): path to where the user want to save his model

		"""
		try:
			dump(self._model, open(self._modelPath, 'wb'))
			print('Model saved in ' + self._modelPath)
		except:
			print('Impossible to save the model.')

	def load_model(self):
		"""This function allows to give model path and returns the model itself.
		@param: model_p (string): path to the model in case we prefer load a model rather learn another one
		@return: proba_model (dictionary): the model.
		"""
		try:
			proba_model = load(open(self._modelPath, 'rb'))
			one_seq = list(proba_model.keys())[0]
			length = len(one_seq)
			return (proba_model, length)
		except:
			print('Impossible to access to the model.')
			return -1


	def generate_seq(self, in_text, n_chars): #(model, mapping, seq_length, in_text, n_chars):
		"""This function allows the user to generate a character sequence given a certain other sequence.
		@param: in_text (string): the character given by the user 
		@param: n_chars (int): the number of character the user want to generate avec the <in_text>
		@return: in_text (string): it is <in_text> as parameter increased by the character generated by the model.
		"""
		pass

	def get_proba(self, in_text, factual_char):
		"""This function returns a probabily. Given a sequence of character, the model is used to returns the probability
		that the <factual_char> that follow appear. 
		@param: in_text (string): a sequence of characters
		@param: factual_char (char): a character (that follow the sequence and for which we want to know the proba)
		@return: proba
		"""
		try:
			if len(in_text) != self._length:
				in_text = in_text[:self._length]
			if in_text in self._model.keys() and factual_char in self._model[in_text].keys():
				return self._model[in_text][factual_char]
			else:
				return 0
		except:
			print('Something went wrong when getting the probability. Please verify this object has a model.')



