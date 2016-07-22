import numpy as np
import scipy.sparse as spsp
import pandas as pd
from rescal import rescal_als
import config
from optparse import OptionParser
from utils import time_utils, pkl_utils
from sklearn.metrics import precision_recall_curve, auc
from numpy.random import shuffle

import logging
logging.basicConfig(level=logging.INFO)
_log = logging.getLogger('Tensor Factorization for DBpedia')

def parse_args(parser):
	parser.add_option("-l", "--lang", default="en", type="string", dest="lang", help="specify the language")
	(options, args) = parser.parse_args()
	return options, args

def parse(lang="en"):
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
		predicateDict[cnt] = predicate
		cnt += 1
	type_entries = [entry for entry in type_entries if entry[0] in instanceSet]
	rows = [entityDict[entry[0]] for entry in type_entries]
	cols = [entityDict[entry[1]] for entry in type_entries]
	data = [1 for entry in type_entries]
	mat = spsp.csr_matrix((data, (rows, cols)), (N, N))
	tensor.append(mat)
	predicateDict[cnt] = rdf_type
	_log.info("%d relations" % (cnt+1))
	pkl_utils._save(config.TENSOR[lang], tensor)
	pkl_utils._save(config.ENTITY[lang], entityDict)
	pkl_utils._save(config.PREDICATE[lang], predicateDict)
	pkl_utils._save(config.INSTANCE[lang], instanceDict)
	pkl_utils._save(config.TYPE[lang], typeDict)
	pkl_utils._save(config.TYPE_MATRIX[lang], (rows, cols))
	_log.info("parsing complete")

def predict_rescal_als(T, idx):
	A, R, _, _, _ = rescal_als(T, 10, maxIter=10, lambda_A=10, lambda_R=10, compute_fit=False)
	n = A.shape[0]
	P = np.dot(A, np.dot(R[-1], A[idx, :].T))
	nrm = np.linalg.norm(P)
	if nrm != 0:
		P = np.round_(P/nrm, decimals=3)
	return P

def factorize(lang="en"):
	X = pkl_utils._load(config.TENSOR[lang])
	entityDict = pkl_utils._load(config.ENTITY[lang])
	typeDict = pkl_utils._load(config.TYPE[lang])
	entry = pkl_utils._load(config.TYPE_MATRIX[lang])
	t2e = {typeDict[t]:entityDict[t] for t in typeDict}
	_log.info("Data has been loaded")
	N, M = X[0].shape[0], len(X)
	_log.info('Datasize: %d x %d x %d' % (N, N, M))

	FOLDS = 5
	IDX = list(range(N))
	shuffle(IDX)
	fsz = int(N/FOLDS)
	offset = 0
	tid = t2e[typeDict["http://dbpedia.org/ontology/Person"]]
	GROUND_TRUTH = X[-1][:, tid]
	AUC = np.zeros(FOLDS)
	for f in range(FOLDS):
		idx = set(IDX[offset:offset+fsz])
		offset += fsz
		_log.info('Fold %d' % f)
		T = [x.copy() for x in X[:-1]]
		rows = []
		cols = []
		data = []
		for x,y in zip(entry[0], entry[1]):
			if (x in idx) and (y == tid):
				continue
			rows.append(x)
			cols.append(y)
			data.append(1)
		T.append(spsp.csr_matrix((data, (rows, cols)), (N, N)))
		_log.info('Construction complete')
		P = predict_rescal_als(T, tid)
		precision, recall, _ = precision_recall_curve(GROUND_TRUTH, P)
		AUC[f] = auc(precision, recall)
		_log.info('AUC: %f' % AUC[f])
	
	_log.info('AUC-PR Test Mean / Std: %f / %f' % (AUC.mean(), AUC.std()))


def main(options):
	lang = options.lang

	#parse(lang)
	factorize(lang)

if __name__ == "__main__":
	parser = OptionParser()
	options, args = parse_args(parser)
	main(options)
