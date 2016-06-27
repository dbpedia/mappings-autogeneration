import os
from optparse import OptionParser
import config

def parse_args(parser):
	parser.add_option("-l", "--lang", default="zh", type="string", dest="lang", help="target language")
	parser.add_option("-p", "--pivot", default="en", type="string", dest="pivots", help="pivot languages")
	parser.add_option("-L", default=0.5, type="float", dest="L", help="parameter to tune the tradeoff between precision and recall")
	parser.add_option("-C", default=10, type="int", dest="C", help="minimum occurrence of an infobox")
	parser.add_option("-e", default=False, action="store_true", dest="evaluate", help="evaluate the predicted mapping")
	(options, args) = parser.parse_args()
	return options, args

def main(options):
	lang = options.lang
	pivots = options.pivots.split("|")
	L = options.L
	C = options.C
	flag = options.evaluate

	if not os.path.isdir(config.DATA_DIR + "/mapping"):
		cmd = "mkdir %s" % (config.DATA_DIR + "/mapping")
		os.system(cmd)
	if not os.path.isdir(config.DATA_DIR + "/article"):
		cmd = "mkdir %s" % (config.DATA_DIR + "/article")
		os.system(cmd)
	if not os.path.isdir(config.DATA_DIR + "/article"):
		cmd = "mkdir %s" % (config.DATA_DIR + "/article")
		os.system(cmd)

	cmd = "python download.py -l %s" % lang
	os.system(cmd)

	for pivot in pivots:
		cmd = "python download.py -l %s" % pivot
		os.system(cmd)

	if not os.path.isdir(config.OUTPUT_DIR + "/template2article"):
		cmd = "mkdir %s" % (config.OUTPUT_DIR + "/template2article")
		os.system(cmd)
	if not os.path.isdir(config.OUTPUT_DIR + "/article2template"):
		cmd = "mkdir %s" % (config.OUTPUT_DIR + "/article2template")
		os.system(cmd)
	if not os.path.isdir(config.OUTPUT_DIR + "/link"):
		cmd = "mkdir %s" % (config.OUTPUT_DIR + "/link")
		os.system(cmd)
	if not os.path.isdir(config.OUTPUT_DIR + "/mapping"):
		cmd = "mkdir %s" % (config.OUTPUT_DIR + "/mapping")
		os.system(cmd)
	if not os.path.isdir(config.OUTPUT_DIR + "/matrix"):
		cmd = "mkdir %s" % (config.OUTPUT_DIR + "/matrix")
		os.system(cmd)
	if not os.path.isdir(config.OUTPUT_DIR + "/predicted"):
		cmd = "mkdir %s" % (config.OUTPUT_DIR + "/predicted")
		os.system(cmd)
	
	for pivot in pivots:
		cmd = "python parse.py -l %s -p %s" % (lang, pivot)
		os.system(cmd)
	
	cmd = "python predict.py -l %s -p \"%s\" -L %f -C %d" % (lang, options.pivots, L, C)
	if flag:
		cmd += " -e"
	os.system(cmd)


if __name__ == "__main__":
	parser = OptionParser()
	options, args = parse_args(parser)
	main(options)
