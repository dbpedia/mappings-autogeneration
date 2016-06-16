import pandas as pd
import rdflib.graph as g
from utils import time_utils, pkl_utils
import sys
import config
from optparse import OptionParser
reload(sys)
sys.setdefaultencoding('utf-8')

def parse_args(parser):
	parser.add_option("-l", "--lang", default="zh", type="string", dest="lang", help="target language")
	parser.add_option("-p", "--pivot", default="en", type="string", dest="pivot", help="pivot language")
	parser.add_option("-m", "--mapping", default=True, action="store_false", dest="mapping", help="don't get existing mapping for the pivot language")
	parser.add_option("-t", "--template", default=True, action="store_false", dest="template", help="don't get the dict from template to article for the target language")
	parser.add_option("-a", "--article", default=True, action="store_false", dest="article", help="don't get the dict from article to template for the pivot language")
	parser.add_option("-i", "--inter", default=True, action="store_false", dest="inter", help="don't get the interlanguage dict from the target language to the pivot language")
	(options, args) = parser.parse_args()
	return options, args

def getExistingMapping(lang="en"):
	print "[%s]: parse existing mapping for language %s" % (time_utils._timestamp(), lang)
	G = g.Graph()
	G.parse(config.EXISTING_MAPPING[lang], format="n3")

	q = '''
PREFIX rr: <http://www.w3.org/ns/r2rml#>

SELECT ?template ?class
WHERE {
	?template rr:subjectMap ?mapping .
	?mapping rr:class ?class .
}
'''
	results = G.query(q)
	mapping = [row[0] for row in results]
	ontology = [row[1] for row in results]
	df = pd.DataFrame({'mapping':mapping, 'ontology':ontology})

	df["template"] = df["mapping"].apply(lambda x: "Template:" + x[47:])
	df.to_csv(config.EXISTING_MAPPING_OUTPUT[lang], index=False)
	print "[%s]: parsing complete" % time_utils._timestamp()

def Template2Article(lang="en"):
	print "[%s]: generate template2article dict for language %s" % (time_utils._timestamp(), lang)
	infile = open(config.ARTICLE_TEMPLATES[lang])
	prefix = config.LANG_PREFIX[lang]
	len_prefix = len(prefix)
	templateDict = {}
	for line in infile.readlines():
		if line[0] != "<":
			continue
		row = line.split()
		article = row[0][1:-1]
		template = row[2][1:-1]
		article = article[len_prefix:]
		template = template[len_prefix:]

		if "/" in template:
			continue

		if template in templateDict:
			templateDict[template].append(article)
		else:
			templateDict[template] = [article, ]
	print "%d templates in total" % len(templateDict)
	pkl_utils._save(config.TEMPLATE2ARTICLE[lang], templateDict)
	print "[%s]: generation complete" % time_utils._timestamp()

def Article2Template(lang="en"):
	print "[%s]: generate article2template dict for language %s" % (time_utils._timestamp(), lang)
	infile = open(config.ARTICLE_TEMPLATES[lang])
	prefix = config.LANG_PREFIX[lang]
	len_prefix = len(prefix)
	articleDict = {}
	for line in infile.readlines():
		if line[0] != "<":
			continue
		row = line.split()
		article = row[0][1:-1]
		template = row[2][1:-1]
		article = article[len_prefix:]
		template = template[len_prefix:]

		if "/" in template:
			continue

		if article in articleDict:
			articleDict[article].append(template)
		else:
			articleDict[article] = [template, ]
	print "%d articles in total" % len(articleDict)
	pkl_utils._save(config.ARTICLE2TEMPLATE[lang], articleDict)
	print "[%s]: generation complete" % time_utils._timestamp()

def getILL(lang, target):
	print "[%s]: generate ILL dict from language %s to language %s" % (time_utils._timestamp(), lang, target)
	infile = open(config.ILL[lang])
	prefix1 = config.LANG_PREFIX[lang]
	prefix2 = config.LANG_PREFIX[target]
	len1 = len(prefix1)
	len2 = len(prefix2)
	linkDict = {}
	for line in infile.readlines():
		if line[0] != "<":
			continue
		row = line.split()
		lang1 = row[0][1:-1]
		lang2 = row[2][1:-1]
		if prefix1 not in lang1:
			continue
		if prefix2 not in lang2:
			continue
		lang1 = lang1[len1:]
		lang2 = lang2[len2:]
		linkDict[lang1] = lang2
	print "%d links in total" % len(linkDict)
	pkl_utils._save(config.ILL_DICT["%s2%s" % (lang, target)], linkDict)
	print "[%s]: generation complete" % time_utils._timestamp()

def process(lang, pivot):
	print "[%s]: process for language %s" % (time_utils._timestamp(), lang)
	linkDict = pkl_utils._load(config.ILL_DICT["zh2en"])
	templateDict = pkl_utils._load(config.TEMPLATE2ARTICLE[lang])
	articleDict = pkl_utils._load(config.ARTICLE2TEMPLATE[pivot])
	mapping = pd.read_csv(config.EXISTING_MAPPING_OUTPUT[pivot], index_col="template")
	template1 = []; template2 = []
	article1 = []; article2 = []; ontology = []
	for template in templateDict:
		articles = templateDict[template]
		for article in articles:
			if article in linkDict:
				tmp = linkDict[article]
				template1.append(template)
				article1.append(article)
				article2.append(tmp)
				if tmp in articleDict:
					templateList = articleDict[tmp]
				else:
					templateList = []
				c = ""
				t = ""
				for template in templateList:
					if template in mapping.index:
						c = mapping.at[template, "ontology"]
						t = template
				template2.append(t)
				ontology.append(c)

	data = {"template1":template1, "article1":article1, "template2":template2, \
			"article2":article2, "ontology":ontology}
	df = pd.DataFrame(data)
	df.to_csv(config.ENTITY_MATRIX["%s2%s" % (lang, pivot)], index=False)
	print "[%s]: processing complete" % time_utils._timestamp()


def main(options):
	lang = options.lang
	pivot = options.pivot
	mapping = options.mapping
	template = options.template
	article = options.article
	inter = options.inter
	
	if mapping:
		getExistingMapping(lang=pivot)
	
	if template:
		Template2Article(lang=lang)
	
	if article:
		Article2Template(lang=pivot)
	
	if inter:
		getILL(lang=lang, target=pivot)

	process(lang=lang, pivot=pivot)

if __name__ == "__main__":
	parser = OptionParser()
	options, args = parse_args(parser)
	main(options)
