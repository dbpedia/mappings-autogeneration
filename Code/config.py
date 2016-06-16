
# --------------------- PATH ---------------------------

# Set the paths for data directory and output directory
ROOT_DIR = "../.."
DATA_DIR = "%s/data/DBpedia/Data" % ROOT_DIR
OUTPUT_DIR = "%s/data/DBpedia/Output" % ROOT_DIR


EXISTING_MAPPING = {
	"en" : "%s/mapping/existing_mapping_en.ttl" % DATA_DIR,
	"de" : "%s/mapping/existing_mapping_de.ttl" % DATA_DIR,
	"it" : "%s/mapping/existing_mapping_it.ttl" % DATA_DIR,
	"pt" : "%s/mapping/existing_mapping_pt.ttl" % DATA_DIR,
	"fr" : "%s/mapping/existing_mapping_fr.ttl" % DATA_DIR,
	"es" : "%s/mapping/existing_mapping_es.ttl" % DATA_DIR,
	"bg" : "%s/mapping/existing_mapping_bg.ttl" % DATA_DIR,
}

EXISTING_MAPPING_OUTPUT = {
	"en" : "%s/mapping/existing_mapping_en.csv" % OUTPUT_DIR,
	"de" : "%s/mapping/existing_mapping_de.csv" % OUTPUT_DIR,
	"it" : "%s/mapping/existing_mapping_it.csv" % OUTPUT_DIR,
	"pt" : "%s/mapping/existing_mapping_pt.csv" % OUTPUT_DIR,
	"fr" : "%s/mapping/existing_mapping_fr.csv" % OUTPUT_DIR,
	"es" : "%s/mapping/existing_mapping_es.csv" % OUTPUT_DIR,
	"bg" : "%s/mapping/existing_mapping_bg.csv" % OUTPUT_DIR,
}

ARTICLE_TEMPLATES = {
	"en" : "%s/article/article_templates_en.ttl" % DATA_DIR,
	"de" : "%s/article/article_templates_de.ttl" % DATA_DIR,
	"it" : "%s/article/article_templates_it.ttl" % DATA_DIR,
	"pt" : "%s/article/article_templates_pt.ttl" % DATA_DIR,
	"fr" : "%s/article/article_templates_fr.ttl" % DATA_DIR,
	"es" : "%s/article/article_templates_es.ttl" % DATA_DIR,
	"zh" : "%s/article/article_templates_zh.ttl" % DATA_DIR,
	"bg" : "%s/article/article_templates_bg.ttl" % DATA_DIR,
}

TEMPLATE2ARTICLE = {
	"en" : "%s/template2article/en.pkl" % OUTPUT_DIR,
	"de" : "%s/template2article/de.pkl" % OUTPUT_DIR,
	"it" : "%s/template2article/it.pkl" % OUTPUT_DIR,
	"pt" : "%s/template2article/pt.pkl" % OUTPUT_DIR,
	"fr" : "%s/template2article/fr.pkl" % OUTPUT_DIR,
	"es" : "%s/template2article/es.pkl" % OUTPUT_DIR,
	"zh" : "%s/template2article/zh.pkl" % OUTPUT_DIR,
	"bg" : "%s/template2article/bg.pkl" % OUTPUT_DIR,
}

ARTICLE2TEMPLATE = {
	"en" : "%s/article2template/en.pkl" % OUTPUT_DIR,
	"de" : "%s/article2template/de.pkl" % OUTPUT_DIR,
	"it" : "%s/article2template/it.pkl" % OUTPUT_DIR,
	"pt" : "%s/article2template/pt.pkl" % OUTPUT_DIR,
	"fr" : "%s/article2template/fr.pkl" % OUTPUT_DIR,
	"es" : "%s/article2template/es.pkl" % OUTPUT_DIR,
	"zh" : "%s/article2template/zh.pkl" % OUTPUT_DIR,
	"bg" : "%s/article2template/bg.pkl" % OUTPUT_DIR,
}

ILL = {
	"en" : "%s/link/interlanguage_links_en.ttl" % DATA_DIR,
	"de" : "%s/link/interlanguage_links_de.ttl" % DATA_DIR,
	"it" : "%s/link/interlanguage_links_it.ttl" % DATA_DIR,
	"fr" : "%s/link/interlanguage_links_fr.ttl" % DATA_DIR,
	"pt" : "%s/link/interlanguage_links_pt.ttl" % DATA_DIR,
	"es" : "%s/link/interlanguage_links_es.ttl" % DATA_DIR,
	"zh" : "%s/link/interlanguage_links_zh.ttl" % DATA_DIR,
	"bg" : "%s/link/interlanguage_links_bg.ttl" % DATA_DIR,
}

ILL_DICT = {
	"zh2en" : "%s/link/dict_zh2en.pkl" % OUTPUT_DIR,
	"zh2de" : "%s/link/dict_zh2de.pkl" % OUTPUT_DIR,
	"bg2en" : "%s/link/dict_bg2en.pkl" % OUTPUT_DIR,
}

ENTITY_MATRIX = {
	"zh2en" : "%s/matrix/zh2en.csv" % OUTPUT_DIR,
	"zh2de" : "%s/matrix/zh2de.csv" % OUTPUT_DIR,
	"bg2en" : "%s/matrix/bg2en.csv" % OUTPUT_DIR,
}

# --------------------- PARAM --------------------------
LANG_PREFIX = {
	"en" : "http://dbpedia.org/resource/",
	"de" : "http://de.dbpedia.org/resource/",
	"it" : "http://it.dbpedia.org/resource/",
	"fr" : "http://fr.dbpedia.org/resource/",
	"es" : "http://es.dbpedia.org/resource/",
	"pt" : "http://pt.dbpedia.org/resource/",
	"zh" : "http://zh.dbpedia.org/resource/",
	"bg" : "http://bg.dbpedia.org/resource/",
}

# --------------------- OTHER --------------------------
