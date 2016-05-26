

# ========================== PATH ----------------------
ROOT_DIR = ".."
DATA_DIR = "%s/Data" % ROOT_DIR
CODE_DIR = "%s/Code" % ROOT_DIR
OUTPUT_DIR = "%s/Output" % ROOT_DIR
QUERY_DIR = "%s/query" % CODE_DIR

EXISTING_MAPPING = { 
	"en" : "%s/mapping/existing_mapping_en.ttl" % DATA_DIR,
	"zh" : "%s/mapping/existing_mapping_zh.ttl" % DATA_DIR,
}
EXISTING_MAPPING_QUERY = "%s/existing_mapping.rq" % QUERY_DIR
EXISTING_MAPPING_OUTPUT = {
	"en" : "%s/existing_mapping_en.txt" % OUTPUT_DIR,
	"zh" : "%s/existing_mapping_zh.txt" % OUTPUT_DIR,
}

MAPPING_STATS = {
	"en" : "%s/templates/mappingstats_en.txt" % DATA_DIR,
	"zh" : "%s/templates/mappingstats_zh.txt" % DATA_DIR,
}

TEMPLATE_OUTPUT = {
	"en" : "%s/templates_en.pkl" % OUTPUT_DIR,
	"zh" : "%s/templates_zh.pkl" % OUTPUT_DIR,
}
