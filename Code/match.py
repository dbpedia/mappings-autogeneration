from utils import pkl_utils
import config
from parse import Template

def main():
	templates_en = pkl_utils._load(config.TEMPLATE_OUTPUT["en"])
	templates_zh = pkl_utils._load(config.TEMPLATE_OUTPUT["zh"])
	count = 0
	for t1 in templates_en:
		for t2 in templates_zh:
			if t1.isMatched(t2):
				count += 1
				break
	print count

if __name__ == "__main__":
	main()

