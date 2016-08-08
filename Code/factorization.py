import numpy as np
import scipy.sparse as spsp
import pandas as pd
from rescal import rescal_als
import config
from optparse import OptionParser
from utils import time_utils, pkl_utils
import os

import logging
logging.basicConfig(level=logging.INFO)
_log = logging.getLogger('RESCAL')

def parse_args(parser):
	parser.add_option("-l", "--lang", default="en", type="string", dest="lang", help="specify the language")
	parser.add_option("-p", "--parse", default=False, action="store_true", dest="parse", help="enable the parsing module")
	parser.add_option("-t", "--train", default=False, action="store_true", dest="train", help="enable the training module")
	parser.add_option("-r", "--rank", default=10, type="int", dest="r", help="specify the rank")
	parser.add_option("-i", "--iteration", default=10, type="int", dest="i", help="specify the number of iteration")
	parser.add_option("--fin", type="string", dest="fin", help="the path of input file")
	parser.add_option("--fout", type="string", dest="fout", help="the path of output file")
	(options, args) = parser.parse_args()
	return options, args

def parse(lang="en"):
	_log.info("starting parsing")
	infile = open(config.INSTANCE_TYPES[lang])
	rdf_type = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
	type_entries = []
	entitySet = set()
	typeSet = set()
	for line in infile.readlines():
		if line[0] != "<":
			continue
		row = line.split()
		instance = row[0][1:-1]
		ontology = row[2][1:-1]
		type_entries.append((instance, ontology))
		entitySet.add(ontology)
		typeSet.add(ontology)
	typeDict = {y:x for x, y in enumerate(typeSet)}
	infile.close()

	cnt_type = len(entitySet)
	_log.info("%d types" % cnt_type)

	infile = open(config.OBJECTS[lang])
	relationDict = {}
	instanceSet = set()
	for line in infile.readlines():
		if line[0] != "<":
			continue
		row = line.split()
		subject = row[0][1:-1]
		predicate = row[1][1:-1]
		target = row[2][1:-1]
		entitySet.add(subject)
		entitySet.add(target)
		instanceSet.add(subject)
		instanceSet.add(target)
		if predicate in relationDict:
			relationDict[predicate].append((subject, target))
		else:
			relationDict[predicate] = [(subject, target)]
	instanceDict = {y:x for x, y in enumerate(instanceSet)}
	entityDict = {y:x for x, y in enumerate(entitySet)}
	infile.close()

	cnt_ins = len(instanceSet)
	N = len(entitySet)
	_log.info("%d instanes" % cnt_ins)
	_log.info("%d entites" % N)
	
	tensor = []
	predicateDict = {}
	cnt = 0
	for predicate in relationDict:
		entries = relationDict[predicate]
		rows = [entityDict[entry[0]] for entry in entries]
		cols = [entityDict[entry[1]] for entry in entries]
		data = [1 for entry in entries]
		mat = spsp.csr_matrix((data, (rows, cols)), (N, N))
		tensor.append(mat)
		predicateDict[predicate] = cnt
		cnt += 1
	type_entries = [entry for entry in type_entries if entry[0] in instanceSet]
	rows = [entityDict[entry[0]] for entry in type_entries]
	cols = [entityDict[entry[1]] for entry in type_entries]
	data = [1 for entry in type_entries]
	mat = spsp.csr_matrix((data, (rows, cols)), (N, N))
	tensor.append(mat)
	predicateDict[rdf_type] = cnt
	_log.info("%d relations" % (cnt+1))
	pkl_utils._save(config.TENSOR[lang], tensor)
	pkl_utils._save(config.ENTITY[lang], entityDict)
	pkl_utils._save(config.PREDICATE[lang], predicateDict)
	pkl_utils._save(config.INSTANCE[lang], instanceDict)
	pkl_utils._save(config.TYPE[lang], typeDict)
	pkl_utils._save(config.TYPE_MATRIX[lang], (rows, cols))
	_log.info("parsing complete")

def tensor_factorization(lang, r, n_iter):
	_log.info("start factorization")
	X = pkl_utils._load(config.TENSOR[lang])
	_log.info("data loading complete")
	A, R, _, _, _ = rescal_als(X, r, maxIter=n_iter, lambda_A=10, lambda_R=10, compute_fit=False)
	data_output = {'A':A, 'R':R}
	pkl_utils._save(config.RESCAL_OUTPUT[lang], data_output)
	_log.info("factorization complete")

def compute_scores(A, R, ss, ps, os):
	return np.array([
		np.dot(A[ss[i], :], np.dot(R[ps[i]], A[os[i], :].T))
		for i in range(len(ss))
	])

def main(options):
	lang = options.lang
	fin = options.fin
	fout = options.fout
	p = options.parse
	t = options.train
	r = options.r
	n_iter = options.i

	if p:
		parse(lang)
	if t:
		tensor_factorization(lang, r, n_iter)
	
	entityDict = pkl_utils._load(config.ENTITY[lang])
	predicateDict = pkl_utils._load(config.PREDICATE[lang])
	tf = pkl_utils._load(config.RESCAL_OUTPUT[lang])
	A = tf["A"]
	R = tf["R"]
	df = pd.read_csv(fin, names=["s", "p", "o"])
	df["s"] = df["s"].map(entityDict)
	df["p"] = df["p"].map(predicateDict)
	df["o"] = df["o"].map(entityDict)
	scores = compute_scores(A, R, list(df["s"]), list(df["p"]), list(df["o"]))
	pd.DataFrame(scores).to_csv(fout, index=False, header=False)


if __name__ == "__main__":
	parser = OptionParser()
	options, args = parse_args(parser)
	main(options)
