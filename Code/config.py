# -*- coding: utf-8 -*-
# --------------------- PATH ---------------------------

# Set the paths for data directory and output directory
ROOT_DIR = "/nfs/data1/pxu4"
DATA_DIR = "%s/DBpedia/Data" % ROOT_DIR
OUTPUT_DIR = "%s/DBpedia/Output" % ROOT_DIR

ONTOLOGY = "%s/dbpedia_2015-10.nt" % DATA_DIR
ONTOLOGY_TREE = "%s/ontology.pkl" % OUTPUT_DIR

EXISTING_MAPPING = {
	"en" : "%s/mapping/existing_mapping_en.ttl" % DATA_DIR,
	"de" : "%s/mapping/existing_mapping_de.ttl" % DATA_DIR,
	"it" : "%s/mapping/existing_mapping_it.ttl" % DATA_DIR,
	"pt" : "%s/mapping/existing_mapping_pt.ttl" % DATA_DIR,
	"fr" : "%s/mapping/existing_mapping_fr.ttl" % DATA_DIR,
	"es" : "%s/mapping/existing_mapping_es.ttl" % DATA_DIR,
	"bg" : "%s/mapping/existing_mapping_bg.ttl" % DATA_DIR,
	"zh" : "%s/mapping/existing_mapping_zh.ttl" % DATA_DIR,
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

INSTANCE_TYPES = {
	"en" : "%s/type/instance_types_en.ttl" % DATA_DIR,
	"de" : "%s/type/instance_types_de.ttl" % DATA_DIR,
	"it" : "%s/type/instance_types_it.ttl" % DATA_DIR,
	"pt" : "%s/type/instance_types_pt.ttl" % DATA_DIR,
	"fr" : "%s/type/instance_types_fr.ttl" % DATA_DIR,
	"es" : "%s/type/instance_types_es.ttl" % DATA_DIR,
	"wikidata" : "%s/type/instance_types_wikidata.ttl" % DATA_DIR,
	"bg" : "%s/type/instance_types_bg.ttl" % DATA_DIR,
	"zh" : "%s/type/instance_types_zh.ttl" % DATA_DIR,
}

LITERALS = {
	"en" : "%s/property/mappingbased_literals_en.ttl" % DATA_DIR,
	"de" : "%s/property/mappingbased_literals_de.ttl" % DATA_DIR,
	"bg" : "%s/property/mappingbased_literals_bg.ttl" % DATA_DIR,
}

OBJECTS = {
	"en" : "%s/property/mappingbased_objects_en.ttl" % DATA_DIR,
	"de" : "%s/property/mappingbased_objects_de.ttl" % DATA_DIR,
	"bg" : "%s/property/mappingbased_objects_bg.ttl" % DATA_DIR,
}

ENTITY = {
	"en" : "%s/tensor/entity_en.pkl" % OUTPUT_DIR,
	"de" : "%s/tensor/entity_de.pkl" % OUTPUT_DIR,
	"bg" : "%s/tensor/entity_bg.pkl" % OUTPUT_DIR,
}

PREDICATE = {
	"en" : "%s/tensor/predicate_en.pkl" % OUTPUT_DIR,
	"de" : "%s/tensor/predicate_de.pkl" % OUTPUT_DIR,
	"bg" : "%s/tensor/predicate_bg.pkl" % OUTPUT_DIR,
}

TENSOR = {
	"en" : "%s/tensor/tensor_en.pkl" % OUTPUT_DIR,
	"de" : "%s/tensor/tensor_de.pkl" % OUTPUT_DIR,
	"bg" : "%s/tensor/tensor_bg.pkl" % OUTPUT_DIR,
}

INSTANCE = {
	"en" : "%s/tensor/instance_en.pkl" % OUTPUT_DIR,
	"de" : "%s/tensor/instance_de.pkl" % OUTPUT_DIR,
	"bg" : "%s/tensor/instance_bg.pkl" % OUTPUT_DIR,
}

TYPE = {
	"en" : "%s/tensor/type_en.pkl" % OUTPUT_DIR,
	"de" : "%s/tensor/type_de.pkl" % OUTPUT_DIR,
	"bg" : "%s/tensor/type_bg.pkl" % OUTPUT_DIR,
}

TYPE_MATRIX = {
	"en" : "%s/tensor/type_matrix_en.pkl" % OUTPUT_DIR,
	"de" : "%s/tensor/type_matrix_de.pkl" % OUTPUT_DIR,
	"bg" : "%s/tensor/type_matrix_bg.pkl" % OUTPUT_DIR,
}

TYPE_DICT = {
	"en" : "%s/type/en.pkl" % OUTPUT_DIR,
	"de" : "%s/type/de.pkl" % OUTPUT_DIR,
	"it" : "%s/type/it.pkl" % OUTPUT_DIR,
	"pt" : "%s/type/pt.pkl" % OUTPUT_DIR,
	"fr" : "%s/type/fr.pkl" % OUTPUT_DIR,
	"es" : "%s/type/es.pkl" % OUTPUT_DIR,
	"wikidata" : "%s/type/wikidata.pkl" % OUTPUT_DIR,
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
	"zh2it" : "%s/link/dict_zh2it.pkl" % OUTPUT_DIR,
	"zh2fr" : "%s/link/dict_zh2fr.pkl" % OUTPUT_DIR,
	"zh2pt" : "%s/link/dict_zh2pt.pkl" % OUTPUT_DIR,
	"zh2es" : "%s/link/dict_zh2es.pkl" % OUTPUT_DIR,
	"zh2wikidata" : "%s/link/dict_zh2wikidata.pkl" % OUTPUT_DIR,
	"bg2en" : "%s/link/dict_bg2en.pkl" % OUTPUT_DIR,
	"bg2de" : "%s/link/dict_bg2de.pkl" % OUTPUT_DIR,
	"bg2it" : "%s/link/dict_bg2it.pkl" % OUTPUT_DIR,
	"bg2fr" : "%s/link/dict_bg2fr.pkl" % OUTPUT_DIR,
	"bg2pt" : "%s/link/dict_bg2pt.pkl" % OUTPUT_DIR,
	"bg2es" : "%s/link/dict_bg2es.pkl" % OUTPUT_DIR,
	"bg2wikidata" : "%s/link/dict_bg2wikidata.pkl" % OUTPUT_DIR,
}

ENTITY_MATRIX = {
	"zh2en" : "%s/matrix/zh2en.csv" % OUTPUT_DIR,
	"zh2de" : "%s/matrix/zh2de.csv" % OUTPUT_DIR,
	"zh2fr" : "%s/matrix/zh2fr.csv" % OUTPUT_DIR,
	"zh2pt" : "%s/matrix/zh2pt.csv" % OUTPUT_DIR,
	"zh2it" : "%s/matrix/zh2it.csv" % OUTPUT_DIR,
	"zh2es" : "%s/matrix/zh2es.csv" % OUTPUT_DIR,
	"zh2wikidata" : "%s/matrix/zh2wikidata.csv" % OUTPUT_DIR,
	"bg2en" : "%s/matrix/bg2en.csv" % OUTPUT_DIR,
	"bg2de" : "%s/matrix/bg2de.csv" % OUTPUT_DIR,
	"bg2it" : "%s/matrix/bg2it.csv" % OUTPUT_DIR,
	"bg2fr" : "%s/matrix/bg2fr.csv" % OUTPUT_DIR,
	"bg2pt" : "%s/matrix/bg2pt.csv" % OUTPUT_DIR,
	"bg2es" : "%s/matrix/bg2es.csv" % OUTPUT_DIR,
	"bg2wikidata" : "%s/matrix/bg2wikidata.csv" % OUTPUT_DIR,
}

MAPPED_INFOBOX = {
	"zh" : "%s/predicted/zh.csv" % OUTPUT_DIR,
	"bg" : "%s/predicted/bg.csv" % OUTPUT_DIR,
}

DATA_DICT = {
	"bg" : "%s/embedding/bg.pkl" % OUTPUT_DIR,
	"en" : "%s/embedding/en.pkl" % OUTPUT_DIR,
	"de" : "%s/embedding/de.pkl" % OUTPUT_DIR,
}

RESCAL_OUTPUT = {
	"en" : "%s/tensor/rescal_en.pkl" % OUTPUT_DIR,
	"de" : "%s/tensor/rescal_de.pkl" % OUTPUT_DIR,
	"bg" : "%s/tensor/rescal_bg.pkl" % OUTPUT_DIR,
}

HOLE_OUTPUT = {
	"en" : "%s/embedding/hole_en.pkl" % OUTPUT_DIR,
	"de" : "%s/embedding/hole_de.pkl" % OUTPUT_DIR,
	"bg" : "%s/embedding/hole_bg.pkl" % OUTPUT_DIR,
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
	"wikidata" : "http://wikidata.dbpedia.org/resource/",
}

TEMPLATE_NAME = {
	"en" : "Template:",
	"zh" : "Template:",
	"bg" : "Шаблон:",
	"de" : "Vorlage:",
	"it" : "Template:",
	"pt" : "Predefinição:",
	"fr" : "Modèle:",
	"es" : "Plantilla:",
}

MISSING_VALUE_STRING = "NA"

# --------------------- OTHER --------------------------
