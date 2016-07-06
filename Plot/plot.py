import matplotlib.pyplot as plt
import pandas as pd

d1 = pd.read_csv("data_without_wikidata.csv")
d2 = pd.read_csv("data_with_wikidata.csv")

grid_size = (2, 1)
plt.subplot2grid(grid_size, (0, 0), rowspan=1, colspan=1)
plt.plot(d1["L"], d1["precision"], marker="o", label="without wikidata")
plt.plot(d2["L"], d2["precision"], marker="o", label="with wikidata")
plt.ylabel('Precision')
plt.xlabel('L')
plt.xlim(0.1, 0.9)
plt.grid(True)
plt.legend(loc=2)

plt.subplot2grid(grid_size, (1, 0), rowspan=1, colspan=1)
plt.plot(d1["L"], d1["recall"], marker="o", label="without wikidata")
plt.plot(d2["L"], d2["recall"], marker="o", label="without wikidata")
plt.ylabel('Recall')
plt.xlabel('L')
plt.xlim(0.1, 0.9)
plt.grid(True)
plt.legend()

plt.suptitle("Performance on bulgarian given 6 pivot languages with C = 10")
#plt.show()
plt.savefig('figure1.png')
