import rdflib.graph as g
import config
import sys
import pandas as pd
import numpy as np
import re
from utils import pkl_utils
reload(sys)
sys.setdefaultencoding('utf-8')

class BaseReplacer:
	def __init__(self, pattern_replace_pair_list=[]):
		self.pattern_replace_pair_list = pattern_replace_pair_list
	def transform(self, text):
		for pattern, replace in self.pattern_replace_pair_list:
			try:
				text = re.sub(pattern, replace, text)
			except:
				pass
		return re.sub(r"\s+", " ", text).strip()

class LowerCaseConverter(BaseReplacer):
	def transform(self, text):
		return text.lower()

class LetterLetterSplitter(BaseReplacer):
	def __init__(self):
		self.pattern_replace_pair_list = [
			(r"[_\-]", r" "),
		]

class UnitProcessor:
	def __init__(self, processors):
		self.processors = processors
	def process(self, s):
		for processor in self.processors:
			s = processor.transform(s)
		return s

class DataFrameProcessor:
	def __init__(self, processors):
		self.processors = processors
	def process(self, df):
		for processor in self.processors:
			df = df.apply(processor.transform)
		return df

class Template:
	def __init__(self, name, occurrence, properties, mapping=None, redirects=[]):
		self.name = name
		self.occurrence = occurrence
		self.propertyCount = len(properties)
		self.properties = properties
		self.mapping = mapping
		self.redirects = redirects
	
	def __str__(self):
		s = ""
		s += "Name: %s\n" % self.name
		s += "Occurrence: %d\n" % self.occurrence
		s += "Property Count: %d\n" % self.propertyCount
		s += "\n".join(p for p in self.properties)
		return s
	
	def isMapped(self):
		return self.mapping != None

	def isMatched(self, t):
		names = set(self.redirects + [self.name])
		return t in names

def getExistingMapping(lang="en"):
	G = g.Graph()
	G.parse(config.EXISTING_MAPPING[lang], format="n3")

	q = open(config.EXISTING_MAPPING_QUERY).read()
	results = G.query(q)
	mapping = [row[0] for row in results]
	ontology = [row[1] for row in results]
	df = pd.DataFrame({'mapping':mapping, 'ontology':ontology})

	processors = [
		LowerCaseConverter(),
		LetterLetterSplitter(),
	]
	processor = DataFrameProcessor(processors)

	df["template"] = processor.process(df["mapping"].apply(lambda x: x[47:]))
	df.to_csv(config.EXISTING_MAPPING_OUTPUT[lang], index=False)

def getStatistic(lang="en"):
	infile = open(config.MAPPING_STATS[lang])
	content = infile.readlines()
	infile.close()
	df = pd.read_csv(config.EXISTING_MAPPING_OUTPUT[lang], index_col="template")

	processors = [
		LowerCaseConverter(),
		LetterLetterSplitter(),
	]
	processor = UnitProcessor(processors)

	N = len(content)
	cursor = 0

	redirect = {}
	for i in range(3, N):
		templates = content[i].split('|')
		if len(templates) != 3:
			cursor = i + 3
			break
		t1 = processor.process(templates[1][9:])
		t2 = processor.process(templates[2][9:])
		if t1 in redirect:
			redirect[t1].append(t2)
		else:
			redirect[t1] = [t2]
		if t2 in redirect:
			redirect[t2].append(t1)
		else:
			redirect[t2] = [t1]

	templateList = []
	while cursor < N:
		if content[cursor][:18] == "template|Template:":
			name = processor.process(content[cursor][18:])
			cursor += 1
		else:
			print("[%d] Template Name Format Error: %s" % (cursor, content[cursor]))
			break
		if content[cursor][:6] == "count|":
			occurrence = int(content[cursor][6:].strip())
			cursor += 1
		else:
			print("[%d] Template Occurrence Format Error: %s" % (cursor, content[cursor]))
			break
		if content[cursor][:11] == "properties|":
			propertyCount = int(content[cursor][11:].strip())
			cursor += 1
		else:
			print("[%d] Template Property Count Format Error: %s" % (cursor, content[cursor]))
			break
		properties = [0] * propertyCount
		flag = False
		for i in range(propertyCount):
			if content[cursor][:2] == "p|":
				properties[i] = content[cursor][2:].strip()
				cursor += 1
			else:
				print("[%d] Template Property Format Error: %s" % (cursor, content[cursor]))
				flag = True
				break
		if flag: break
		redirects = []
		if name in redirect:
			redirects = redirect[name]
		if name in df.index:
			t = Template(name, occurrence, properties, df.loc(name, "ontology"), redirects)
		else:
			mapping = None
			for rd in redirects:
				if rd in df.index:
					mapping = df.loc(rd, "ontology")
					break
			t = Template(name, occurrence, properties, mapping, redirects)
		templateList.append(t)
		while cursor < N and content[cursor].isspace():
			cursor += 1
	
	pkl_utils._save(config.TEMPLATE_OUTPUT[lang], templateList)
	print("There are %d templates with lang:%s in total." % (len(templateList), lang))
	print("Among them, %d templates have been mapped" % sum([t.isMapped() for t in templateList]))

def main():
	#getStatistic(lang="en")
	#getStatistic(lang="zh")
	templates_en = pkl_utils._load(config.TEMPLATE_OUTPUT["en"])
	templates_zh = pkl_utils._load(config.TEMPLATE_OUTPUT["zh"])

	processors = [
		LowerCaseConverter(),
		LetterLetterSplitter(),
	]
	processor = UnitProcessor(processors)

	infile = open(config.TEMPLATE_LINKS["zh"])
	linkList = []
	for line in infile.readlines():
		items = line.split()
		t1 = processor.process(items[0][41:-1])
		t2 = processor.process(items[2][38:-1])
		if "/" in t1:
			continue
		linkList.append((t1, t2))
	c1 = 0; c2 = 0
	for link in linkList:
		for t in templates_zh:
			if t.isMatched(link[0]):
				c1 += 1
				break
		for t in templates_en:
			if t.isMatched(link[1]):
				c2 += 1
				break
	print c1, c2



if __name__ == "__main__":
	main()
