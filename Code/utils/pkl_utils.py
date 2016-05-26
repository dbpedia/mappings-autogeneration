import pickle

def _save(fname, data, protocal=-1):
	with open(fname, "wb") as f:
		pickle.dump(data, f, protocal)

def _load(fname):
	with open(fname, "rb") as f:
		return pickle.load(f)
