import config
import os
from optparse import OptionParser

def parse_args(parser):
	parser.add_option("-l", "--lang", default="en", type="string", dest="lang", help="specify the language to download")
	#parser.add_option("-m", "--mapping", default=True, action="store_false", dest="mapping", help="don't download dataset for existing mappings")
	#parser.add_option("-a", "--article", default=True, action="store_false", dest="article", help="don't download dataset for article template links")
	#parser.add_option("-i", "--inter", default=True, action="store_false", dest="inter", help="don't download dataset for interlanguage links")
	(options, args) = parser.parse_args()
	return options, args

def main(options):
	lang = options.lang
	#mapping = options.mapping
	#article = options.article
	#inter = options.inter

	# Download dataset for existing mappings
	if not os.path.isfile(config.EXISTING_MAPPING[lang]):
		cmd = "wget -P %s http://mappings.dbpedia.org/server/mappings/%s/pages/rdf/all" % (config.DATA_DIR + "/mapping/", lang)
		os.system(cmd)
		cmd = "mv %s %s" % (config.DATA_DIR + "/mapping/all", config.EXISTING_MAPPING[lang])
		os.system(cmd)

	# Download dataset for article template links
	if not os.path.isfile(config.ARTICLE_TEMPLATES[lang]):
		cmd = "wget -P %s http://downloads.dbpedia.org/2015-10/core-i18n/%s/article_templates_%s.ttl.bz2" % (config.DATA_DIR + "/article/", lang, lang)
		os.system(cmd)
		cmd = "bunzip2 %s" % (config.ARTICLE_TEMPLATES[lang] + ".bz2")
		os.system(cmd)

	# Download dataset for interlanguage links
	if not os.path.isfile(config.ILL[lang]):
		cmd = "wget -P %s http://downloads.dbpedia.org/2015-10/core-i18n/%s/interlanguage_links_%s.ttl.bz2" % (config.DATA_DIR + "/link/", lang, lang)
		os.system(cmd)
		cmd = "bunzip2 %s" % (config.ILL[lang] + ".bz2")
		os.system(cmd)

if __name__ == "__main__":
	parser = OptionParser()
	options, args = parse_args(parser)
	main(options)
