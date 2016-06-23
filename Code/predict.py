import config
import pandas as pd
from utils import time_utils, pkl_utils
from optparse import OptionParser
from collections import defaultdict
import os.path
import parse

G = pkl_utils._load(config.ONTOLOGY_TREE)
Root = "http://www.w3.org/2002/07/owl#Thing"

def parse_args(parser):
	parser.add_option("-l", "--lang", default="zh", type="string", dest="lang", help="target language")
	parser.add_option("-p", "--pivot", default="en", type="string", dest="pivots", help="pivot lanuages")
	parser.add_option("-L", default=0.5, type="float", dest="L", help="parameter to tune the tradeoff between precision and recall")
	parser.add_option("-C", default=10, type="int", dest="C", help="minimum occuurrence of a infobox")
	parser.add_option("-e", default=False, action="store_true", dest="evaluate", help="evaluate the predicted mapping")
	(options, args) = parser.parse_args()
	return options, args

def lca(root, e1, e2):
	if (root == e1) or (root == e2):
		return root
	if not G.has_key(root):
		return 0
	nodeList = []
	for child in G[root]:
		node = lca(child, e1, e2)
		if node != 0:
			nodeList.append(node)
	if len(nodeList) > 1:
		return root
	elif len(nodeList) == 1:
		return nodeList[0]
	else:
		return 0

def isin(root, node):
	if root == node:
		return True
	if not G.has_key(root):
		return False
	flag = False
	for child in G[root]:
		flag |= isin(child, node)
	return flag

def assign2(t1, t2):
	if t1 == config.MISSING_VALUE_STRING:
		return t2
	if t2 == config.MISSING_VALUE_STRING:
		return t1
	if t1 == t2:
		return t1
	ans = lca(Root, t1, t2)
	if ans == t1:
		return t2
	if ans == t2:
		return t1
	if ans == 0:
		print t1, t2
		print isin(Root, t1), isin(Root, t2)
		print G.has_key(t1), G.has_key(t2)
	return ans

def assign(typeString):
	types = typeString.split("\t")
	ans = assign2(types[0], types[1])
	for t in types[2:]:
		ans = assign2(ans, t)
	return ans

def main(options):
	lang = options.lang
	pivots = options.pivots.split("|")
	L = options.L
	C = options.C
	flag = options.evaluate
	print "[%s]: predict the mapping for language %s" % (time_utils._timestamp(), lang)

	drop_columns = ["template2", "article2"]
	dfList = []
	for pivot in pivots:
		df = pd.read_csv(config.ENTITY_MATRIX["%s2%s" % (lang, pivot)])
		df = df.drop(drop_columns, axis=1)
		df = df.rename(columns={"ontology":pivot})
		dfList.append(df)
	df = dfList[0]
	for df0 in dfList[1:]:
		df = pd.merge(df, df0, on=["article1", "template1"], how="outer")
	#print df.shape[0]
	msk = df[pivots[0]].notnull()
	for pivot in pivots[1:]:
		msk |= df[pivot].notnull()
	df = df[msk]
	df = df.fillna(config.MISSING_VALUE_STRING)
	df["str"] = df[pivots[0]]
	for pivot in pivots[1:]:
		df["str"] = df["str"] + "\t" + df[pivot]
	df["ontology"] = df["str"].apply(assign)
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
	msk = (res["occurrence"] > C) & (res["frequency"] > L)
	res = res[msk]
	res.to_csv(config.MAPPED_INFOBOX[lang], index=False)
	print "[%s]: prediction complete complete" % time_utils._timestamp()

	if flag:
		if not os.path.isfile(config.EXISTING_MAPPING_OUTPUT[lang]):
			parse.getExistingMapping(lang=lang)
		print "[%s]: evaluate the predicted mapping" % time_utils._timestamp()
		mapping = pd.read_csv(config.EXISTING_MAPPING_OUTPUT[lang], index_col="template")
		TP = 0 ; FP = 0
		for t, o in zip(res["template"], res["ontology"]):
			if t in mapping.index:
				if o == mapping.loc[t, "ontology"]:
					TP += 1
				else:
					FP += 1
		M = mapping.shape[0]
		print "True positives: %d" % TP
		print "False positives: %d" % FP
		print "False negatives: %d" % M-TP
		print "precision: %3f" % (1.0*TP/(TP + FP))
		print "recall:    %3f" % (1.0*TP/M)

		print "[%s]: evaluation complete" % time_utils._timestamp()

if __name__ == "__main__":
	parser = OptionParser()
	options, args = parse_args(parser)
	main(options)
