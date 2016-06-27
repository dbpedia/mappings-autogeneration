import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("data1.csv")

grid_size = (1, 2)
plt.subplot2grid(grid_size, (0, 0), rowspan=1, colspan=1)
plt.plot(data["L"], data["precision"], marker="o")
plt.ylabel('Precision')
plt.xlabel('L')
plt.grid(True)

plt.subplot2grid(grid_size, (0, 1), rowspan=1, colspan=1)
plt.plot(data["L"], data["recall"], marker="o")
plt.ylabel('Recall')
plt.xlabel('L')
plt.grid(True)

plt.suptitle("Performance on bulgarian given 6 pivot languages with C = 10")
#plt.show()
plt.savefig('figure1.png')
