import config
import rdflib.graph as g
from utils import time_utils, pkl_utils
import pandas as pd

class Template:
	def __init__(self, url, articles, mapping=None, lang="en"):
		self.url = url
		self.occurrence = len(articles)
		self.articles = articles
		self.mapping = mapping
		self.lang = lang
	
	def __str__(self):
		return self.url

def parse(lang="en"):
	print time_utils._timestamp()
	G = g.Graph()
	G.parse(config.ARTICLE_TEMPLATES[lang], format="n3")
	print time_utils._timestamp()

	q = '''
SELECT * WHERE {
	?sub ?pred ?obj .
}'''
	results = G.query(q)
	templateDict = {}
	for row in results:
		article = row[0]
		template = row[1]
		if template in templateDict:
			templateDict[template].append(article)
		else:
			templateDict[template] = [article,]
	print "%d templates in total." % len(templateDict)
	df = pd.read_csv(config.EXISTING_MAPPING_OUTPUT[lang], index_col="mapping")
	templateList = []
	mapped_template = 0
	for template in templateDict:
		mapping = None
		if template in df.index:
			mapping = df.loc(template, "ontology")
			mapped_template += 1
		t = Template(template, templateDict[template], mapping, lang)
		templateList.append(t)
	pickle_utils._save(config.TEMPLATE_OUTPUT[lang], templateList)
	print "%d templates mapped" % mapped_template
	print time_utils._timestamp()

def main():
	parse()

if __name__ == "__main__":
	main()
