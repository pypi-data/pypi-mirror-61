import os
import io
import subprocess

def get_txt_from_file(file_name):
	"""This function only reads a file and returns its containt.
	@param: file_name (string): path to the file
	@return: txt (string): text read in <file_name>
	"""
	txt = ''
	file = io.open(file_name, mode='r', encoding='utf-8')
	txt += file.read()
	file.close()
	return txt


def get_txt_from_dir(dir_name):
	"""This function, given a directory, returns a dictionary as:
	- keys: file_name (found in <dir_name>)
	- values: text read in <file_name>
	@param: dir_name (string): path to the directory we want to get the texts
	@returns: res (directory): see above.
	"""
	file_names = [n for n in os.listdir(dir_name) if '.txt' in n]
	res = {f:get_txt_from_file(dir_name+f) for f in file_names}
	return res

def parse_asrtoolkit_result(res):
	"""This function returns the asrtoolkit result (cer or wer) as follow:
	'CER: 4%' --> 4
	@param: res (string): the string that asrtoolkit returns
	@return: res_net (float): only the number
	"""
	res_net = str(res)
	for s in ['WER: ', 'CER: ', '%\\n', '\'', 'b']:
		res_net = res_net.replace(s, '')
	return float(res_net)

def cer_wer(file_ref, file_test):
	"""This function processes, using the asrtoolkit, the character error rate and the word error rate,
	given a reference text file and a file to test.
	@param: file_ref (string): path to the reference text
	@param: file_test (string): path to the text to test
	@return: error_rates (tuple): (cer, wer)
	"""
	# Character Error Rate
	cer_cmd = 'wer ' + file_ref + ' ' + file_test + ' --char-level'
	cer_res = subprocess.check_output(cer_cmd, shell=True)
	cer = parse_asrtoolkit_result(cer_res)
	# Word Error Rate
	wer_cmd = 'wer ' + file_ref + ' ' + file_test
	wer_res = subprocess.check_output(wer_cmd, shell=True)
	wer = parse_asrtoolkit_result(wer_res)
	return (cer, wer)

def cer_wer_from_directories(dir_ref, dir_test):
	"""This function allows the user to process cer and wer for several files at the same time. But the files
	in <dir_test> must be aligned to the files in <dir_ref>, aligned by their names...
	@param: dir_ref (string): path to the directory in which the reference files are stored
	@param: dir_test (string): path to the directory in which the test files are stored
	@return: res (dictionary): dictionary in which the (cer, wer) are stored (key=(path_ref, path_test), values=(cer, wer))
	"""
	res = {}
	ref_files = sorted([n for n in os.listdir(dir_ref) if '.txt' in n])
	test_files = sorted([n for n in os.listdir(dir_test) if '.txt' in n])
	root_names = [n.replace('.txt', '') for n in ref_files] # Here, we assume that the ref files names are 
															# "root"=in all the test files we can find the
															# root and something more as suffixe.
	for root in root_names:
		r = dir_ref + root + '.txt'
		t = '' # We try to find the test file associated to the ref file
		for file in test_files:
			if root in file:
				t = dir_test + file
		if t != '':
			res[(r, t)] = cer_wer(r, t)
	return res

def get_sequencies(txt, length):
	"""Given a raw text (string), this function returns all the sequencies we can find by a sliding
	window.
	@param: txt (string)
	@param: length (int)
	@return: sequencies (list)
	"""
	raw_text = txt.replace('\n', ' ')
	sequencies = []
	for i in range(length, len(raw_text)):
		seq = raw_text[i-length:i+1] # A sequence of characters
		sequencies.append(seq)
	return sequencies

def global_proba_with_model(txt_file, model, ngrams):
	"""This function calculates, for a sequence (length=ngrams), the probabiblity to have the next 
	character, given a language model. And this is done for the entire text, with a sliding window.
	@param: txt_file (string): file in which the text is stored
	@param: model (LanguageModel): the language model, neural with the Keras library or only probabilistic:
			it's used to predict the next character given a sequence
	@param: ngrams (int): this is the length the model was learnt with 
	@return: proba (float): the sum of all the probabilities calculated for the entire text with the 
			 given model
	"""
	proba = 0
	txt = get_txt_from_file(txt_file)
	sequencies = get_sequencies(txt, ngrams)
	for i in range(len(sequencies) - 1):
		proba += model.get_proba(sequencies[i], sequencies[i + 1][0])
	return proba

def proba_per_line_with_model(txt_file, model, ngrams):
	"""This function calculates, for a sequence (length=ngrams), the probabiblity to have the next 
	character, given a language model. And this is done for every lines in the text, with a sliding window.
	BUT: the number of characters might be inferior than the ngrams; in this case, the function give -1. 
	@param: txt_file (string): file in which the text is stored
	@param: model (LanguageModel): the language model, neural with the Keras library or only probabilistic:
			it's used to predict the next character given a sequence
	@param: ngrams (int): this is the length the model was learnt with 
	@return: probas (dictionary): keys=nb_line, values=sum of the probas for this line
	"""
	probas = {}
	txt = get_txt_from_file(txt_file)
	lines = txt.split('\n')
	cnt = 1 # line counter
	for line in lines:
		line_name = 'line' + str(cnt)
		proba = -1
		sequencies = get_sequencies(line, ngrams)
		if len(sequencies) > 2:
			proba = 0
			for i in range(len(sequencies) - 1):
				proba += model.get_proba(sequencies[i], sequencies[i + 1][0])
		probas[line_name] = proba
		cnt += 1
	return probas




