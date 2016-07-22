import os
import pandas as pd

def main():
	lang = "bg"
	pivots = "en|de|it|fr|pt|es"
	C = 10
	Ls = [0.1, 0.3, 0.5, 0.7, 0.9]
	#L = 0.5
	#Cs = [10, 20, 30, 50, 100]
	Ps = []; Rs = []
	for L in Ls:
		cmd = "python workflow.py -l %s -p \"%s\" -L %f -C %d -e -w > test.txt" % (lang, pivots, L, C)
		os.system(cmd)
		infile = open("test.txt")
		contents = infile.readlines()
		precision = float(contents[6][11:].strip())
		recall = float(contents[7][11:].strip())
		print precision, recall
		Ps.append(precision)
		Rs.append(recall)
	df = pd.DataFrame({"L":Ls, "precision":Ps, "recall":Rs})
	df.to_csv("data4.csv", index=False)


if __name__ == "__main__":
	main()


