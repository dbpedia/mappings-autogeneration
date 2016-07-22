from utils import time_utils
import config
from collections import defaultdict
import predict

def checkUniq(lang="en"):
	infile = open(config.INSTANCE_TYPES[lang])
	prefix = config.LANG_PREFIX[lang]
	len_prefix = len(prefix)
	typeDict = {}
	for line in infile.readlines():
		if line[0] != "<":
			continue
		row = line.split()
		instance = row[0][1:-1]
		ontology = row[2][1:-1]
		if prefix not in instance:
			continue
		instance = instance[len_prefix:]
		if instance in typeDict:
			typeDict[instance].append(ontology)
		else:
			typeDict[instance] = [ontology]
	for instance in typeDict:
		types = typeDict[instance]
		typeString = ""
		for t in types:
			if predict.isin(predict.Root, t):
				typeString += "\t" + t
		if len(typeString.split("\t")) > 2:
			ontology = predict.assign(typeString.strip())
			print instance, ontology



def main():
	checkUniq()

if __name__ == "__main__":
	main()
