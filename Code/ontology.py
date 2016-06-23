import config
from utils import time_utils, pkl_utils
import rdflib.graph as g

def main():
	print "[%s]: generate ontology hierarchy tree" % (time_utils._timestamp())
	G = g.Graph()
	G.parse(config.ONTOLOGY, format="n3")

	q = '''
PREFIX rr: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?child ?parent
WHERE {
	?child rr:subClassOf ?parent .
}'''
	
	results = G.query(q)
	ontologyDict = {}
	for row in results:
		child = str(row[0])
		parent = str(row[1])
		if parent in ontologyDict:
			ontologyDict[parent].append(child)
		else:
			ontologyDict[parent] = [child,]
	pkl_utils._save(config.ONTOLOGY_TREE, ontologyDict)
	print "[%s]: generation complete" % time_utils._timestamp()

if __name__ == "__main__":
	main()
