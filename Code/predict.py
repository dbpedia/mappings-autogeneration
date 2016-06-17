# -*- coding: utf-8 -*-
import pandas as pd
import config
from utils import time_utils
from collections import defaultdict
from optparse import OptionParser
import os.path
import parse

def parse_args(parser):
	parser.add_option("-l", "--lang", default="bg", type="string", dest="lang", help="specify the language to evaluate")
	parser.add_option("-p", "--pivots", default="en", type="string", dest="pivots", help="specify the pivot languages")
	parser.add_option("-L", default=0.5, type="float", dest="L", help="parameter to tune the tradeoff between precision and recall")
	parser.add_option("-C", default=10, type="int", dest="C", help="minimum occuurrence of a infobox")
	parser.add_option("-e", default=False, action="store_true", dest="evaluate", help="evaluate the predicted mapping")
	(options, args) = parser.parse_args()
	return options, args

def main(options):
	lang = options.lang
	pivots= options.pivots
	L = options.L
	C = options.C
	flag = options.evaluate
	print "[%s] predict the mapping for language %s" % (time_utils._timestamp(), lang)

	df = pd.read_csv(config.ENTITY_MATRIX["%s2%s" % (lang, pivots)])
	df = df.dropna()
	grouped = df.groupby("template1")
	template = []; ontology = []; occurrence = []; frequency = []
	for name, group in grouped:
		classDict = defaultdict(int)
		for o in group["ontology"]:
			classDict[o] += 1
		N = group.shape[0]
		c = sorted(classDict, key=classDict.get, reverse=True)[0]
		template.append(name)
		ontology.append(c)
		occurrence.append(N)
		frequency.append(1.0*classDict[c]/N)
	data = {"template":template, "ontology":ontology, "occurrence":occurrence, "frequency":frequency}
	res = pd.DataFrame(data)
	#msk = (res["occurrence"] > C) & (res["frequency"] > L)
	#res = res[msk]
	res.to_csv(config.MAPPED_INFOBOX[lang],index=False)
	print "[%s] prediction complete" % time_utils._timestamp()

	if flag:
		if not os.path.isfile(config.EXISTING_MAPPING_OUTPUT[lang]):
			parse.getExistingMapping(lang=lang)
		print "[%s] evaluate the predicted mapping" % time_utils._timestamp()
		mapping = pd.read_csv(config.EXISTING_MAPPING_OUTPUT[lang], index_col="template")
		TP = 0
		for t, o in zip(res["template"], res["ontology"]):
			if t in mapping.index:
				if o == mapping.loc[t, "ontology"]:
					TP += 1
		N = res.shape[0]
		M = mapping.shape[0]
		print "precison: %3f" % (1.0*TP/N)
		print "recall:   %3f" % (1.0*TP/M)
		
		print "[%s] evaluation complete" % time_utils._timestamp()


if __name__ == "__main__":
	parser = OptionParser()
	options, args = parse_args(parser)
	main(options)
