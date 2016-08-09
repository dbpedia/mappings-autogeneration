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
_log = logging.getLogger('Tensor Factorization for DBpedia')

def parse_args(parser):
	parser.add_option("-l", "--lang", default="en", type="string", dest="lang", help="specify the language")
	parser.add_option("-p", "--parse", default=False, action="store_true", dest="parse", help="enable the parsing module")
	parser.add_option("-t", "--train", default=False, action="store_true", dest="train", help="enable the training module")
	parser.add_option("-c", "--ncomp", default=150, type="int", dest="ncomp", help="number of components")
	parser.add_option("-e", "--me", default=500, type="int", dest="me", help="maximum epoches")
	parser.add_option("--fin", type="string", dest="fin", help="the path of input file")
	parser.add_option("--fout", type="string", dest="fout", help="the path of output file")
	(options, args) = parser.parse_args()
	return options, args

def parse(lang="en"):
	dataDict = {}
	
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
	
	triples = []
	predicateDict = {}
	cnt = 0
	for predicate in relationDict:
		entries = relationDict[predicate]
		sub = [entityDict[entry[0]] for entry in entries]
		obj = [entityDict[entry[1]] for entry in entries]
		pred = [cnt for entry in entries]
		triples.extend(zip(sub, obj, pred))
		predicateDict[cnt] = predicate
		cnt += 1
	type_entries = [entry for entry in type_entries if entry[0] in instanceSet]
	sub = [entityDict[entry[0]] for entry in type_entries]
	obj = [entityDict[entry[1]] for entry in type_entries]
	pred = [cnt for entry in type_entries]
	triples.extend(zip(sub, obj, pred))
	predicateDict[cnt] = rdf_type
	triples = pd.Series(triples)
	_log.info("%d relations" % (cnt+1))
	_log.info("%d triples" % len(triples))

	dataDict["entities"] = list(entitySet)
	dataDict["relations"] = predicateDict.values()
	IDX = list(range(len(triples)))
	shuffle(IDX)
	dataDict["train_subs"] = list(triples[IDX[:-20000]])
	dataDict["valid_subs"] = list(triples[IDX[-20000:-10000]])
	dataDict["test_subs"] = list(triples[IDX[-10000:]])
	pkl_utils._save(config.DATA_DICT[lang], dataDict)

	_log.info("train size: %d" % len(dataDict["train_subs"]))
	_log.info("valid size: %d" % len(dataDict["valid_subs"]))
	_log.info("test size: %d" % len(dataDict["test_subs"]))

	_log.info("parsing complete")

def main(options):
	lang = options.lang
	p = options.parse
	t = options.train
	ncomp = options.ncomp
	me = options.me
	fin = options.fin
	fout = options.fout

	if p:
		parse(lang)
	if t:
		cmd = "python run_hole.py --fin %s --fout %s --test-all 50 --nb 100 --me %d \
			--margin 0.2 --lr 0.1 --ncomp %d" % (lang, config.HOLE_OUTPUT[lang], me, ncomp)
		os.system(cmd)
	
	hole = pkl_utils._load(config.HOLE_OUTPUT[lang])
	data_dict = pkl_utils._load(config.DATA_DICT[lang])
	model = hole["model"]
	entityDict = { y:x for x, y in enumerate(data_dict["entities"])}
	predicateDict = { y:x for x, y in enumerate(data_dict["relations"])}
	df = pd.read_csv(fin, names=["s", "p", "o"])
	df["s"] = df["s"].map(entityDict)
	df["p"] = df["p"].map(predicateDict)
	df["o"] = df["o"].map(entityDict)
	scores = model._scores(list(df["s"]), list(df["p"]), list(df["o"]))
	pd.DataFrame(scores).to_csv(fout, index=False, header=False)

if __name__ == "__main__":
	parser = OptionParser()
	options, args = parse_args(parser)
	main(options)
