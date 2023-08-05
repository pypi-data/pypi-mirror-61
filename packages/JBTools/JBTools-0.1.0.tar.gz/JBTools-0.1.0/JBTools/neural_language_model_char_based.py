# I used this tutorial to make this code :
# https://machinelearningmastery.com/develop-character-based-neural-language-model-keras/
import sys
from numpy import array
from pickle import dump, load
from keras.utils import to_categorical
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import LSTM

class CharBasedNeuralLanguageModel():
	"""This class is used to learn, save, load and use character based language model."""

	def __init__(self, t='', l=0, model_p='', mapping_p=''):
		"""In order to create a neural language model, we can give:
		@param: txt (string): a raw txt
		@param: length (int): an interger = the character sequence length needed to learn the model
		@param: model_p (string): path to the model in case we prefer load a model rather learn another one
		@param: mapping_p (string): path to the character/integer mapping dictionary
		"""
		self._txt = t
		self._length = l
		self._modelPath = model_p
		self._mappingPath = mapping_p
		if self._txt != '' and self._length != 0: # That means we have to learn a model
			d = self.learn_language_model(self._txt, self._length)
			self._model, self._mapping = (d['model'], d['mapping'])
			if self._modelPath != '' and self._mappingPath != '': # That means the uses want to save his model
				self.save_model()
		elif self._length != 0 and self._modelPath != '' and self._mappingPath != '': # That means we hate to load a model
			d = self.load_model(self._modelPath, self._mappingPath)
			self._model, self._mapping = (d['model'], d['mapping'])
		else:
			print('In order to create a CharBasedNeuralLanguageModel Object, you need to:'
				+ '\n- or give a raw text and a length ;'
				+ '\n- or give a path to a model and to a mapping dictionary to load and a length.')


	def learn_language_model(self, txt, length):
		"""This function allows to create learn a character based language model. 
		@param: txt (string): a raw text
		@param: length (int): the character sequence length needed to learn the model
		@return: d (dictionary): in <d> are stored the model and the character/integer mapping dic
		"""
		# a. Get the data (raw_text and character sequencies)
		tokens = txt.split()
		raw_text = ' '.join(tokens)
		sequences = []
		for i in range(length, len(raw_text)):
			seq = raw_text[i-length:i+1] # A sequence of characters
			sequences.append(seq)
		chars = sorted(list(set(raw_text))) # An sorted list of all distinct characters in raw_text
		# b. Transform the sequencies by integers
		mapping = dict((c, i) for i, c in enumerate(chars)) # A dic where characters are associated to an integer
		encoded_sequences = [] # Here we encoded the sequences with the integer (via <mapping>)
		for line in sequences:
			encoded_seq = [mapping[char] for char in line]
			encoded_sequences.append(encoded_seq)
		vocab_size = len(mapping)
		encoded_sequences = array(encoded_sequences)
		# c. Prepare the data

		X, y = encoded_sequences[:,:-1], encoded_sequences[:,-1]
		sequences = [to_categorical(x, num_classes=vocab_size) for x in X] # one-hot representation
		X = array(sequences)
		y = to_categorical(y, num_classes=vocab_size) # one-hot representation
		# d. Define the model
		model = Sequential()
		model.add(LSTM(75, input_shape=(X.shape[1], X.shape[2]))) # return_sequences=True pour BILSTM
		model.add(Dense(vocab_size, activation='softmax'))
		model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
		model.fit(X, y, epochs=100, verbose=2)
		d = {'model': model, 'mapping': mapping}
		return d

	def load_model(self, model_path, mapping_path):
		"""This function allows to give two paths to first a model and also a character/integer mapping dictionary
		and returns the model and the mapping dic.
		@param: model_p (string): path to the model in case we prefer load a model rather learn another one
		@param: mapping_p (string): path to the character/integer mapping dictionary
		@return: d (dictionary): in <d> are stored the model and the character/integer mapping dic
		"""
		try:
			model = load_model(model_path)
			mapping = load(open(mapping_path, 'rb'))
			d = {'model': model, 'mapping': mapping}
			return d
		except:
			print('Impossible to access to the model or the mapping.')
			return {'model': '', 'mapping': ''}

	def save_model(self):
		"""Function to save the model and the mapping dictionary.
		@param: model: the model
		@param: model_path (string): path to where the user want to save his model
		@param: mapping (dictionary): in it are stored the model and the character/integer mapping dictionary
		@param: mapping_path (string): path to where the user want to save his mapping dictionary

		"""
		try:
			self._model.save(self._modelPath)
			dump(self._mapping, open(self._mappingPath, 'wb'))
			print('Model and mapping saved')
		except:
			print('Impossible to save the model or the mapping.')

	def generate_seq(self, in_text, n_chars): #(model, mapping, seq_length, in_text, n_chars):
		"""This function allows the user to generate a character sequence given a certain other sequence.
		@param: in_text (string): the character given by the user 
		@param: n_chars (int): the number of character the user want to generate avec the <in_text>
		@return: in_text (string): it is <in_text> as parameter increased by the character generated by the model.
		"""
		try:
			for _ in range(n_chars): # This is the number of character we want to generate
				encoded = [self._mapping[char] for char in in_text] # Transforme the given text by integers
				encoded = pad_sequences([encoded], maxlen=self._length, truncating='pre') # truncate sequences to a fixed length
				encoded = to_categorical(encoded, num_classes=len(self._mapping)) # one hot encode
				yhat = self._model.predict_classes(encoded, verbose=0) # predict character
				# reverse map integer to character
				out_char = ''
				for char, index in self._mapping.items():
					if index == yhat:
						out_char = char
						break
				in_text += char # append to input
			return in_text
		except:
			print('Something went wrong in the character generation. Please verify this object has a model and a mapping dic.')

	def get_proba(self, in_text, factual_char):
		"""This function returns a probabily. Given a sequence of character, the model is used to returns the probability
		that the <factual_char> that follow appear. 
		@param: in_text (string): a sequence of characters
		@param: factual_char (char): a character (that follow the sequence and for which we want to know the proba)
		@return: proba
		"""
		try:
			known_chars = list(self._mapping.keys())
			test_chars = list(set(in_text + factual_char))
			sanity_check = all(elem in known_chars for elem in test_chars)
			if sanity_check == True:
				encoded = [self._mapping[char] for char in in_text] # Transforme the given text by integers
				encoded = pad_sequences([encoded], maxlen=self._length, truncating='pre') # truncate sequences to a fixed length
				encoded = to_categorical(encoded, num_classes=len(self._mapping)) # one hot encode --> returns a matrix 
				proba = self._model.predict_proba(encoded)
				return proba[0][self._mapping[factual_char]]
			else:
				return 0
		except:
			print('Something went wrong when getting the probability. Please verify this object has a model and a mapping dic.')




